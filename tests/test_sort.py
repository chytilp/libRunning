from decimal import Decimal

from libRunning.core.auxiliary import get_sorted_section_or_aggregation_values
from libRunning.core.functions import sort_aggregations, sort_sections
from libRunning.core.grades import calculate_grades
from libRunning.core.sorting import compare_section_or_aggregation
from libRunning.model.aggregation_desc import AggregationDesc, SortDefinition
from libRunning.model.sorting import SortResult

data: dict = {
    "section_grades": {},
    "aggregation_grades": {},
    "trainings": {
        "2026-02-01": {
            "sections": {
                "1.km": {"value": 295}
            },
            "aggregations": {
                "1.round": {"value": 1440}
            }
        },
        "2026-02-02": {
            "sections": {
                "1.km": {"value": 330}
            },
            "aggregations": {
                "1.round": {"value": 1400}
            }
        },
        "2026-02-03": {
            "sections": {
                "1.km": {"value": 315}
            },
            "aggregations": {
                "1.round": {"value": 1390}
            }
        },
        "2026-02-04": {
            "sections": {
                "1.km": {"value": 307}
            },
            "aggregations": {
                "1.round": {"value": 1445}
            }
        },
        "2026-02-05": {
            "sections": {
                "1.km": {"value": 340}
            },
            "aggregations": {
                "1.round": {"value": 1435}
            }
        },
    }
}

data_2: dict = {
    "section_grades": {},
    "aggregation_grades": {},
    "trainings": {
        "2026-02-01": {
            "sections": {
                "1.km": {"value": 295}
            }
        },
        "2026-02-02": {
            "sections": {
                "1.km": {"value": 310}
            }
        },
        "2026-02-03": {
            "sections": {
                "1.km": {"value": 295}
            }
        },
        "2026-02-04": {
            "sections": {
                "1.km": {"value": 310}
            }
        },
        "2026-02-05": {
            "sections": {
                "1.km": {"value": 320}
            }
        },
    }
}

data_3: dict = {
    "section_grades": {},
    "aggregation_grades": {},
    "trainings": {
        "2026-02-01": {
            "aggregations": {
                "under5:30": {"value": 1}
            }
        },
        "2026-02-02": {
            "aggregations": {
                "under5:30": {"value": 2}
            }
        },
        "2026-02-03": {
            "aggregations": {
                "under5:30": {"value": 3}
            }
        },
        "2026-02-04": {
            "aggregations": {
                "under5:30": {"value": 4}
            }
        },
        "2026-02-05": {
            "aggregations": {
                "under5:30": {"value": 5}
            }
        },
    }
}


def assert_sort_result(result: SortResult, expected_order: int, expected_lost: int, expected_grade: int) -> None:
    assert result.order == expected_order
    assert result.lost == expected_lost
    assert result.grade == expected_grade


def test_only_sort_section_result() -> None:
    # order, lost, grade
    sorted_values = get_sorted_section_or_aggregation_values(data, "1.km", "sections")
    grades = calculate_grades(sorted_values)
    output: dict[str, SortResult] = compare_section_or_aggregation(sorted_values, grades)
    assert_sort_result(output["2026-02-01"], expected_order=1, expected_lost=0, expected_grade=1)
    assert_sort_result(output["2026-02-04"], expected_order=2, expected_lost=12, expected_grade=2)
    assert_sort_result(output["2026-02-03"], expected_order=3, expected_lost=20, expected_grade=3)
    assert_sort_result(output["2026-02-02"], expected_order=4, expected_lost=35, expected_grade=4)
    assert_sort_result(output["2026-02-05"], expected_order=5, expected_lost=45, expected_grade=5)


def test_only_sort_section_result_same_values() -> None:
    sorted_values = get_sorted_section_or_aggregation_values(data_2, "1.km", "sections")
    grades = calculate_grades(sorted_values)
    output: dict[str, SortResult] = compare_section_or_aggregation(sorted_values, grades)
    assert_sort_result(output["2026-02-01"], expected_order=1, expected_lost=0, expected_grade=1)
    assert_sort_result(output["2026-02-03"], expected_order=1, expected_lost=0, expected_grade=1)
    assert_sort_result(output["2026-02-02"], expected_order=3, expected_lost=15, expected_grade=4)
    assert_sort_result(output["2026-02-04"], expected_order=3, expected_lost=15, expected_grade=4)
    assert_sort_result(output["2026-02-05"], expected_order=5, expected_lost=25, expected_grade=5)


def test_sort_sections() -> None:
    result = sort_sections(data, ["1.km"])
    root = result["trainings"]
    assert root["2026-02-01"]["sections"]["1.km"] == {"value": 295, "order": 1, "lost": 0, "grade": 1, "time_convertible": True, "less_is_best": True}
    assert root["2026-02-04"]["sections"]["1.km"] == {"value": 307, "order": 2, "lost": 12, "grade": 2, "time_convertible": True, "less_is_best": True}
    assert root["2026-02-03"]["sections"]["1.km"] == {"value": 315, "order": 3, "lost": 20, "grade": 3, "time_convertible": True, "less_is_best": True}
    assert root["2026-02-02"]["sections"]["1.km"] == {"value": 330, "order": 4, "lost": 35, "grade": 4, "time_convertible": True, "less_is_best": True}
    assert root["2026-02-05"]["sections"]["1.km"] == {"value": 340, "order": 5, "lost": 45, "grade": 5, "time_convertible": True, "less_is_best": True}
    assert "1.km" in list(result["section_grades"].keys())
    assert result["section_grades"]["1.km"] == {1: (295, 304), 2: (304, 313), 3: (313, 322), 4: (322, 331), 5: (331, 341)}
    assert id(data) != id(result)


def test_sort_aggregations() -> None:
    result = sort_aggregations(data, [AggregationDesc(name="1.round", reducer="sum")])
    root = result["trainings"]
    assert root["2026-02-01"]["aggregations"]["1.round"] == {"value": 1440, "order": 4, "lost": 50, "grade": 5, "time_convertible": True, "less_is_best": True}
    assert root["2026-02-04"]["aggregations"]["1.round"] == {"value": 1445, "order": 5, "lost": 55, "grade": 5, "time_convertible": True, "less_is_best": True}
    assert root["2026-02-03"]["aggregations"]["1.round"] == {"value": 1390, "order": 1, "lost": 0, "grade": 1, "time_convertible": True, "less_is_best": True}
    assert root["2026-02-02"]["aggregations"]["1.round"] == {"value": 1400, "order": 2, "lost": 10, "grade": 1, "time_convertible": True, "less_is_best": True}
    assert root["2026-02-05"]["aggregations"]["1.round"] == {"value": 1435, "order": 3, "lost": 45, "grade": 5, "time_convertible": True, "less_is_best": True}
    assert "1.round" in list(result["aggregation_grades"].keys())
    assert result["aggregation_grades"]["1.round"] == {1: (1390, 1401, True), 2: (1401, 1412, True), 3: (1412, 1423, True),
                                                       4: (1423, 1434, True), 5: (1434, 1446, True)}
    assert id(data) != id(result)


def test_sort_aggregation_more_is_best() -> None:
    result = sort_aggregations(data_3, [AggregationDesc(name="under5:30", reducer="len", sort_definition=SortDefinition.MORE_IS_BEST, time_convertible=False)])
    root = result["trainings"]
    assert root["2026-02-01"]["aggregations"]["under5:30"] == {"value": 1, "order": 5, "lost": 4, "grade": 5, "time_convertible": False, "less_is_best": False}
    assert root["2026-02-02"]["aggregations"]["under5:30"] == {"value": 2, "order": 4, "lost": 3, "grade": 4, "time_convertible": False, "less_is_best": False}
    assert root["2026-02-03"]["aggregations"]["under5:30"] == {"value": 3, "order": 3, "lost": 2, "grade": 3, "time_convertible": False, "less_is_best": False}
    assert root["2026-02-04"]["aggregations"]["under5:30"] == {"value": 4, "order": 2, "lost": 1, "grade": 2, "time_convertible": False, "less_is_best": False}
    assert root["2026-02-05"]["aggregations"]["under5:30"] == {"value": 5, "order": 1, "lost": 0, "grade": 1, "time_convertible": False, "less_is_best": False}
    assert "under5:30" in list(result["aggregation_grades"].keys())
    assert result["aggregation_grades"]["under5:30"] == {1: (Decimal("5"), Decimal("4.2"), False), 2: (Decimal("4.2"), Decimal("3.4"), False),
                                                         3: (Decimal("3.4"), Decimal("2.6"), False), 4: (Decimal("2.6"), Decimal("1.8"), False),
                                                         5: (Decimal("1.8"), Decimal("0.9"), False)}
    assert id(data_3) != id(result)
