from typing import Any

from libRunning.config import get_config
from libRunning.core.data_module import get
from libRunning.core.functions import prepare_data
from libRunning.core.index import read_index, read_index_routes
from libRunning.model.printing import (
    CellIdentModel,
    CompareModel,
    DashboardModel,
    GradeModel,
    RouteModel,
    SectionModel,
    SectionsModel,
    TrainingModel,
    TrainingsModel,
)


def _prepare_data(route: RouteModel, from_: str, to_: str) -> dict[str, Any]:
    config = get_config()
    index_data = read_index(index_file=config.get_index_file_path(), route=route, version=2)
    return prepare_data(index_data=index_data, from_=from_, to_=to_)


def _merge(data_1: dict[tuple[str, str], dict[str, Any]], data_2: dict[tuple[str, str], dict[str, Any]]
           ) -> dict[tuple[str, str], dict[str, Any]]:
    output: dict[tuple[str, str], dict[str, Any]] = data_1
    for (key_1, key_2), value in data_2.items():
        output[key_1, key_2] = value
    return output


def get_routes() -> list[RouteModel]:
    config = get_config()
    routes = read_index_routes(config.get_index_file_path())
    return routes


def get_dates(route: RouteModel) -> TrainingsModel:
    data: dict[str, Any] = _prepare_data(route=route, from_="", to_="")
    dates: list[str] = [date for date in data["trainings"].keys()]
    return TrainingsModel(dates=dates)


def _get_training_data(data: dict[str, Any], date: str) -> TrainingModel:
    sections: list[SectionModel] = []
    for section, section_data in data["sections"].items():
        sections.append(SectionModel.from_dict(section, section_data))

    aggregations: list[SectionModel] = []
    for agg, agg_data in data["aggregations"].items():
        aggregations.append(SectionModel.from_dict(agg, agg_data))

    return TrainingModel(date=date, note=data.get("note"), sections=sections, aggregations=aggregations)


def get_date(route: RouteModel, date: str) -> TrainingModel:
    data: dict[str, Any] = _prepare_data(route=route, from_="", to_="")
    date_data = get(data, ["trainings", date])
    return _get_training_data(data=date_data, date=date)


def get_section(route: RouteModel, section: str, from_: str = "", to_: str = "", mark_date: str = "") -> SectionsModel:
    section = section.lower()
    data: dict[str, Any] = _prepare_data(route=route, from_=from_, to_=to_)
    data = get(data, ["trainings", "*", "sections", section])
    data = dict(sorted(data.items(), key=lambda item: item[1]["order"]))
    date_sections: dict[str, SectionModel] = {}
    for date, date_values in data.items():
        date_sections[date] = SectionModel.from_dict(section, date_values)

    return SectionsModel(date_sections=date_sections, mark_date=mark_date)


def get_aggregation(route: RouteModel, aggregation: str, from_: str = "", to_: str = "", mark_date: str = ""
                    ) -> SectionsModel:
    aggregation = aggregation.lower()
    data: dict[str, Any] = _prepare_data(route=route, from_=from_, to_=to_)
    data = get(data, ["trainings", "*", "aggregations", aggregation])
    data = dict(sorted(data.items(), key=lambda item: item[1]["order"]))
    date_aggregations: dict[str, SectionModel] = {}
    for date, date_values in data.items():
        date_aggregations[date] = SectionModel.from_dict(aggregation, date_values)

    return SectionsModel(date_sections=date_aggregations, mark_date=mark_date)


def _get_grades(data: dict[str, Any], key: str, section_name: str) -> list[GradeModel]:
    grades = get(data, [key, section_name])
    grades_list: list[GradeModel] = []
    for grade, grade_data in grades.items():
        grades_list.append(GradeModel(
            grade=grade,
            from_=grade_data[0],
            to_=grade_data[1],
            time_convertible=True,
        ))
    return grades_list


def get_section_grades(route: RouteModel, section_name: str, from_: str = "", to_: str = "") -> list[GradeModel]:
    section_name = section_name.lower()
    data: dict[str, Any] = _prepare_data(route=route, from_=from_, to_=to_)
    return _get_grades(data=data, key="section_grades", section_name=section_name)


def get_aggregation_grades(route: RouteModel, aggregation_name: str, from_: str = "", to_: str = "") -> list[GradeModel]:
    aggregation_name = aggregation_name.lower()
    data: dict[str, Any] = _prepare_data(route=route, from_=from_, to_=to_)
    return _get_grades(data=data, key="aggregation_grades", section_name=aggregation_name)


def get_dashboard(route: RouteModel, from_: str = "", to_: str = "", sections: list[str] | None = None,
                  aggregations: list[str] | None = None) -> DashboardModel:
    config = get_config()
    index_data = read_index(index_file=config.get_index_file_path(), route=route, version=2)
    if sections is None:
        sections = index_data.dashboard_sections
    if aggregations is None:
        aggregations = index_data.dashboard_aggregations
    data: dict[str, Any] = prepare_data(index_data=index_data, from_=from_, to_=to_)
    sections_data: dict[tuple[str, str], dict[str, Any]] = get(data, ["trainings", "*", "sections", "*"])
    aggregations_data = get(data, ["trainings", "*", "aggregations", "*"])
    all_sections: list[str] = [section for date, section in sections_data.keys()]
    all_aggregations: list[str] = [agg for date, agg in aggregations_data.keys()]

    def _is_section(section_name: str) -> bool:
        if section_name in all_sections:
            return True
        if section_name in all_aggregations:
            return False
        raise Exception(f"Invalid section name: {section_name}, It's not a section nor aggregation.")

    data_for_print: dict[tuple[str, str], dict[str, Any]] = _merge(sections_data, aggregations_data)
    output_data: dict[CellIdentModel, SectionModel] = {}
    for (date, section), value in data_for_print.items():
        if (_is_section(section) and section in sections) or (not _is_section(section) and section in aggregations):
            ident = CellIdentModel(date=date, section=section, is_section=_is_section(section))
            output_data[ident] = SectionModel.from_dict(section, value)
    return DashboardModel(data=output_data, sections=sections, aggregations=aggregations)


def get_compare(route: RouteModel, date_1: str, date_2: str) -> CompareModel:
    data: dict[str, Any] = _prepare_data(route=route, from_="", to_="")
    date1_data = get(data, ["trainings", date_1])
    date1_obj = _get_training_data(data=date1_data, date=date_1)
    date2_data = get(data, ["trainings", date_2])
    date2_obj = _get_training_data(data=date2_data, date=date_2)
    return CompareModel(
        data_1=date1_obj,
        data_2=date2_obj,
    )
