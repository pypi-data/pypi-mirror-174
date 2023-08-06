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
from logging import INFO, WARNING
from typing import Dict, List, Optional, Tuple, TypedDict
from daisyfl.common.typing import NDArrays
from daisyfl.server import Server as BaseServer
from daisyfl.server.client_manager import ClientManager
from daisyfl.server.strategy import Strategy
from daisyfl.common import (
    FitIns,
    FitRes,
    Parameters,
    Scalar,
    Report,
    Task,
    CURRENT_ROUND,
    TIMEOUT,
    FIT_SAMPLES,
    METRICS,
    parameters_to_ndarrays,
    ndarrays_to_parameters,
)
from daisyfl.daisy.plugin.sec_agg.common.typing import (
    Proto,
    PROTO_KEY,
    SEC_AGG_PARAM_DICT,
    PUBLIC_KEYS,
    PUBLIC_KEYS_LIST,
    ShareKeysPacket,
    SHARE_KEYS_PACKETS,
    FORWARD_PACKETS,
    ShareRequest,
    SHARE_REQUEST,
    SHARE_RESPONSE,
)
from daisyfl.server.client_proxy import ClientProxy
from daisyfl.daisy.plugin.sec_agg.utils import primitives

from daisyfl.common.logger import log

FitResultsAndFailures = Tuple[List[Tuple[ClientProxy, FitRes]], List[BaseException]]

class Server(BaseServer):
    """Wrapper which adds SecAgg methods."""

    def __init__(
        self,
        s: BaseServer,
    ) -> None:
        self.server = s

    def disconnect_all_clients(self, timeout: Optional[float]) -> None:
        """Send shutdown signal to all clients."""
        self.server.disconnect_all_clients(timeout)

    def fit_round_api(
        self,
        parameters: Parameters,
        task: Task,
    ) -> Optional[
        Tuple[Optional[Parameters], Optional[Report]]
    ]:
        setattr(self.server.strategy.on_fit_config_fn, "_task", task.config)
        """Perform a single round fit."""
        # Get clients and their respective instructions from strategy
        client_instructions = self.server.strategy.configure_fit(
            server_round=task.config[CURRENT_ROUND],
            parameters=parameters,
            client_manager=self.server._client_manager,
        )

        # TODO: stages to APIs
        # === Stage 0: Setup ===
        log(INFO, "SecAgg Stage 0: Setting up Params")
        sec_agg_param_dict = get_sec_agg_param_dict(task,len(client_instructions))
        setup_dict: Dict[int, Tuple[ClientProxy, FitIns]] = \
            initialize_ins_dict(client_instructions)
        setup_dict = set_ins_stage(setup_dict, Proto.SETUP.value)
        setup_dict = set_sec_agg_param_dict(setup_dict, sec_agg_param_dict)
        # pass dummy parameters via gRPC
        setup_dict = set_ins_parameters(setup_dict, Parameters(tensors=[], tensor_type=""))
        client_instructions = client_ins_from_ins_dict(setup_dict)

        results_and_failures: FitResultsAndFailures = self.server._fit_clients(
            client_instructions=client_instructions,
            max_workers=self.server.max_workers,
            timeout=task.config[TIMEOUT],
        )
        results = results_and_failures[0]
        check_num_survivals(results, sec_agg_param_dict)
        
        # === Stage 1: Ask Public Keys ===
        log(INFO, "SecAgg Stage 1: Asking Keys")
        ask_keys_dict: Dict[int, Tuple[ClientProxy, FitIns]] = \
            next_ins_dict(setup_dict, results)
        ask_keys_dict = set_ins_stage(ask_keys_dict, Proto.ASK_KEYS.value)
        client_instructions = client_ins_from_ins_dict(ask_keys_dict)

        results_and_failures: FitResultsAndFailures = self.server._fit_clients(
            client_instructions=client_instructions,
            max_workers=self.server.max_workers,
            timeout=task.config[TIMEOUT],
        )
        results = results_and_failures[0]
        check_num_survivals(results, sec_agg_param_dict)

        # === Stage 2: Share Keys ===
        log(INFO, "SecAgg Stage 2: Sharing Keys")
        share_keys_dict: Dict[int, Tuple[ClientProxy, FitIns]] = \
            next_ins_dict(ask_keys_dict, results)
        share_keys_dict = set_ins_stage(share_keys_dict, Proto.SHARE_KEYS.value)
        share_keys_dict = set_pks_dict(share_keys_dict, results)
        client_instructions = client_ins_from_ins_dict(share_keys_dict)

        results_and_failures: FitResultsAndFailures = self.server._fit_clients(
            client_instructions=client_instructions,
            max_workers=self.server.max_workers,
            timeout=task.config[TIMEOUT],
        )
        results = results_and_failures[0]
        check_num_survivals(results, sec_agg_param_dict)

        # === Stage 3: Ask Vectors ===
        log(INFO, "SecAgg Stage 3: Asking Vectors")
        ask_vectors_dict = next_ins_dict(share_keys_dict, results)
        ask_vectors_dict = set_ins_stage(ask_vectors_dict, Proto.ASK_VECTORS.value)
        ask_vectors_dict = set_packet_list(ask_vectors_dict, results)
        # parameters for training
        ask_vectors_dict = set_ins_parameters(ask_vectors_dict, parameters)
        client_instructions = client_ins_from_ins_dict(ask_vectors_dict)

        results_and_failures: FitResultsAndFailures = self.server._fit_clients(
            client_instructions=client_instructions,
            max_workers=self.server.max_workers,
            timeout=task.config[TIMEOUT],
        )
        results = results_and_failures[0]
        check_num_survivals(results, sec_agg_param_dict)

        # === Stage 4: Unmask Vectors ===
        log(INFO, "SecAgg Stage 4: Unmasking Vectors")
        unmask_vectors_dict = next_ins_dict(ask_vectors_dict, results)
        unmask_vectors_dict = set_ins_stage(unmask_vectors_dict, Proto.UNMASK_VECTORS.value)
        masked_vectors, num_examples, metrics = aggregate_fit(results)
        unmask_vectors_dict = set_surviving_info(unmask_vectors_dict, ask_vectors_dict)
        # pass dummy parameters via gRPC
        unmask_vectors_dict = set_ins_parameters(unmask_vectors_dict, Parameters(tensors=[], tensor_type=""))
        client_instructions = client_ins_from_ins_dict(unmask_vectors_dict)
        
        results_and_failures: FitResultsAndFailures = self.server._fit_clients(
            client_instructions=client_instructions,
            max_workers=self.server.max_workers,
            timeout=task.config[TIMEOUT],
        )
        results = results_and_failures[0]
        check_num_survivals(results, sec_agg_param_dict)

        parameters_aggregated = unmask_vector(unmask_vectors_dict, ask_vectors_dict, masked_vectors, results, sec_agg_param_dict)

        # (parameters, num_examples, metrics) -> Parameters, Report
        report = Report(config={
            CURRENT_ROUND: task.config[CURRENT_ROUND],
            FIT_SAMPLES: num_examples,
            METRICS: metrics,
        })

        return parameters_aggregated, report

    def evaluate_round_api(
        self, 
        parameters: Parameters,
        task: Task,
    ) -> Optional[Report]:
        return self.server.evaluate_round_api(parameters, task)

def set_ins_parameters(
    ins_dict: Dict[int, Tuple[ClientProxy, FitIns]],
    parameters = Parameters,
) -> Dict[int, Tuple[ClientProxy, FitIns]]:
    for key, _ in ins_dict.items():
        ins_dict[key][1].parameters = parameters
    return ins_dict 

def set_ins_stage(
    ins_dict: Dict[int, Tuple[ClientProxy, FitIns]],
    proto_value: int,
) -> Dict[int, Tuple[ClientProxy, FitIns]]:
    for key, _ in ins_dict.items():
        ins_dict[key][1].config[PROTO_KEY] = proto_value
    return ins_dict

def process_sec_agg_param_dict(
    sec_agg_param_dict: Dict[str, Scalar],
    sample_num: int
) -> Dict[str, Scalar]:
    sec_agg_param_dict["sample_num"] = sample_num
    # min_num will be replaced with intended min_num based on sample_num
    # if both min_frac or min_num not provided, we take maximum of either 2 or 0.9 * sampled
    # if either one is provided, we use that
    # Otherwise, we take the maximum
    # Note we will eventually check whether min_num>=2
    if 'min_frac' not in sec_agg_param_dict:
        if 'min_num' not in sec_agg_param_dict:
            sec_agg_param_dict['min_num'] = max(
                2, int(0.9*sec_agg_param_dict['sample_num']))
    else:
        if 'min_num' not in sec_agg_param_dict:
            sec_agg_param_dict['min_num'] = int(
                sec_agg_param_dict['min_frac']*sec_agg_param_dict['sample_num'])
        else:
            sec_agg_param_dict['min_num'] = max(sec_agg_param_dict['min_num'], int(
                sec_agg_param_dict['min_frac']*sec_agg_param_dict['sample_num']))

    if 'share_num' not in sec_agg_param_dict:
        # Complete graph
        sec_agg_param_dict['share_num'] = sec_agg_param_dict['sample_num']
    elif sec_agg_param_dict['share_num'] % 2 == 0 and sec_agg_param_dict['share_num'] != sec_agg_param_dict['sample_num']:
        # we want share_num of each node to be either odd or sample_num
        log(WARNING, "share_num value changed due to sample num and share_num constraints! See documentation for reason")
        sec_agg_param_dict['share_num'] += 1

    if 'threshold' not in sec_agg_param_dict:
        sec_agg_param_dict['threshold'] = max(
            2, int(sec_agg_param_dict['share_num'] * 0.9))

    # Maximum number of example trained set to 1000
    if 'max_weights_factor' not in sec_agg_param_dict:
        sec_agg_param_dict['max_weights_factor'] = 50000

    # Quantization parameters
    if 'clipping_range' not in sec_agg_param_dict:
        sec_agg_param_dict['clipping_range'] = 3

    if 'target_range' not in sec_agg_param_dict:
        sec_agg_param_dict['target_range'] = 10000

    if 'mod_range' not in sec_agg_param_dict:
        sec_agg_param_dict['mod_range'] = sec_agg_param_dict['sample_num'] * \
            sec_agg_param_dict['target_range'] * \
            sec_agg_param_dict['max_weights_factor']

    log(
        INFO,
        "SecAgg parameters: %s",
        sec_agg_param_dict,
    )

    assert (
        sec_agg_param_dict['sample_num'] >= 2
        and sec_agg_param_dict['min_num'] >= 2
        and sec_agg_param_dict['sample_num'] >= sec_agg_param_dict['min_num']
        and sec_agg_param_dict['share_num'] <= sec_agg_param_dict['sample_num']
        and sec_agg_param_dict['threshold'] <= sec_agg_param_dict['share_num']
        and sec_agg_param_dict['threshold'] >= 2
        and (sec_agg_param_dict['share_num'] % 2 == 1 or sec_agg_param_dict['share_num'] == sec_agg_param_dict['sample_num'])
        and sec_agg_param_dict['target_range']*sec_agg_param_dict['sample_num']*sec_agg_param_dict['max_weights_factor'] <= sec_agg_param_dict['mod_range']
    ), "SecAgg parameters not accepted"
    return sec_agg_param_dict

def initialize_ins_dict(
    client_instructions = List[Tuple[ClientProxy, FitIns]],
) -> Dict[int, Tuple[ClientProxy, FitIns]]:
    ins_dict: Dict[int, Tuple[ClientProxy, FitIns]] = {}
    for idx, value in enumerate(client_instructions):
        ins = value[0], FitIns(value[1].parameters, value[1].config.copy())
        ins_dict[idx] = ins
    return ins_dict

def next_ins_dict(
    ins_dict: Dict[int, Tuple[ClientProxy, FitIns]],
    results: List[Tuple[ClientProxy, FitRes]],
) -> Dict[int, Tuple[ClientProxy, FitIns]]:
    next_ins_dict = {}
    for idx, ins in ins_dict.items():
        if ins[0] in [result[0] for result in results]:
            next_ins_dict[idx] = ins
            for i in [
                SEC_AGG_PARAM_DICT,
                PUBLIC_KEYS,
                PUBLIC_KEYS_LIST,
                SHARE_KEYS_PACKETS,
                FORWARD_PACKETS,
                SHARE_REQUEST,
                SHARE_RESPONSE,
            ]:
                try:
                    del next_ins_dict[idx][1].config[i]
                except:
                    pass
    return next_ins_dict

def client_ins_from_ins_dict(
    ins_dict: Dict[int, Tuple[ClientProxy, FitIns]],
) -> List[Tuple[ClientProxy, FitIns]]:
    return [ins for _, ins in ins_dict.items()]

def check_num_survivals(
    results: List[Tuple[ClientProxy, FitRes]],
    sec_agg_param_dict: Dict,
) -> None:
    if len(results) < sec_agg_param_dict['min_num']:
        raise Exception("Not enough available clients")

def check_enough_shares(
    share_list: List[bytes],
    sec_agg_param_dict: Dict,
) -> None:
    if len(share_list) < sec_agg_param_dict['threshold']:
        raise Exception(
            "Not enough shares to recover secret in unmask vectors stage"
        )

def get_sec_agg_param_dict(
    task: Task,
    num_instructions: int,
) -> Dict[int, Tuple[ClientProxy, FitIns]]:
    sec_agg_param_dict = task.config[SEC_AGG_PARAM_DICT] \
        if task.config.__contains__(SEC_AGG_PARAM_DICT) else {}
    sec_agg_param_dict = process_sec_agg_param_dict(sec_agg_param_dict, num_instructions)
    return sec_agg_param_dict

def set_sec_agg_param_dict(
    ins_dict: Dict[int, Tuple[ClientProxy, FitIns]],
    sec_agg_param_dict: Dict,
) -> Dict[int, Tuple[ClientProxy, FitIns]]:
    for key, _ in ins_dict.items():
        tmp = sec_agg_param_dict.copy()
        tmp["sec_agg_id"] = key
        ins_dict[key][1].config[SEC_AGG_PARAM_DICT] = tmp
    return ins_dict

def set_pks_dict(
    ins_dict: Dict[int, Tuple[ClientProxy, FitIns]],
    results: List[Tuple[ClientProxy, FitRes]],
) -> Dict[int, Tuple[ClientProxy, FitIns]]:
    pks_dict = {}
    for result in results:
        for idx, ins in ins_dict.items():    
            if ins[0] == result[0]:
                pks_dict[idx] = result[1].config[PUBLIC_KEYS]
                break
    for key, _ in ins_dict.items():
        ins_dict[key][1].config[PUBLIC_KEYS_LIST] = pks_dict

    return ins_dict

def set_packet_list(
    ins_dict: Dict[int, Tuple[ClientProxy, FitIns]],
    results: List[Tuple[ClientProxy, FitRes]],
) -> Dict[int, Tuple[ClientProxy, FitIns]]:
    total_packet_list: List[dict] = []
    for _, ins in ins_dict.items():
        pos = [result[0] for result in results].index(ins[0])
        packet_list = results[pos][1].config[SHARE_KEYS_PACKETS]
        total_packet_list += packet_list
    
    for idx, _ in ins_dict.items():
        ins_dict[idx][1].config[FORWARD_PACKETS] = []

    for packet in total_packet_list:
        destination = packet["destination"]
        if destination in ins_dict.keys():
            ins_dict[destination][1].config[FORWARD_PACKETS].append(packet)

    return ins_dict

def aggregate_fit(
    results: List[Tuple[ClientProxy, FitRes]],
) -> Tuple[NDArrays, int, TypedDict]:
    # Get shape of vector sent by first client
    masked_vectors = primitives.weights_zero_generate(
        [i.shape for i in parameters_to_ndarrays(results[0][1].parameters)]
    )
    total_examples = 0
    for result in results:
        masked_vectors = primitives.weights_addition(
            masked_vectors, parameters_to_ndarrays(result[1].parameters)
        )
        num_examples = result[1].config[FIT_SAMPLES]
        total_examples = total_examples + num_examples

    avg_examples = int(total_examples / len(results))
    
    return masked_vectors, avg_examples, {}

def set_surviving_info(
    survivals_dict: Dict[int, Tuple[ClientProxy, FitIns]],
    participants_dict: Dict[int, Tuple[ClientProxy, FitIns]],
) -> Dict[int, Tuple[ClientProxy, FitIns]]:
    survivals = [idx for idx, _ in survivals_dict.items()]
    dropouts = []
    for idx, _ in participants_dict.items():
        if idx not in survivals:
            dropouts.append(idx)
    share_request: dict = ShareRequest(survivals=survivals, dropouts=dropouts).to_dict()
    
    for idx, _ in survivals_dict.items():
        survivals_dict[idx][1].config[SHARE_REQUEST] = share_request
    return survivals_dict

def unmask_vector(
    survivals_dict: Dict[int, Tuple[ClientProxy, FitIns]],
    participants_dict: Dict[int, Tuple[ClientProxy, FitIns]],
    masked_vectors: NDArrays,
    results: List[Tuple[ClientProxy, FitRes]],
    sec_agg_param_dict: Dict,
) -> Parameters:
    collected_shares_dict: Dict[int, List[bytes]] = {}
    for idx in participants_dict.keys():
        collected_shares_dict[idx] = []

    for result in results:
        for owner_id, share in result[1].config[SHARE_RESPONSE]["share_dict"].items():
            collected_shares_dict[owner_id].append(share)
    
    # Remove masks
    for client_id, share_list in collected_shares_dict.items():
        check_enough_shares(share_list, sec_agg_param_dict)
        secret = primitives.combine_shares(share_list=share_list)

        # survivals
        if client_id in survivals_dict.keys():
            # unmask b
            mask_b = primitives.pseudo_rand_gen(
                secret, sec_agg_param_dict['mod_range'], primitives.weights_shape(masked_vectors)
            )
            masked_vectors = primitives.weights_subtraction(masked_vectors, mask_b)
        else:
            # dropouts
            # get neighbor_list
            # neighbor is a client with whom "client_id" shared its key-shares
            neighbor_list: List[int] = []
            if sec_agg_param_dict['share_num'] == sec_agg_param_dict['sample_num']:
                # SecAgg
                # share with all other clients
                neighbor_list = list(participants_dict.keys())
                neighbor_list.remove(client_id)
            else:
                # SecAgg+
                for i in range(-int(sec_agg_param_dict['share_num'] / 2), int(sec_agg_param_dict['share_num'] / 2) + 1):
                    neighbor_id = (i + client_id) % sec_agg_param_dict['sample_num']
                    if i != 0 and neighbor_id in participants_dict.keys():
                        neighbor_list.append(neighbor_id)
            # unmask sk1
            for neighbor_id in neighbor_list:
                shared_key = primitives.generate_shared_key(
                    primitives.bytes_to_private_key(secret),
                    primitives.bytes_to_public_key(participants_dict[neighbor_id][1].config[PUBLIC_KEYS]["pk1"]),
                )
                pairwise_mask = primitives.pseudo_rand_gen(
                    shared_key, sec_agg_param_dict['mod_range'], primitives.weights_shape(masked_vectors)
                )
                if client_id > neighbor_id:
                    masked_vectors = primitives.weights_addition(
                        masked_vectors, pairwise_mask
                    )
                else:
                    masked_vectors = primitives.weights_subtraction(
                        masked_vectors, pairwise_mask
                    )
    masked_vectors = primitives.weights_mod(
        masked_vectors, sec_agg_param_dict['mod_range']
    )
    total_weights_factor, masked_vectors = primitives.factor_weights_extract(masked_vectors)
    masked_vectors = primitives.weights_divide(masked_vectors, total_weights_factor)
    aggregated_vector = primitives.reverse_quantize(
        masked_vectors, sec_agg_param_dict['clipping_range'], sec_agg_param_dict['target_range']
    )
    aggregated_parameters = ndarrays_to_parameters(aggregated_vector)
    return aggregated_parameters