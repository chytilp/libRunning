from dataclasses import dataclass
from typing import Any

from libRunning.model.aggregation_desc import AggregationDesc, SortDefinition


@dataclass
class IndexData:
    version: int
    files: list[str]
    aggregations: dict[str, AggregationDesc]
    sections: list[str]
    dashboard_sections: list[str]
    dashboard_aggregations: list[str]


@dataclass
class SectionProperties:
    sort_definition: SortDefinition
    time_convertible: bool


@dataclass
class PathProperties:
    path: str
    # keys are section names
    sections: dict[str, SectionProperties]
    # keys are aggregation names
    aggregations: dict[str, AggregationDesc]
    constants: dict[str, SectionProperties]
    dashboard_sections: list[str]
    dashboard_aggregations: list[str]
    dashboard_constants: list[str]

@dataclass
class IndexDataV2:
    version: int
    route: str
    files: list[str]
    # | path specific values
    # V
    path_properties: dict[str, PathProperties]
