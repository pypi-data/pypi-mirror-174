from ast import Param
import timeit
from logging import DEBUG, INFO
from typing import Dict, List, Optional, Tuple, Union, Callable

from daisyfl.common import (
    NUM_ROUNDS,
    CURRENT_ROUND,
    EVALUATE,
    TIMEOUT,
    FIT_SAMPLES,
    EVALUATE_SAMPLES,
    LOSS,
    METRICS,
    decode_ndarrays,
    ndarrays_to_parameters,
    parameters_to_ndarrays,
    Code,
    DisconnectRes,
    EvaluateIns,
    EvaluateRes,
    FitIns,
    FitRes,
    Parameters,
    ReconnectIns,
    Scalar,
    Task,
    Report,
    MetaTask,
    PLUGIN,
)
from daisyfl.common.logger import log
from daisyfl.common.typing import GetParametersIns
from daisyfl.server.server import Server
from daisyfl.server.history import History
from daisyfl.common import Type
from daisyfl.utils import DynamicLoader

from daisyfl.client import ZoneClient
import threading

class TaskManager():
    """Task manager."""

    def __init__(
        self,
        server: Server,
        manager_type: Type,
        master_address: str,
        on_configure_task_fn: Optional[Callable[[Parameters, Dict[str, Scalar]], List[Dict[str, Scalar]]]],
    ) -> None:
        self.start_times: List[(int, float)] = []
        self.server: Server = server
        self.type: Type = manager_type
        self.zone_client = threading.Thread(target=ZoneClient, args=(self, master_address)).start() \
            if self.type == Type.ZONE else None

        # MetaTask
        self.meta_tasks: List[MetaTask] = []
        # TODO: policy of on_configure_task_fn
        self.on_configure_task_fn: List[(int, Callable)] = []
        
        # for zones: wait for receiving tasks sent from master
        self._cnd_stop = threading.Condition()
        self.history = History()

    def receive_task(self, parameters: Parameters, task: Task) -> Tuple[Report, int]:
        # set task attributes
        # TODO: tid management
        tid = self.get_tid()
        start_time = timeit.default_timer()
        configured_tasks = self.configure_task(task)
        meta_task = MetaTask(
            tid=tid,
            start_time=start_time,
            task=task,
            parameters=parameters,
            configured_tasks=configured_tasks,
        )
        self.append_meta_task(meta_task)
        log(DEBUG, "create MetaTask with task %s", meta_task.task)

        # assign tasks one by one
        report = self.assign_tasks(tid)
        # TODO: complete
        # self.pop_meta_task(tid)
        # return the last report
        return report, tid

    # How to configure the current task
    def configure_task(self, task: Task) -> List[Task]:
        # configure an evaluation task
        if task.config[EVALUATE]:
            return [Task(config={
                NUM_ROUNDS: 1,
                CURRENT_ROUND: task.config[CURRENT_ROUND],
                EVALUATE: True,
                TIMEOUT: task.config[TIMEOUT],
                PLUGIN: task.config[PLUGIN],
            })]

        # configure fitting tasks
        tasks: List[Task] = []
        for i in range(task.config[NUM_ROUNDS]):
            # append a fitting task
            tasks.append(Task(config={
                NUM_ROUNDS: 1,
                CURRENT_ROUND: task.config[CURRENT_ROUND] + i,
                EVALUATE: False,
                TIMEOUT: task.config[TIMEOUT],
                PLUGIN: task.config[PLUGIN],
            }))
            if self.type == Type.MASTER:
                # append a local evaluation task
                # NUM_ROUNDS: -1 -> let assign_tasks know it is a local evaluation
                tasks.append(Task(config={
                    NUM_ROUNDS: -1,
                    CURRENT_ROUND: task.config[CURRENT_ROUND] + i,
                    EVALUATE: True,
                    TIMEOUT: task.config[TIMEOUT],
                    PLUGIN: task.config[PLUGIN],
                }))
        return tasks

    def assign_tasks(self, tid: int) -> Report:
        meta_task = self.get_meta_task(tid)

        while (len(meta_task.configured_tasks) > 0):
            # pop the first task
            task = meta_task.configured_tasks.pop(0)
            # assign task to server
            parameters, report = self.assign_task(meta_task.parameters, task)
            # update global attribute
            meta_task.parameters = parameters
        
        end_time = timeit.default_timer()
        elapsed = end_time - meta_task.start_time
        log(INFO, "FL finished in %s", elapsed)
        return report
    
    def assign_task(
        self,
        parameters: Parameters,
        task: Task
    ) -> Tuple[Parameters, int, Report]:
        loader = DynamicLoader("daisyfl.daisy.plugin." + task.config[PLUGIN], "Server")
        server = loader.plugin(self.server)
        if task.config[EVALUATE]:
            # get evaluate Report
            if (task.config[NUM_ROUNDS] < 0):
                # local evaluation
                task.config[NUM_ROUNDS] = 1
                report: Report = server.evaluate_round_api(parameters, task)
                # update history
                self.history.add_loss_distributed(
                    server_round=report.config[CURRENT_ROUND], loss=report.config[LOSS]
                )
                self.history.add_metrics_distributed(
                    server_round=report.config[CURRENT_ROUND], metrics=report.config[METRICS]
                )
                return parameters, report
            # EvaluateIns from upper layer
            report: Report = server.evaluate_round_api(parameters, task)
            return parameters, report

        # fitting task
        parameters, report = server.fit_round_api(parameters, task)
        return parameters, report

    # TODO: random tid
    # TODO: if multi-threading, wait others
    def get_tid(self,) -> int:
        tids = [meta_task.tid for meta_task in self.meta_tasks]
        i = 0
        while(i in tids):
            i = i + 1
        return i

    # TODO: if multi-threading, wait others
    def append_meta_task(self, meta_task: MetaTask) -> None:
        self.meta_tasks.append(meta_task)
    
    # TODO: if multi-threading, wait others
    # DEBUG: tid not found
    def get_meta_task(self, tid: int) -> MetaTask:
        for i in range(len(self.meta_tasks)):
            if self.meta_tasks[i].tid == tid:
                return self.meta_tasks[i]
        return None
    
    # TODO: if multi-threading, wait others
    def pop_meta_task(self, tid: int) -> bool:
        for i in range(len(self.meta_tasks)):
            if self.meta_tasks[i].tid == tid:
                self.meta_tasks.pop(i)
                return True
        return False

    def get_parameters_api(self, tid: int) -> Parameters:
        meta_task = self.get_meta_task(tid)
        if hasattr(meta_task, "parameters"):
            return meta_task.parameters
        raise AttributeError

    def stop_zone_server_api(self,) -> None:
        with self._cnd_stop:
            self._cnd_stop.notify()