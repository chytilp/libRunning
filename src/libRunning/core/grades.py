import math
from decimal import Decimal
import operator
from typing import Any

from libRunning.model.aggregation_desc import AggregationDesc, SortDefinition
from libRunning.model.grade import Grade, Grades


def calculate_grades(sorted_data: list[tuple[str, int]], aggregation: AggregationDesc | None = None) -> Grades:
    return calculate_section_grades(sorted_data, aggregation)

def grades_for_one_value_list(values: list[int], aggregation: AggregationDesc | None = None) -> Grades:
    value = values[0]
    grades = Grades()
    grades.add(Grade.create(grade=1, from_=value, to_=value + 1))
    grades.add(Grade.create(grade=2, from_=value + 1, to_=value + 2))
    grades.add(Grade.create(grade=3, from_=value + 2, to_=value + 3))
    grades.add(Grade.create(grade=4, from_=value + 3, to_=value + 4))
    grades.add(Grade.create(grade=5, from_=value + 4, to_=value + 5))
    if aggregation is not None:
        grades.time_convertible = aggregation.time_convertible
    if aggregation is not None:
        grades.less_is_best = (aggregation.sort_definition == SortDefinition.LESS_IS_BEST)
    return grades

def calculate_section_grades(sorted_section: list[tuple[str, int]], aggregation: AggregationDesc | None = None) -> Grades:
    values = [section_value for date, section_value in sorted_section]
    if len(values) > 0 and values[0] != max(values) and values[0] != min(values):
        raise ValueError("Section values are not sorted.")

    if not values:
        return Grades()

    if len(values) == 1:
        return grades_for_one_value_list(values, aggregation)

    first: int = values[0]
    last: int = values[-1]
    reverse = first > last
    step: Decimal = Decimal(str(abs(first - last) / 5))
    op = operator.add if not reverse else operator.sub
    first_dec = Decimal(str(first))
    last_dec = Decimal(str(last))
    grades = Grades()

    if aggregation is not None:
        grades.time_convertible = aggregation.time_convertible

    grade_1_to: Decimal = op(first_dec, step)
    not_decimal: bool = grade_1_to == int(grade_1_to)
    final_to_step: Decimal = Decimal("1") if not_decimal else Decimal("0.1")

    grades.add(Grade(1, from_=first_dec, to_=grade_1_to))
    grades.add(Grade(2, from_=op(first_dec, step), to_=op(first_dec, 2 * step)))
    grades.add(Grade(3, from_=op(first_dec, 2 * step), to_=op(first_dec, 3 * step)))
    grades.add(Grade(4, from_=op(first_dec, 3 * step), to_=op(first_dec, 4 * step)))
    grades.add(Grade(5, from_=op(first_dec, 4 * step), to_=op(last_dec, final_to_step)))

    if aggregation is not None:
        grades.less_is_best = (aggregation.sort_definition == SortDefinition.LESS_IS_BEST)

    return grades


def update_section_grades(data: dict[str, Any], type_: str, key: str, grades: dict[int, tuple[Decimal, Decimal]]
                                         ) -> dict[str, Any]:
    # key = "section_grades" if not is_aggregation else "aggregation_grades"
    data[key][type_] = grades
    return data


def update_aggregation_grades(data: dict[str, Any], type_: str, key: str, grades: dict[int, tuple[Decimal, Decimal, bool]]
                                         ) -> dict[str, Any]:
    # key = "section_grades" if not is_aggregation else "aggregation_grades"
    data[key][type_] = grades
    return data
