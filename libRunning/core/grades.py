import math
from typing import Any

from libRunning.model.aggregation_desc import AggregationDesc
from libRunning.model.grade import Grade, Grades


def calculate_grades(sorted_data: list[tuple[str, int]], aggregation: AggregationDesc | None = None) -> Grades:
    return calculate_section_grades(sorted_data, aggregation)


def calculate_section_grades(sorted_section: list[tuple[str, int]], aggregation: AggregationDesc | None = None) -> Grades:
    values = [section_value for date, section_value in sorted_section]
    if len(values) > 0 and values[0] != max(values) and values[0] != min(values):
        raise ValueError("Section values are not sorted.")

    if not values:
        return Grades()

    first: int = values[0]
    last: int = values[-1]
    reverse = first > last
    range_ = last - first
    step: int = int(math.floor(range_ / 5.0))
    grades = Grades()
    if aggregation is not None:
        grades.time_convertible = aggregation.time_convertible

    grades.add(Grade(grade=1, from_=first, to_=first + step))
    grades.add(Grade(grade=2, from_=first + step, to_=first + (2 * step)))
    grades.add(Grade(grade=3, from_=first + (2 * step), to_=first + (3 * step)))
    grades.add(Grade(grade=4, from_=first + (3 * step), to_=first + (4 * step)))
    grades.add(Grade(grade=5, from_=first + (4 * step), to_=last - 1 if reverse else last + 1))
    return grades


def update_section_or_aggregation_grades(data: dict[str, Any], type_: str, key: str, grades: dict[int, tuple[int, int]]) -> dict[str, Any]:
    # key = "section_grades" if not is_aggregation else "aggregation_grades"
    data[key][type_] = grades
    return data
