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
"""Flower server app."""


from dataclasses import dataclass
from logging import INFO, WARN
from typing import Optional, Tuple, Dict, Callable, List

from daisyfl.common.logger import log
from daisyfl.common import (
    Type,
    Task,
    Scalar,
    NUM_ROUNDS,
    CURRENT_ROUND,
    EVALUATE,
    TIMEOUT,
    GRPC_MAX_MESSAGE_LENGTH,
    Parameters,
    decode_ndarrays,
    ndarrays_to_parameters,
    parameter,
    PLUGIN,
    PIDS,
)
from daisyfl.proto.driver_pb2_grpc import add_DriverServicer_to_server
from daisyfl.proto.transport_pb2_grpc import add_FlowerServiceServicer_to_server
from daisyfl.server.client_manager import ClientManager, SimpleClientManager
from daisyfl.server.driver.driver_servicer import DriverServicer
from daisyfl.server.grpc_server.flower_service_servicer import FlowerServiceServicer
from daisyfl.server.grpc_server.grpc_server import (
    generic_create_grpc_server,
    start_grpc_server,
)
from daisyfl.server.history import History
from daisyfl.server.server import Server
from daisyfl.server.task_manager import TaskManager
from daisyfl.server.strategy import FedAvg, Strategy

import os
import signal

DEFAULT_SERVER_ADDRESS = "[::]:8080"
DEFAULT_SERVER_ADDRESS_DRIVER = "[::]:9091"
DEFAULT_SERVER_ADDRESS_FLEET = "[::]:9092"

@dataclass
class ServerConfig:
    """Flower server config.
    All attributes have default values which allows users to configure
    just the ones they care about.
    """

    num_rounds: int = 1
    round_timeout: Optional[float] = None
    config_storage = {}


def start_server(  # pylint: disable=too-many-arguments
    *,
    # task manager
    task_manager: Optional[TaskManager] = None,
    num_rounds: int = 3,
    timeout: Optional[int] = 100000,
    zone: bool = False,
    master_address: str = "",
    model_path: str = "",
    on_configure_task_fn: Optional[Callable[[Dict[str, Scalar]], List[Dict[str, Scalar]]]] = None,
    # server
    server: Optional[Server] = None,
    server_address: str = DEFAULT_SERVER_ADDRESS,
    client_manager: Optional[ClientManager] = None,
    # strategy
    strategy: Optional[Strategy] = None,
    # grpc
    grpc_max_message_length: int = GRPC_MAX_MESSAGE_LENGTH,
    certificates: Optional[Tuple[bytes, bytes, bytes]] = None,
) -> History:
    """Start a Flower server using the gRPC transport layer.

    Arguments
    ---------
    server_address : Optional[str]
        The IPv4 or IPv6 address of the server. Defaults to `"[::]:8080"`.
    server : Optional[flwr.server.Server] (default: None)
        A server implementation, either `flwr.server.Server` or a subclass
        thereof. If no instance is provided, then `start_server` will create
        one.
    config : ServerConfig (default: None)
        Currently supported values are `num_rounds` (int, default: 1) and
        `round_timeout` in seconds (float, default: None).
    strategy : Optional[flwr.server.Strategy] (default: None).
        An implementation of the abstract base class
        `flwr.server.strategy.Strategy`. If no strategy is provided, then
        `start_server` will use `flwr.server.strategy.FedAvg`.
    client_manager : Optional[flwr.server.ClientManager] (default: None)
        An implementation of the abstract base class
        `flwr.server.ClientManager`. If no implementation is provided, then
        `start_server` will use
        `flwr.server.client_manager.SimpleClientManager`.
    grpc_max_message_length : int (default: 536_870_912, this equals 512MB)
        The maximum length of gRPC messages that can be exchanged with the
        Flower clients. The default should be sufficient for most models.
        Users who train very large models might need to increase this
        value. Note that the Flower clients need to be started with the
        same value (see `flwr.client.start_client`), otherwise clients will
        not know about the increased limit and block larger messages.
    certificates : Tuple[bytes, bytes, bytes] (default: None)
        Tuple containing root certificate, server certificate, and private key
        to start a secure SSL-enabled server. The tuple is expected to have
        three bytes elements in the following order:

            * CA certificate.
            * server certificate.
            * server private key.

    Returns
    -------
    hist : flwr.server.history.History
        Object containing training and evaluation metrics.

    Examples
    --------
    Starting an insecure server:

    >>> start_server()

    Starting an SSL-enabled server:

    >>> start_server(
    >>>     certificates=(
    >>>         Path("/crts/root.pem").read_bytes(),
    >>>         Path("/crts/localhost.crt").read_bytes(),
    >>>         Path("/crts/localhost.key").read_bytes()
    >>>     )
    >>> )
    """
    # zone or master
    manager_type = Type.ZONE if zone else Type.MASTER
    
    # initial parameters
    def initialize_parameters(model_path: str) -> Parameters:
        # FL Starting
        log(INFO, "FL starting")
        log(INFO, "Initializing global parameters")
        with open(model_path, "r") as f:
            return ndarrays_to_parameters(decode_ndarrays(f.read()))
    # initial task
    def initialize_task(num_rounds: int, timeout: int) -> Task:
        return Task(config={
            NUM_ROUNDS: num_rounds,
            CURRENT_ROUND: 0,
            EVALUATE: False,
            TIMEOUT: timeout,
            PLUGIN: "sec_agg",
        })

    # Initialize server and task manager
    initialized_server, initialized_task_manager = _init_defaults(
        # task manager
        task_manager=task_manager,
        manager_type=manager_type,
        master_address=master_address,
        on_configure_task_fn=on_configure_task_fn,
        # server
        server=server,
        client_manager=client_manager,
        # strategy
        strategy=strategy,
    )
    log(INFO, "Starting Flower server",)

    # Start gRPC server
    grpc_server = start_grpc_server(
        client_manager=initialized_server.client_manager(),
        server_address=server_address,
        max_message_length=grpc_max_message_length,
        certificates=certificates,
    )
    log(
        INFO,
        "Flower ECE: gRPC server running , SSL is %s",
        "enabled" if certificates is not None else "disabled",
    )

    # Update running pids info
    def housekeeping_entry():
        pid = str(os.getpid())
        housekeeping_exit.pid = pid
        os.system("mkdir -p " + PIDS)
        with open(PIDS + pid + ".txt", "w") as f:
            f.write(pid)
    
    # Shut down
    def housekeeping_exit():
        if hasattr(housekeeping_exit, "pid"):
            # Discconect all clients
            initialized_server.disconnect_all_clients(timeout=None)
            # Stop the gRPC server
            grpc_server.stop(grace=1)
            os.remove(PIDS + housekeeping_exit.pid + ".txt")
        else:
            raise AttributeError
    
    # Interrupt
    def handler(signum, frame,):
        housekeeping_exit()
        exit(1)

    housekeeping_entry()
    signal.signal(signal.SIGINT, handler)

    # for zones: do nothing but wait until the master call "stop"
    # return server.hist
    if initialized_task_manager.type == Type.MASTER:
        parameters = initialize_parameters(model_path)
        task = initialize_task(num_rounds=num_rounds, timeout=timeout)
        # Start training
        hist = _fl(
            task_manager=initialized_task_manager,
            parameters=parameters,
            task=task,
        )
    else:
        with initialized_task_manager._cnd_stop:
            initialized_task_manager._cnd_stop.wait()
        hist = initialized_task_manager.history

    housekeeping_exit()

    return hist


def _init_defaults(
    # task manager
    task_manager: Optional[TaskManager],
    manager_type: Optional[Type],
    master_address: Optional[str],
    on_configure_task_fn: Optional[Callable[[Dict[str, Scalar]], List[Dict[str, Scalar]]]],
    # server
    server: Optional[Server],
    client_manager: Optional[ClientManager],
    # strategy
    strategy: Optional[Strategy],
) -> Tuple[Server, TaskManager]:
    # Create task manager instance if none was given
    if task_manager is None:
        if server is None:
            if client_manager is None:
                client_manager = SimpleClientManager()
            if strategy is None:
                strategy = FedAvg()
            server = Server(client_manager=client_manager, strategy=strategy)
        # Start task manager
        task_manager = TaskManager(
            server=server,
            manager_type=manager_type,
            master_address=master_address,
            on_configure_task_fn=on_configure_task_fn,
        )
    
    elif strategy is not None:
        log(WARN, "Task manager, server and strategy were provided, ignoring strategy")

    return server, task_manager


def _fl(
    task_manager: TaskManager,
    parameters: Parameters,
    task: Task,
) -> History:
    # Fit model
    report, _ = task_manager.receive_task(parameters=parameters, task=task)
    hist = task_manager.history

    log(INFO, "app_fit: losses_distributed %s", str(hist.losses_distributed))
    log(INFO, "app_fit: metrics_distributed %s", str(hist.metrics_distributed))
    log(INFO, "app_fit: losses_centralized %s", str(hist.losses_centralized))
    log(INFO, "app_fit: metrics_centralized %s", str(hist.metrics_centralized))
    log(INFO, "report: %s", str(report))

    return hist


def run_server() -> None:
    """Run Flower server."""
    log(INFO, "Starting Flower server")

    client_manager: ClientManager = SimpleClientManager()

    # Create Driver API gRPC server
    driver_server_address: str = DEFAULT_SERVER_ADDRESS_DRIVER
    driver_servicer = DriverServicer(client_manager=client_manager)
    driver_add_servicer_to_server_fn = add_DriverServicer_to_server
    driver_grpc_server = generic_create_grpc_server(
        servicer_and_add_fn=(driver_servicer, driver_add_servicer_to_server_fn),
        server_address=driver_server_address,
        max_message_length=GRPC_MAX_MESSAGE_LENGTH,
        certificates=None,
    )

    # Create (legacy) Fleet API gRPC server
    fleet_server_address: str = DEFAULT_SERVER_ADDRESS_FLEET
    fleet_servicer = FlowerServiceServicer(client_manager=client_manager)
    fleet_add_servicer_to_server_fn = add_FlowerServiceServicer_to_server
    fleet_grpc_server = generic_create_grpc_server(
        servicer_and_add_fn=(fleet_servicer, fleet_add_servicer_to_server_fn),
        server_address=fleet_server_address,
        max_message_length=GRPC_MAX_MESSAGE_LENGTH,
        certificates=None,
    )

    # Start Driver API gRPC server
    driver_grpc_server.start()
    log(
        INFO,
        "Flower ECE: driver gRPC server running on %s",
        driver_server_address,
    )

    # Start (legacy) Fleet API gRPC server
    fleet_grpc_server.start()
    log(
        INFO,
        "Flower ECE: fleet gRPC server running on %s",
        fleet_server_address,
    )

    # Wait for termination of both servers
    driver_grpc_server.wait_for_termination()
    fleet_grpc_server.wait_for_termination()
