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
"""Flower utilities shared between server and client."""


from .parameter import bytes_to_ndarray as bytes_to_ndarray
from .parameter import ndarray_to_bytes as ndarray_to_bytes
from .parameter import ndarrays_to_parameters as ndarrays_to_parameters
from .parameter import parameters_to_ndarrays as parameters_to_ndarrays
from .parameter import encode_ndarrays as encode_ndarrays
from .parameter import decode_ndarrays as decode_ndarrays
from .typing import Code as Code
from .typing import DisconnectRes as DisconnectRes
from .typing import EvaluateIns as EvaluateIns
from .typing import EvaluateRes as EvaluateRes
from .typing import FitIns as FitIns
from .typing import FitRes as FitRes
from .typing import GetParametersIns as GetParametersIns
from .typing import GetParametersRes as GetParametersRes
from .typing import GetPropertiesIns as GetPropertiesIns
from .typing import GetPropertiesRes as GetPropertiesRes
from .typing import Metrics as Metrics
from .typing import MetricsAggregationFn as MetricsAggregationFn
from .typing import NDArray as NDArray
from .typing import NDArrays as NDArrays
from .typing import Parameters as Parameters
from .typing import Properties as Properties
from .typing import ReconnectIns as ReconnectIns
from .typing import Scalar as Scalar
from .typing import Element as Element
from .typing import Status as Status
from .typing import Task as Task
from .typing import Report as Report
from .typing import  NUM_ROUNDS as NUM_ROUNDS
from .typing import CURRENT_ROUND as CURRENT_ROUND
from .typing import EVALUATE as EVALUATE
from .typing import TIMEOUT as TIMEOUT
from .typing import FIT_SAMPLES as FIT_SAMPLES
from .typing import EVALUATE_SAMPLES as EVALUATE_SAMPLES
from .typing import LOSS as LOSS
from .typing import METRICS as METRICS
from .typing import Type as Type
from .typing import MetaTask as MetaTask
from .typing import TID as TID
from .typing import PLUGIN as PLUGIN
from .typing import PIDS as PIDS

GRPC_MAX_MESSAGE_LENGTH: int = 536_870_912  # == 512 * 1024 * 1024

__all__ = [
    "PIDS",
    "NUM_ROUNDS",
    "CURRENT_ROUND",
    "EVALUATE",
    "TIMEOUT",
    "FIT_SAMPLES",
    "EVALUATE_SAMPLES",
    "LOSS",
    "METRICS",
    "Type",
    "MetaTask",
    "encode_ndarrays",
    "decode_ndarrays",
    "bytes_to_ndarray",
    "Code",
    "Element",
    "DisconnectRes",
    "EvaluateIns",
    "EvaluateRes",
    "FitIns",
    "FitRes",
    "GetParametersIns",
    "GetParametersRes",
    "GetPropertiesIns",
    "GetPropertiesRes",
    "GRPC_MAX_MESSAGE_LENGTH",
    "Metrics",
    "MetricsAggregationFn",
    "ndarray_to_bytes",
    "NDArray",
    "NDArrays",
    "ndarrays_to_parameters",
    "Parameters",
    "parameters_to_ndarrays",
    "Properties",
    "ReconnectIns",
    "Scalar",
    "Status",
    "Task",
    "Report",
    "TID",
    "PLUGIN",
]
