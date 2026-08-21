from decimal import Decimal
from typing import Any

import pytest

from libRunning.core.auxiliary import get_sorted_section_or_aggregation_values
from libRunning.core.grades import (
    calculate_grades,
    calculate_section_grades,
    update_section_grades,
)
from libRunning.model.grade import Grades

data: list[tuple[str, int]] = [
    ("2026-02-01", 400),
    ("2026-02-02", 300),
    ("2026-02-03", 500),
    ("2026-02-04", 350),
    ("2026-02-05", 450),
    ("2026-02-06", 550),
    ("2026-02-07", 420),
    ("2026-02-08", 440),
    ("2026-02-09", 600),
    ("2026-02-10", 380),
]

data_2: list[tuple[str, int]] = [
    ("2026-02-01", 1440),
    ("2026-02-04", 1445),
    ("2026-02-03", 1390),
    ("2026-02-02", 1400),
    ("2026-02-05", 1435),
]

data_3: dict[str, Any] = {
    "section_grades": {},
    "trainings": {
        "2026-02-01": {
            "sections": {
                "1.km": {"value": 400},
            }
        },
        "2026-02-02": {
            "sections": {
                "1.km": {"value": 300},
            }
        },
        "2026-02-03": {
            "sections": {
                "1.km": {"value": 500},
            }
        },
        "2026-02-04": {
            "sections": {
                "1.km": {"value": 350},
            }
        },
        "2026-02-05": {
            "sections": {
                "1.km": {"value": 450},
            }
        },
        "2026-02-06": {
            "sections": {
                "1.km": {"value": 550},
            }
        },
        "2026-02-07": {
            "sections": {
                "1.km": {"value": 420},
            }
        },
        "2026-02-08": {
            "sections": {
                "1.km": {"value": 440},
            }
        },
        "2026-02-09": {
            "sections": {
                "1.km": {"value": 600},
            }
        },
        "2026-02-10": {
            "sections": {
                "1.km": {"value": 380},
            }
        }
    }
}

data_4_list: list[tuple[str, int]] = [
    ("2026-07-22", 6),
    ("2026-05-15", 5),
    ("2026-05-12", 5),
    ("2026-07-07", 4),
    ("2026-06-11", 4),
    ("2026-05-26", 4),
    ("2026-05-19", 4),
    ("2026-08-18", 3),
    ("2026-08-11", 3),
    ("2026-06-24", 3),
    ("2026-07-10", 2),
    ("2026-07-01", 2),
    ("2026-04-24", 2),
    ("2026-04-09", 2),
    ("2026-06-02", 1),
    ("2026-04-17", 1),
    ("2026-05-05", 0),
    ("2025-09-19", 0),
    ("2025-09-11", 0),
    ("2025-09-08", 0),
    ("2025-09-04", 0),
    ("2025-09-01", 0),
]


def assert_data_grades(grades: Grades) -> None:
    assert len(grades.grades) == 5
    assert grades.grade_1().tuple == (Decimal("300"), Decimal("360"))
    assert grades.grade_2().tuple == (Decimal("360"), Decimal("420"))
    assert grades.grade_3().tuple == (Decimal("420"), Decimal("480"))
    assert grades.grade_4().tuple == (Decimal("480"), Decimal("540"))
    assert grades.grade_5().tuple == (Decimal("540"), Decimal("601"))


def assert_grades_dict(grades: dict[int, tuple[Decimal, Decimal]]) -> None:
    assert len(grades) == 5
    assert grades[1] == (Decimal("300"), Decimal("360"))
    assert grades[2] == (Decimal("360"), Decimal("420"))
    assert grades[3] == (Decimal("420"), Decimal("480"))
    assert grades[4] == (Decimal("480"), Decimal("540"))
    assert grades[5] == (Decimal("540"), Decimal("601"))


def test_grades() -> None:
    data_sorted = sorted(data, key=lambda x: x[1])
    grades = calculate_section_grades(data_sorted)
    assert_data_grades(grades)


def test_grades_error_unsorted() -> None:
    with pytest.raises(ValueError):
        _ = calculate_section_grades(data)


def test_grades_other_set() -> None:
    data_sorted = sorted(data_2, key=lambda x: x[1])
    grades = calculate_section_grades(data_sorted)
    assert len(grades.grades) == 5
    assert grades.grade_1().tuple == (Decimal("1390"), Decimal("1401"))
    assert grades.grade_2().tuple == (Decimal("1401"), Decimal("1412"))
    assert grades.grade_3().tuple == (Decimal("1412"), Decimal("1423"))
    assert grades.grade_4().tuple == (Decimal("1423"), Decimal("1434"))
    assert grades.grade_5().tuple == (Decimal("1434"), Decimal("1446"))


def test_calculate_grade() -> None:
    data_sorted = sorted(data_2, key=lambda x: x[1])
    grades = calculate_section_grades(data_sorted)
    grade_26_02_01 = grades.get_grade_match(1440)
    assert grade_26_02_01 == 5
    grade_26_02_04 = grades.get_grade_match(1445)
    assert grade_26_02_04 == 5
    grade_26_02_03 = grades.get_grade_match(1390)
    assert grade_26_02_03 == 1
    grade_26_02_02 = grades.get_grade_match(1400)
    assert grade_26_02_02 == 1
    grade_26_02_05 = grades.get_grade_match(1435)
    assert grade_26_02_05 == 5


def test_calculate_grades_from_app_data() -> None:
    sorted_values = get_sorted_section_or_aggregation_values(data_3, "1.km", "sections")
    grades = calculate_grades(sorted_values)
    assert_data_grades(grades)


def test_calculate_grades_not_in_data() -> None:
    sorted_values = get_sorted_section_or_aggregation_values(data_3, "2.km", "sections")
    grades = calculate_grades(sorted_values)
    assert grades.empty is True


def test_calculate_section_and_update_data() -> None:
    data_: dict[str, Any] = data_3
    section = "1.km"
    sorted_values = get_sorted_section_or_aggregation_values(data_, section, "sections")
    grades = calculate_grades(sorted_values)
    new_data = update_section_grades(data_, section, "section_grades", grades.get_section_dict())
    root = new_data["section_grades"][section]
    assert_grades_dict(root)


def test_calculate_aggregation_grades_more_is_best() -> None:
    grades = calculate_grades(data_4_list)
    assert grades.grade_1().tuple == (Decimal("6"), Decimal("4.8"))
    assert grades.grade_2().tuple == (Decimal("4.8"), Decimal("3.6"))
    assert grades.grade_3().tuple == (Decimal("3.6"), Decimal("2.4"))
    assert grades.grade_4().tuple == (Decimal("2.4"), Decimal("1.2"))
    assert grades.grade_5().tuple == (Decimal("1.2"), Decimal("-0.1"))


def test_calculate_grades_with_one_value() -> None:
    grades = calculate_grades([("2026-08-18", 100)])
    assert grades.grade_1().tuple == (Decimal("100"), Decimal("101"))
    assert grades.grade_2().tuple == (Decimal("101"), Decimal("102"))
    assert grades.grade_3().tuple == (Decimal("102"), Decimal("103"))
    assert grades.grade_4().tuple == (Decimal("103"), Decimal("104"))
    assert grades.grade_5().tuple == (Decimal("104"), Decimal("105"))
