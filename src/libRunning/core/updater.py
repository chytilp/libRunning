from decimal import Decimal
from typing import Any

from libRunning.model.printing import SectionModelV2


def _add_missing_nodes(data: dict[str, Any], data_path: list[str]) -> dict[str, Any]:
    root = data.copy()
    tmp = root
    # add missing nodes
    for part_path in data_path:
        if part_path not in tmp:
            tmp[part_path] = {}
        tmp = tmp[part_path]
    return root


def _find_node(data: dict[str, Any], data_path: list[str]) -> dict[str, Any]:
    node = data.copy()
    for idx, part_path in enumerate(data_path):
        node = node[part_path]
    return node


def update_grades(data: dict[str, Any], data_path: list[str], grades: dict[int, tuple[Decimal, Decimal]]) -> dict[str, Any]:
    root = _add_missing_nodes(data, data_path)

    rest, last = data_path[:-1], data_path[-1]
    node = _find_node(root, rest)
    node[last] = grades
    return root


def update_section_data(data: dict[str, Any], data_path: list[str], values: dict[str, SectionModelV2]) -> dict[str, Any]:
    new_data = data.copy()
    for training in values:
        new_data = _add_missing_nodes(new_data, ["trainings", training] + data_path)


    for training, value in values.items():
        complete_path = ["trainings", training] + data_path
        rest, last = complete_path[:-1], complete_path[-1]
        node = _find_node(new_data, rest)
        dt = value.to_dict()
        if 'value' in dt:
            dt.pop("value")
        new_value = node[last]
        new_value.update(dt)
        node[last] = new_value
    return new_data
