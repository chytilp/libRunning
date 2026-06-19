from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RouteModel:
    name: str
    description: str = ""

    def __hash__(self) -> int:
        return hash(f"{self.name},{self.description}")

    def __eq__(self, other: RouteModel) -> bool:
        return hash(self) == hash(other)


@dataclass
class TrainingsModel:
    dates: list[str] = field(default_factory=list)


@dataclass
class SectionModel:
    name: str
    value: int
    order: int
    grade: int
    lost: int
    time_convertible: bool

    @staticmethod
    def from_dict(name: str, data: dict[str, Any]) -> SectionModel:
        return SectionModel(
            name=name,
            **data
        )


@dataclass
class TrainingModel:
    date: str
    note: str | None
    sections: list[SectionModel]
    aggregations: list[SectionModel]


@dataclass
class SectionsModel:
    # various dates(trainings) , same section
    date_sections: dict[str, SectionModel]
    mark_date: str | None


@dataclass
class GradeModel:
    grade: int
    from_: int
    to_: int
    time_convertible: bool


@dataclass
class CellIdentModel:
    date: str
    section: str
    is_section: bool = False

    def __hash__(self) -> int:
        return hash(self.date + "," + self.section)

    def __eq__(self, other: Any) -> bool:
        return hash(self) == hash(other)

    def __lt__(self, other: Any) -> bool:
        return f"{self.date},{self.is_section!s},{self.section}" <= f"{other.date},{other.is_section!s},{other.section}"


@dataclass
class DashboardModel:
    data: dict[CellIdentModel, SectionModel] = field(default_factory=dict)
    sections: list[str] = field(default_factory=list)
    aggregations: list[str] = field(default_factory=list)

    def get_dates(self) -> list[str]:
        dates: set[str] = set()
        for ident in self.data.keys():
            dates.add(ident.date)
        return sorted(list(dates), reverse=True)

    def exists_key(self, date: str, section: str) -> bool:
        ident = CellIdentModel(date=date, section=section)
        return ident in self.data.keys()

    def get_data(self, date: str, section: str) -> SectionModel | None:
        ident = CellIdentModel(date=date, section=section)
        return self.data.get(ident)


@dataclass
class CompareModel:
    data_1: TrainingModel
    data_2: TrainingModel

    def _find_in_list(self, name: str, arr: list[SectionModel]) -> SectionModel | None:
        for section in arr:
            if section.name == name:
                return section
        return None

    def get_sections(self, section_name: str) -> tuple[SectionModel | None, SectionModel | None]:
        first: SectionModel | None = self._find_in_list(section_name, self.data_1.sections)
        second: SectionModel | None = self._find_in_list(section_name, self.data_2.sections)
        return first, second

    def get_aggregations(self, aggregation_name: str) -> tuple[SectionModel | None, SectionModel | None]:
        first: SectionModel | None = self._find_in_list(aggregation_name, self.data_1.aggregations)
        second: SectionModel | None = self._find_in_list(aggregation_name, self.data_2.aggregations)
        return first, second
