from typing import Any

from libRunning.model.grade import Grades
from libRunning.model.sorting import SortResult


def compare_section_or_aggregation(sorted_values: list[tuple[str, int]], grades: Grades) -> dict[str, SortResult]:
    output: dict[str, SortResult] = {}
    if len(sorted_values) == 0:
        return output

    first = sorted_values[0][1]
    order: int = 1
    how_many: int = 1
    index: int = -1
    for date, value in sorted_values:
        index += 1
        if index == 0:
            pass
        elif sorted_values[index - 1][1] == value:
            how_many += 1
        else:
            order = order + how_many
            how_many = 1

        lost = abs(value - first)
        if grades.empty:
            raise ValueError("Grades cannot be empty")

        grade = grades.get_grade_match(value)
        if grade is None:
            raise ValueError(f"Value: {value} cannot have None grade. Grades: {grades}")

        output[date] = SortResult(order=order, lost=lost, grade=grade, time_convertible=grades.time_convertible,
                                  less_is_best=grades.less_is_best)

    return output


def update_section_or_aggregation_data(data: dict[str, Any], type_: str, key: str,
                                       sort_result: dict[str, SortResult]) -> dict[str, Any]:
    root = data["trainings"]
    for date, value in sort_result.items():
        sub_root = root[date][key][type_]
        sub_root["order"] = value.order
        sub_root["lost"] = value.lost
        sub_root["grade"] = value.grade
        sub_root["time_convertible"] = value.time_convertible
        sub_root["less_is_best"] = value.less_is_best
    return data
