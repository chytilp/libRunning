from copy import deepcopy
from typing import Any

from core.grades import calculate_grades
from libRunning.core.auxiliary import get_sorted_section_or_aggregation_values
from libRunning.core.data_wrapper import DataWrapper
from libRunning.core.read import read_data
from libRunning.model.aggregation_desc import AggregationDesc
from libRunning.model.index_data import IndexDataV2, ItemDesc, PathProperties


def calculate_aggregations(data: dict[str, Any], aggregation_types: dict[str, Any]) -> dict[str, Any]:
    new_data: dict[str, Any] = deepcopy(data)
    for aggregation in aggregation_types.keys():
        for training_key, training in new_data["trainings"].items():
            if "aggregations" not in training:
                training["aggregations"] = {}
            agg_fce = create_calculate_aggregation(aggregation_types)
            aggregation_value: dict[str, Any] | None = agg_fce(new_data, training_key, aggregation)
            if aggregation_value:
                training["aggregations"][aggregation] = aggregation_value
    return new_data


def sort_sections(data: DataWrapper, sections: list[ItemDesc]) -> dict[str, Any]:
    # new_data: dict[str, Any] = deepcopy(data)
    for section_desc in sections:
        new_data = sort_section(data, section_desc)
    return new_data


def sort_aggregations(data: dict[str, Any], aggregations: list[AggregationDesc]) -> dict[str, Any]:
    new_data: dict[str, Any] = deepcopy(data)
    for aggregation in aggregations:
        new_data = sort_aggregation(new_data, aggregation)
    return new_data


def sort_aggregation(data: dict[str, Any], aggregation: AggregationDesc) -> dict[str, Any]:
    sorted_agg_values = get_sorted_section_or_aggregation_values(data, aggregation.name, "aggregations",
                                                                 reverse=aggregation.reverse)
    grades = calculate_grades(sorted_agg_values, aggregation)
    new_data = update_aggregation_grades(data, aggregation.name, "aggregation_grades", grades.get_aggregation_dict())
    sort_result = compare_section_or_aggregation(sorted_agg_values, grades)
    new_data = update_section_or_aggregation_data(new_data, aggregation.name, "aggregations", sort_result)
    return new_data


def sort_section(data: DataWrapper, section: ItemDesc) -> dict[str, Any]:
    sorted_section_values = get_sorted_section_or_aggregation_values(data, section, "sections")
    grades = calculate_grades(sorted_section_values)
    new_data = update_section_grades(data, section, "section_grades", grades.get_section_dict())
    sort_result = compare_section_or_aggregation(sorted_section_values, grades)
    new_data = update_section_or_aggregation_data(new_data, section, "sections", sort_result)
    return new_data


# napred zkusit pro jednu path
def prepare_data(index_data: IndexDataV2, path: str, from_: str, to_: str) -> dict[str, Any]:
    data: dict[str, Any] = {"section_grades": {}, "aggregation_grades": {}, "trainings": {}}
    new_data = read_data(data, index_data.files, from_, to_)
    new_data = sort_sections(new_data, index_data.get_path_props(path).sections_props)
    new_data = calculate_aggregations(new_data, index_data.aggregations)
    new_data = sort_aggregations(new_data, list(index_data.aggregations.values()))
    return new_data