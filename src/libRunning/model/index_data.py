from __future__ import annotations
from dataclasses import dataclass, field
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

    @staticmethod
    def from_dict(data: dict[str, Any]) -> SectionProperties:
        return SectionProperties(
            sort_definition=SortDefinition(data["sort_definition"]),
            time_convertible=bool(data["time_convertible"])
        )


@dataclass
class PathProperties:
    path: str
    # keys are section names
    sections: dict[str, SectionProperties] = field(default_factory=dict)
    # keys are aggregation names
    aggregations: dict[str, AggregationDesc] = field(default_factory=dict)
    constants: dict[str, SectionProperties] = field(default_factory=dict)
    dashboard_sections: list[str] = field(default_factory=list)
    dashboard_aggregations: list[str] = field(default_factory=list)
    dashboard_constants: list[str] = field(default_factory=list)

@dataclass
class IndexDataV2:
    version: int
    route: str
    files: list[str]
    # | path specific values
    # V
    path_properties: dict[str, PathProperties] = field(default_factory=dict)

    def add_path_props(self, path: str, properties: PathProperties) -> None:
        self.path_properties[path] = properties

    def get_path_props(self, path: str) -> PathProperties:
        return self.path_properties[path]
