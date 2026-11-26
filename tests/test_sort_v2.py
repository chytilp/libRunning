import pytest

from libRunning.core.functions3 import sort_section, get_sorted_values
from libRunning.core.data_reader import DataReader
from libRunning.model.aggregation_desc import SortDefinition
from libRunning.model.index_data import ItemDesc

data = {
        "trainings": {
            "2026-01-01": {
                "time": {
                    "sections": {
                        "1.km": {"value": 100}
                    }
                }
            },
            "2026-02-02": {
                "time": {
                    "sections": {
                        "1.km": {"value": 200}
                    }
                }
            },
            "2026-03-03": {
                "time": {
                    "sections": {
                        "1.km": {"value": 150}
                    }
                }
            },
            "2026-04-04": {
                "time": {
                    "sections": {
                        "1.km": {"value": 190}
                    }
                }
            },
        }
    }


def test_sort_section() -> None:
    section_desc = ItemDesc(
        name="1.km",
        path="time",
        sort_definition=SortDefinition.LESS_IS_BEST,
        time_convertible=True,
    )
    new_data = sort_section(data, section_desc)
    reader = DataReader(new_data)
    expected_01_01 = {"value": 100, "order": 1, "grade": 1, "lost": 0, "time_convertible": True,
                      "sort_def": SortDefinition.LESS_IS_BEST}
    assert reader.get_time_section_node("2026-01-01", "1.km") == expected_01_01

    expected_02_02 = {"value": 200, "order": 4, "grade": 5, "lost": 100, "time_convertible": True,
                      "sort_def": SortDefinition.LESS_IS_BEST}
    assert reader.get_time_section_node("2026-02-02", "1.km") == expected_02_02

    expected_03_03 = {"value": 150, "order": 2, "grade": 3, "lost": 50, "time_convertible": True,
                      "sort_def": SortDefinition.LESS_IS_BEST}
    assert reader.get_time_section_node("2026-03-03", "1.km") == expected_03_03

    expected_04_04 = {"value": 190, "order": 3, "grade": 5, "lost": 90, "time_convertible": True,
                      "sort_def": SortDefinition.LESS_IS_BEST}
    assert reader.get_time_section_node("2026-04-04", "1.km") == expected_04_04


@pytest.mark.parametrize(
    "section_desc, expected_ok, expected_data",
    (
        (
            ItemDesc(name="1.km", path="time", sort_definition=SortDefinition.LESS_IS_BEST, time_convertible=True),
            True,
            [("2026-01-01", 100), ("2026-03-03", 150), ("2026-04-04", 190), ("2026-02-02", 200)]
        ),
        (
            ItemDesc(name="1.km", path="time", sort_definition=SortDefinition.MORE_IS_BEST, time_convertible=True),
            True,
            [("2026-02-02", 200), ("2026-04-04", 190), ("2026-03-03", 150), ("2026-01-01", 100)]
        ),
        (
            ItemDesc(name="1.km", path="time", sort_definition=SortDefinition.DO_NOT_SORT, time_convertible=True),
            False,
            []
        ),
    )
)
def test_get_sorted_values(section_desc: ItemDesc, expected_ok: bool, expected_data: list[tuple[str, int]]) -> None:
    ok, sorted_data = get_sorted_values(data, "sections", section_desc)
    assert ok == expected_ok
    assert sorted_data == expected_data
