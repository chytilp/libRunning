from typing import Any

import pytest

from libRunning.core.auxiliary import get_sorted_section_or_aggregation_values
from libRunning.core.grades import (
    calculate_grades,
    calculate_section_grades,
    update_section_or_aggregation_grades,
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


def assert_data_grades(grades: Grades) -> None:
    assert len(grades.grades) == 5
    assert grades.grade_1().tuple == (300, 360)
    assert grades.grade_2().tuple == (360, 420)
    assert grades.grade_3().tuple == (420, 480)
    assert grades.grade_4().tuple == (480, 540)
    assert grades.grade_5().tuple == (540, 601)


def assert_grades_dict(grades: dict[int, tuple[int, int]]) -> None:
    assert len(grades) == 5
    assert grades[1] == (300, 360)
    assert grades[2] == (360, 420)
    assert grades[3] == (420, 480)
    assert grades[4] == (480, 540)
    assert grades[5] == (540, 601)


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
    assert grades.grade_1().tuple == (1390, 1401)
    assert grades.grade_2().tuple == (1401, 1412)
    assert grades.grade_3().tuple == (1412, 1423)
    assert grades.grade_4().tuple == (1423, 1434)
    assert grades.grade_5().tuple == (1434, 1446)


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
    new_data = update_section_or_aggregation_grades(data_, section, "section_grades", grades.get_dict())
    root = new_data["section_grades"][section]
    assert_grades_dict(root)
