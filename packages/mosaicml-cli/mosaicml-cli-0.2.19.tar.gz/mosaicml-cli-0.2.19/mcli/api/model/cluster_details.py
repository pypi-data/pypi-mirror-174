""" MCLI Abstraction for Clusters and Utilization """
from __future__ import annotations

import functools
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from mcli.api.exceptions import MAPI_DESERIALIZATION_ERROR
from mcli.api.schema.generic_model import DeserializableModel
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.utils.utils_serializable_dataclass import SerializableDataclass

logger = logging.getLogger(__name__)


def check_response(response: Dict[str, Any], expected: Set[str]) -> None:
    missing = expected - set(response)
    if missing:
        raise MAPI_DESERIALIZATION_ERROR


@dataclass
class ClusterUtilizationByUser:
    """Utilization for a specific user on a cluster
    """

    id: str
    user: str
    num_runs: int
    gpus_used: int
    gpus_queued: int

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ClusterUtilizationByUser:
        check_response(response, {'id', 'userName', 'numRuns', 'gpusQueued'})
        return cls(
            id=response['id'],
            user=response['userName'],
            num_runs=response['numRuns'],
            gpus_used=response['gpusUsed'],
            gpus_queued=response['gpusQueued'],
        )


@dataclass
class ClusterUtilization:
    """Utilization on a cluster
    """

    gpus_total: int
    gpus_used: int
    gpus_queued: int
    gpus_available: int
    by_user: List[ClusterUtilizationByUser] = field(default_factory=list)

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ClusterUtilization:
        check_response(response, {'gpusTotal', 'gpusUsed', 'gpusQueued', 'gpusAvailable', 'byUser'})
        return cls(
            gpus_total=response['gpusTotal'],
            gpus_used=response['gpusUsed'],
            gpus_queued=response['gpusQueued'],
            gpus_available=response['gpusAvailable'],
            by_user=[ClusterUtilizationByUser.from_mapi_response(i) for i in response['byUser']],
        )


@dataclass
@functools.total_ordering
class ClusterInstance:
    """Instance of a cluster
    """

    gpu_type: GPUType
    gpu_nums: List[int] = field(default_factory=list)

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ClusterInstance:
        check_response(response, {'gpuType', 'gpuNums'})
        return cls(gpu_type=GPUType.from_string(response['gpuType']), gpu_nums=response['gpuNums'])

    def __lt__(self, other: ClusterInstance):
        return self.gpu_type < other.gpu_type


@dataclass
@functools.total_ordering
class ClusterDetails(SerializableDataclass, DeserializableModel):
    """Details of a cluster, including instances and utilization
    """

    name: str
    cluster_instances: List[ClusterInstance] = field(default_factory=list)
    utilization: Optional[ClusterUtilization] = None

    kubernetes_context: str = ''
    namespace: str = ''

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ClusterDetails:
        check_response(response, {'name'})
        utilization = None if 'utilization' not in response else ClusterUtilization.from_mapi_response(
            response['utilization'])
        return cls(
            name=response['name'],
            cluster_instances=[ClusterInstance.from_mapi_response(i) for i in response.get('allowedInstances', [])],
            utilization=utilization,
        )

    def __lt__(self, other: ClusterDetails):
        return self.name < other.name
