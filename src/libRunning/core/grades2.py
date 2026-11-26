import operator
from decimal import Decimal

from libRunning.model.grade import Grades, Grade
from libRunning.model.index_data import ItemDesc


def grades_for_one_value_list(values: list[int], item_desc: ItemDesc) -> Grades:
    value = values[0]
    grades = Grades()
    grades.add(Grade.create(grade=1, from_=value, to_=value + 1))
    grades.add(Grade.create(grade=2, from_=value + 1, to_=value + 2))
    grades.add(Grade.create(grade=3, from_=value + 2, to_=value + 3))
    grades.add(Grade.create(grade=4, from_=value + 3, to_=value + 4))
    grades.add(Grade.create(grade=5, from_=value + 4, to_=value + 5))
    grades.time_convertible = item_desc.time_convertible
    # grades.less_is_best = (aggregation.sort_definition == SortDefinition.LESS_IS_BEST)
    grades.sort_definition = item_desc.sort_definition
    return grades


def calculate_grades(sorted_section: list[tuple[str, int]], item_desc: ItemDesc) -> Grades:
    values = [section_value for date, section_value in sorted_section]
    if len(values) > 0 and values[0] != max(values) and values[0] != min(values):
        raise ValueError("Section values are not sorted.")

    if not values:
        return Grades()

    if len(values) == 1:
        return grades_for_one_value_list(values, item_desc)

    first: int = values[0]
    last: int = values[-1]
    reverse = first > last
    step: Decimal = Decimal(str(abs(first - last) / 5))
    op = operator.add if not reverse else operator.sub
    first_dec = Decimal(str(first))
    last_dec = Decimal(str(last))
    grades = Grades()

    grades.time_convertible = item_desc.time_convertible

    grade_1_to: Decimal = op(first_dec, step)
    not_decimal: bool = grade_1_to == int(grade_1_to)
    final_to_step: Decimal = Decimal("1") if not_decimal else Decimal("0.1")

    grades.add(Grade(1, from_=first_dec, to_=grade_1_to))
    grades.add(Grade(2, from_=op(first_dec, step), to_=op(first_dec, 2 * step)))
    grades.add(Grade(3, from_=op(first_dec, 2 * step), to_=op(first_dec, 3 * step)))
    grades.add(Grade(4, from_=op(first_dec, 3 * step), to_=op(first_dec, 4 * step)))
    grades.add(Grade(5, from_=op(first_dec, 4 * step), to_=op(last_dec, final_to_step)))

    grades.sort_definition = item_desc.sort_definition

    return grades
