import daisyfl as fl
from daisyfl.common import (
    Task,
    ndarrays_to_parameters,
    parameters_to_ndarrays,
    FIT_SAMPLES,
    METRICS,
    LOSS,
    EVALUATE_SAMPLES,
    TID,
)
import argparse
from daisyfl.client.numpy_client import NumPyClient

# Define Flower Zone client
class ZoneClient(NumPyClient):
    def __init__(self, task_manager, master_address):
        self.task_manager = task_manager

        # Start Flower client
        fl.client.start_numpy_client(
            server_address=master_address,
            client=self,
        )

    def get_parameters(self, config):
        # return ndarrays
        if config.__contains__(TID):
            parameters = self.task_manager.get_parameters_api(config[TID])
            return parameters_to_ndarrays(parameters) if parameters is not None else None
        raise AttributeError

    def fit(self, parameters, config):
        report, tid =  self.task_manager.receive_task(ndarrays_to_parameters(parameters) , Task(config=config))
        config[TID] = tid
        parameters = self.get_parameters(config=config)
        # return (ndarrays, num_examples, metrics)
        return parameters, report.config[FIT_SAMPLES], report.config[METRICS]

    def evaluate(self, parameters, config):
        report, tid =  self.task_manager.receive_task(ndarrays_to_parameters(parameters) , Task(config=config))
        # return "loss, num_examples, metrics"
        return report.config[LOSS], report.config[EVALUATE_SAMPLES], report.config[METRICS]

    def stop_zone_server(self):
        self.task_manager.stop_zone_server_api()