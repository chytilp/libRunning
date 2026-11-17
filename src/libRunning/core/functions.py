
from copy import deepcopy
from typing import Any

from libRunning.core.read import read, filter_
from libRunning.core.aggregation_functions import create_calculate_aggregation
from libRunning.core.auxiliary import (
    get_sorted_section_or_aggregation_values,
)
from libRunning.core.data_module import data
from libRunning.core.grades import (
    calculate_grades,
    update_aggregation_grades,
    update_section_grades,
)
from libRunning.core.sorting import (
    compare_section_or_aggregation,
    update_section_or_aggregation_data,
)
from libRunning.model.aggregation_desc import AggregationDesc
from libRunning.model.index_data import IndexData


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


def sort_sections(data: dict[str, Any], sections: list[str]) -> dict[str, Any]:
    new_data: dict[str, Any] = deepcopy(data)
    for section in sections:
        new_data = sort_section(new_data, section)
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


def sort_section(data: dict[str, Any], section: str) -> dict[str, Any]:
    sorted_section_values = get_sorted_section_or_aggregation_values(data, section, "sections")
    grades = calculate_grades(sorted_section_values)
    new_data = update_section_grades(data, section, "section_grades", grades.get_section_dict())
    sort_result = compare_section_or_aggregation(sorted_section_values, grades)
    new_data = update_section_or_aggregation_data(new_data, section, "sections", sort_result)
    return new_data


def prepare_data(index_data: IndexData, from_: str, to_: str) -> dict[str, Any]:
    new_data = read(data, index_data.files)
    new_data = filter_(new_data, from_=from_, to_=to_)
    new_data = sort_sections(new_data, index_data.sections)
    new_data = calculate_aggregations(new_data, index_data.aggregations)
    new_data = sort_aggregations(new_data, list(index_data.aggregations.values()))
    return new_data
