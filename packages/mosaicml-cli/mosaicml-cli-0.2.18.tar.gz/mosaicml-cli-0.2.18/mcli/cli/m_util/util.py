""" mcli util helpers """

import logging
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, Dict, Generator, List, Optional

import yaml
from rich.style import Style
from rich.table import Table

from mcli.api.cluster import get_clusters
from mcli.api.exceptions import MAPIErrorMessages, MAPIException, cli_error_handler
from mcli.api.model.cluster_details import ClusterDetails
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.cli.m_util.kube_util import get_row_color

logger = logging.getLogger(__name__)


@dataclass
class UtilizationInfo(MCLIDisplayItem):
    name: str
    user: str
    num_runs: int
    gpus_used: int
    gpus_queued: int


class UtilizationDisplay(MCLIGetDisplay):
    """Display information about the node
    """

    @property
    def index_label(self) -> str:
        if self.num_clusters == 1:
            return "user"
        else:
            return "name"

    def __init__(self, clusters: List[ClusterDetails]):
        self.clusters = clusters
        self.num_clusters = len({i.name for i in clusters})

    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        for cluster in self.clusters:
            assert cluster.utilization
            for i, by_user in enumerate(cluster.utilization.by_user):
                cluster_name = cluster.name
                if self.num_clusters == 1:
                    # Exclude cluster name from table completely when there's only one cluster
                    cluster_name = ''
                elif i > 0:
                    # Skip cluster name if it was the same as the previous
                    cluster_name = ''

                yield UtilizationInfo(
                    cluster_name,
                    by_user.user,
                    by_user.num_runs,
                    by_user.gpus_used,
                    by_user.gpus_queued,
                )


@dataclass
class ClusterInfo(MCLIDisplayItem):
    name: str
    gpus_total: int
    gpus_used: int
    gpus_queued: int
    gpus_available: int


class ClusterDisplay(MCLIGetDisplay):
    """Display information about the node
    """

    def __init__(self, clusters: List[ClusterDetails]):
        self.clusters = sorted(clusters)
        self.num_clusters = len({i.name for i in clusters})

    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        for cluster in self.clusters:
            assert cluster.utilization
            yield ClusterInfo(
                cluster.name,
                cluster.utilization.gpus_total,
                cluster.utilization.gpus_used,
                cluster.utilization.gpus_queued,
                cluster.utilization.gpus_available,
            )

    def to_table(self, items: List[Dict[str, Any]]) -> Table:
        """Overrides MCLIGetDisplay.to_table to have custom node colors by row using rich style
        """

        def _to_str(obj: Any) -> str:
            return yaml.safe_dump(obj, default_flow_style=None).strip() if not isinstance(obj, str) else obj

        column_names = self.override_column_ordering or [key for key, val in items[0].items() if val and key != 'name']

        data_table = Table(box=None, pad_edge=False)
        data_table.add_column('NAME', justify='left', no_wrap=True)

        for column_name in column_names:
            data_table.add_column(column_name.upper())

        for item in items:
            row_args = {}
            data_row = tuple(_to_str(item[key]) for key in column_names)
            color = get_row_color(item)
            if color is not None:
                row_args["style"] = Style(color=color)
            data_table.add_row(item['name'], *data_row, **row_args)

        return data_table


@cli_error_handler('mcli util')
def get_util(clusters: Optional[List[str]] = None, hide_users: bool = False, **kwargs) -> int:
    del kwargs

    try:
        c = get_clusters(clusters=clusters, include_utilization=True)
    except MAPIException as e:
        if e.status == HTTPStatus.NOT_FOUND:
            e.message = MAPIErrorMessages.NOT_FOUND_CLUSTER.value
        raise e

    agg = ''
    if len({cluster.name for cluster in c}) > 1:
        agg = ' by Cluster'

    print(f'Available GPUs{agg}:')
    cluster_display = ClusterDisplay(c)
    cluster_display.print(OutputDisplay.TABLE)

    if not hide_users:
        print(f'\nGPUs{agg} by User:')
        display = UtilizationDisplay(c)
        display.print(OutputDisplay.TABLE)

    return 0
