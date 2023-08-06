# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Flower server."""


import concurrent.futures
import timeit
from logging import DEBUG, INFO
from typing import Dict, List, Optional, Tuple, Union

from daisyfl.common import (
    Task,
    Report,
    CURRENT_ROUND,
    EVALUATE,
    TIMEOUT,
    FIT_SAMPLES,
    EVALUATE_SAMPLES,
    LOSS,
    METRICS,
    Code,
    DisconnectRes,
    EvaluateIns,
    EvaluateRes,
    FitIns,
    FitRes,
    Parameters,
    ReconnectIns,
    Scalar,
)
from daisyfl.common.logger import log
from daisyfl.common.typing import GetParametersIns
from daisyfl.server.client_manager import ClientManager
from daisyfl.server.client_proxy import ClientProxy
from daisyfl.server.history import History
from daisyfl.server.strategy import FedAvg, Strategy

FitResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, FitRes]],
    List[Union[Tuple[ClientProxy, FitRes], BaseException]],
]
EvaluateResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, EvaluateRes]],
    List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
]
ReconnectResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, DisconnectRes]],
    List[Union[Tuple[ClientProxy, DisconnectRes], BaseException]],
]
    

class Server:
    """Flower server."""

    def __init__(
        self, *, 
        client_manager: ClientManager,
        strategy: Optional[Strategy] = None,
    ) -> None:
        self._client_manager: ClientManager = client_manager
        self.strategy: Strategy = strategy if strategy is not None else FedAvg()
        self.max_workers: Optional[int] = None

    def set_max_workers(self, max_workers: Optional[int]) -> None:
        """Set the max_workers used by ThreadPoolExecutor."""
        self.max_workers = max_workers

    def set_strategy(self, strategy: Strategy) -> None:
        """Replace server strategy."""
        self.strategy = strategy

    def client_manager(self) -> ClientManager:
        """Return ClientManager."""
        return self._client_manager

    def disconnect_all_clients(self, timeout: Optional[float]) -> None:
        """Send shutdown signal to all clients."""
        all_clients = self._client_manager.all()
        clients = [all_clients[k] for k in all_clients.keys()]
        instruction = ReconnectIns(seconds=None)
        client_instructions = [(client_proxy, instruction) for client_proxy in clients]
        _ = self._reconnect_clients(
            client_instructions=client_instructions,
            max_workers=self.max_workers,
            timeout=timeout,
        )

    def fit_round_api(
        self,
        parameters: Parameters,
        task: Task,
    ) -> Optional[
        Tuple[Optional[Parameters], Optional[Report]]
    ]:
        setattr(self.strategy.on_fit_config_fn, "_task", task.config)
        cur = task.config[CURRENT_ROUND]
        """Perform a single round fit."""
        
        # Get clients and their respective instructions from strategy
        client_instructions = self.strategy.configure_fit(
            server_round=cur,
            parameters=parameters,
            client_manager=self._client_manager,
        )

        if not client_instructions:
            log(INFO, "fit_round %s: no clients selected, cancel", cur)
            return None
        log(
            DEBUG,
            "fit_config: %s",
            client_instructions[0][1].config,
        )
        log(
            DEBUG,
            "fit_round %s: strategy sampled %s clients (out of %s)",
            cur,
            len(client_instructions),
            self._client_manager.num_available(),
        )

        # Collect `fit` results from all clients participating in this round
        results, failures = self._fit_clients(
            client_instructions=client_instructions,
            max_workers=self.max_workers,
            timeout=task.config[TIMEOUT],
        )
        log(
            DEBUG,
            "fit_round %s received %s results and %s failures",
            cur,
            len(results),
            len(failures),
        )

        # Parameters, Report in results -> (parameters, num_examples, metrics)
        results_for_aggregate = [(
            client, type('',(object,),{
                "parameters": res.parameters,
                "num_examples": res.config[FIT_SAMPLES],
                "metrics": res.config[METRICS],
            })()
        ) for client, res in results]

        # num_examples
        num_examples = int(sum([res.config[FIT_SAMPLES] for _, res in results]) / len(results))

        # Aggregate training results
        aggregated_result: Tuple[
            Optional[Parameters],
            Dict[str, Scalar],
        ] = self.strategy.aggregate_fit(cur, results_for_aggregate, failures)

        parameters_aggregated, metrics_aggregated = aggregated_result

        # (parameters, num_examples, metrics) -> Parameters, Report
        report = Report(config={
            CURRENT_ROUND: cur,
            FIT_SAMPLES: num_examples,
            METRICS: metrics_aggregated,
        })

        return parameters_aggregated, report
    
    def evaluate_round_api(
        self, 
        parameters: Parameters,
        task: Task,
    ) -> Optional[Report]:
        setattr(self.strategy.on_evaluate_config_fn, "_task", task.config)
        cur = task.config[CURRENT_ROUND]
        """Validate current global model on a number of clients."""

        # Get clients and their respective instructions from strategy
        client_instructions = self.strategy.configure_evaluate(
            server_round=cur,
            parameters=parameters,
            client_manager=self._client_manager,
        )
        if not client_instructions:
            log(INFO, "evaluate_round %s: no clients selected, cancel", cur)
            return None
        log(
            DEBUG,
            "evaluate_config: %s",
            client_instructions[0][1].config,
        )
        log(
            DEBUG,
            "evaluate_round %s: strategy sampled %s clients (out of %s)",
            cur,
            len(client_instructions),
            self._client_manager.num_available(),
        )

        # Collect `evaluate` results from all clients participating in this round
        results, failures = self._evaluate_clients(
            client_instructions,
            max_workers=self.max_workers,
            timeout=task.config[TIMEOUT],
        )
        log(
            DEBUG,
            "evaluate_round %s received %s results and %s failures",
            cur,
            len(results),
            len(failures),
        )

        # Report in results -> (loss, num_examples, metrics)
        results_for_aggregate = [(
            client, type('',(object,),{
                "loss": res.config[LOSS],
                "num_examples": res.config[EVALUATE_SAMPLES],
                "metrics": res.config[METRICS],
            })()
        ) for client, res in results]
        
        # num_examples
        num_examples = int(sum([res.config[EVALUATE_SAMPLES] for _, res in results]) / len(results))

        # Aggregate the evaluation results
        aggregated_result: Tuple[
            Optional[float],
            Dict[str, Scalar],
        ] = self.strategy.aggregate_evaluate(cur, results_for_aggregate, failures)

        loss_aggregated, metrics_aggregated = aggregated_result

        # (loss, num_examples, metrics) -> Report
        report = Report(config={
            CURRENT_ROUND: cur,
            LOSS: loss_aggregated,
            EVALUATE_SAMPLES: num_examples,
            METRICS: metrics_aggregated,
        })

        return report


    def _reconnect_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, ReconnectIns]],
        max_workers: Optional[int],
        timeout: Optional[float],
    ) -> ReconnectResultsAndFailures:
        """Instruct clients to disconnect and never reconnect."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            submitted_fs = {
                executor.submit(self._reconnect_client, client_proxy, ins, timeout)
                for client_proxy, ins in client_instructions
            }
            finished_fs, _ = concurrent.futures.wait(
                fs=submitted_fs,
                timeout=None,  # Handled in the respective communication stack
            )

        # Gather results
        results: List[Tuple[ClientProxy, DisconnectRes]] = []
        failures: List[Union[Tuple[ClientProxy, DisconnectRes], BaseException]] = []
        for future in finished_fs:
            failure = future.exception()
            if failure is not None:
                failures.append(failure)
            else:
                result = future.result()
                results.append(result)
        return results, failures


    def _reconnect_client(
        self,
        client: ClientProxy,
        reconnect: ReconnectIns,
        timeout: Optional[float],
    ) -> Tuple[ClientProxy, DisconnectRes]:
        """Instruct client to disconnect and (optionally) reconnect later."""
        disconnect = client.reconnect(
            reconnect,
            timeout=timeout,
        )
        return client, disconnect


    def _fit_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, FitIns]],
        max_workers: Optional[int],
        timeout: Optional[float],
    ) -> FitResultsAndFailures:
        """Refine parameters concurrently on all selected clients."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            submitted_fs = {
                executor.submit(self._fit_client, client_proxy, ins, timeout)
                for client_proxy, ins in client_instructions
            }
            finished_fs, _ = concurrent.futures.wait(
                fs=submitted_fs,
                timeout=None,  # Handled in the respective communication stack
            )

        # Gather results
        results: List[Tuple[ClientProxy, FitRes]] = []
        failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]] = []
        for future in finished_fs:
            self._handle_finished_future_after_fit(
                future=future, results=results, failures=failures
            )
        return results, failures


    def _fit_client(
        self,
        client: ClientProxy, ins: FitIns, timeout: Optional[float]
    ) -> Tuple[ClientProxy, FitRes]:
        """Refine parameters on a single client."""
        fit_res = client.fit(ins, timeout=timeout)
        return client, fit_res


    def _handle_finished_future_after_fit(
        self,
        future: concurrent.futures.Future,  # type: ignore
        results: List[Tuple[ClientProxy, FitRes]],
        failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
    ) -> None:
        """Convert finished future into either a result or a failure."""

        # Check if there was an exception
        failure = future.exception()
        if failure is not None:
            failures.append(failure)
            return

        # Successfully received a result from a client
        result: Tuple[ClientProxy, FitRes] = future.result()
        _, res = result

        # Check result status code
        if res.status.code == Code.OK:
            results.append(result)
            return

        # Not successful, client returned a result where the status code is not OK
        failures.append(result)


    def _evaluate_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, EvaluateIns]],
        max_workers: Optional[int],
        timeout: Optional[float],
    ) -> EvaluateResultsAndFailures:
        """Evaluate parameters concurrently on all selected clients."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            submitted_fs = {
                executor.submit(self._evaluate_client, client_proxy, ins, timeout)
                for client_proxy, ins in client_instructions
            }
            finished_fs, _ = concurrent.futures.wait(
                fs=submitted_fs,
                timeout=None,  # Handled in the respective communication stack
            )

        # Gather results
        results: List[Tuple[ClientProxy, EvaluateRes]] = []
        failures: List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]] = []
        for future in finished_fs:
            self._handle_finished_future_after_evaluate(
                future=future, results=results, failures=failures
            )
        return results, failures


    def _evaluate_client(
        self,
        client: ClientProxy,
        ins: EvaluateIns,
        timeout: Optional[float],
    ) -> Tuple[ClientProxy, EvaluateRes]:
        """Evaluate parameters on a single client."""
        evaluate_res = client.evaluate(ins, timeout=timeout)
        return client, evaluate_res


    def _handle_finished_future_after_evaluate(
        self,
        future: concurrent.futures.Future,  # type: ignore
        results: List[Tuple[ClientProxy, EvaluateRes]],
        failures: List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
    ) -> None:
        """Convert finished future into either a result or a failure."""

        # Check if there was an exception
        failure = future.exception()
        if failure is not None:
            failures.append(failure)
            return

        # Successfully received a result from a client
        result: Tuple[ClientProxy, EvaluateRes] = future.result()
        _, res = result

        # Check result status code
        if res.status.code == Code.OK:
            results.append(result)
            return

        # Not successful, client returned a result where the status code is not OK
        failures.append(result)
