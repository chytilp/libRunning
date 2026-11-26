from typing import Any, cast

from libRunning.core.data_reader import DataReader
from libRunning.core.grades2 import calculate_grades
from libRunning.core.sorting import compare_section_or_aggregation_v2
from libRunning.core.updater import update_grades, update_section_data
from libRunning.model.aggregation_desc import SortDefinition
from libRunning.model.index_data import ItemDesc



def get_sorted_values(data: dict[str, Any], type_name: str, item_desc: ItemDesc) -> tuple[bool, list[tuple[str, int]]]:
    # name in format path/sections/{section} or path/aggregations/{aggregation}
    # use value field !!!
    if item_desc.sort_definition == SortDefinition.DO_NOT_SORT:
        return False, []

    name: list[str] = [item_desc.path, type_name, item_desc.name]
    section_times: dict[str, int] = {}
    reverse: bool = item_desc.sort_definition == SortDefinition.MORE_IS_BEST
    for training_key, training_value in data["trainings"].items():
        tmp = training_value
        for name_part in name:
            tmp = tmp[name_part]
        assert isinstance(tmp, dict)
        assert isinstance(training_key, str)
        section_times[training_key] = tmp["value"]
    return True, sorted(section_times.items(), key=lambda kv: kv[1], reverse=reverse)


def sort_section(data: dict[str, Any], section_desc: ItemDesc) -> dict[str, Any]:
    was_sorted, sorted_section_values = get_sorted_values(data, "sections", section_desc)
    if was_sorted:
        grades = calculate_grades(sorted_section_values, section_desc)
        new_data = update_grades(data, ["grades", section_desc.path, "sections", section_desc.name], grades.get_section_dict())
        sort_result = compare_section_or_aggregation_v2(sorted_section_values, grades, section_desc.name)
        new_data = update_section_data(new_data, [section_desc.path, "sections", section_desc.name], sort_result)
    else:
        new_data = data
    return new_data