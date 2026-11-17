from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Protocol

from libRunning.model.aggregation_desc import AggregationDesc, SortDefinition

@dataclass
class ItemDesc:
    name: str
    sort_definition: SortDefinition
    time_convertible: bool
    path: str

    @property
    def reverse(self) -> bool:
        return self.sort_definition == SortDefinition.MORE_IS_BEST


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

    def get_session_props(self, session: str) -> ItemDesc:
        session_props = self.sections[session]
        return ItemDesc(
            name=session,
            path=self.path,
            sort_definition=session_props.sort_definition,
            time_convertible=session_props.time_convertible,
        )

    def get_aggregation_props(self, aggregation: str) -> ItemDesc:
        agg = self.aggregations[aggregation]
        return ItemDesc(
            name=aggregation,
            sort_definition=agg.sort_definition,
            time_convertible=agg.time_convertible,
            path=agg.path,
        )

    @property
    def session_keys(self) -> list[str]:
        return list(self.sections.keys())

    @property
    def aggregation_keys(self) -> list[str]:
        return list(self.aggregations.keys())

@dataclass
class IndexDataV2:
    route: str
    files: list[str]
    # | path specific values
    # V
    path_properties: dict[str, PathProperties] = field(default_factory=dict)

    def add_path_props(self, path: str, properties: PathProperties) -> None:
        self.path_properties[path] = properties

    def get_path_props(self, path: str) -> PathProperties:
        return self.path_properties[path]

    @property
    def paths(self) -> list[str]:
        return list(self.path_properties.keys())
