from collections import OrderedDict
from decimal import Decimal

from libRunning.core.updater import update_grades, update_section_data
from libRunning.model.aggregation_desc import SortDefinition
from libRunning.model.printing import SectionModelV2


def test_update_grades() -> None:
    data = {"grades": {}}
    grades = {
        1: (Decimal(1), Decimal(2)),
        2: (Decimal(2), Decimal(3)),
        3: (Decimal(3), Decimal(4)),
        4: (Decimal(4), Decimal(5)),
        5: (Decimal(5), Decimal(6)),
    }

    new_data = update_grades(data, ["grades", "time", "sections", "1.km"], grades)
    assert new_data.get("grades") is not None
    assert new_data["grades"].get("time") is not None
    assert isinstance(new_data["grades"]["time"], dict)
    assert new_data["grades"]["time"].get("sections") is not None
    assert isinstance(new_data["grades"]["time"]["sections"], dict)
    assert new_data["grades"]["time"]["sections"].get("1.km") is not None
    assert isinstance(new_data["grades"]["time"]["sections"]["1.km"], dict)
    assert new_data["grades"]["time"]["sections"]["1.km"] == grades

def test_update_section_data() -> None:
    data = {"trainings":
                {
                    "2026-01-01": {
                        "time": {
                            "sections": {
                                "1.km": {"value": 100},
                            }
                        }
                    },
                    "2026-02-02": {
                        "time": {
                            "sections": {
                                "1.km": {"value": 200},
                            }
                        }
                    },
                    "2026-03-03": {
                        "time": {
                            "sections": {
                                "1.km": {"value": 300},
                            }
                        },
                    }
                }
    }
    dict_01_01 = {"grade": 1, "lost": 0, "order": 1, "time_convertible": True, "sort_def": SortDefinition.LESS_IS_BEST}
    dict_02_02 = {"grade": 2, "lost": 5, "order": 2, "time_convertible": True, "sort_def": SortDefinition.LESS_IS_BEST}
    dict_03_03 = {"grade": 3, "lost": 10, "order": 3, "time_convertible": True, "sort_def": SortDefinition.LESS_IS_BEST}
    values = {
        "2026-01-01": SectionModelV2.from_dict(dict_01_01),
        "2026-02-02": SectionModelV2.from_dict(dict_02_02),
        "2026-03-03": SectionModelV2.from_dict(dict_03_03),
    }
    new_data = update_section_data(data, ["time", "sections", "1.km"], values)
    assert list(new_data["trainings"].keys()) == ["2026-01-01", "2026-02-02", "2026-03-03"]
    # 2026-01-01
    new_values = new_data["trainings"]["2026-01-01"]["time"]["sections"]["1.km"]
    # original value should not be rewritten
    dict_01_01.update({"value": 100})
    assert new_values == dict_01_01
    # 2026-02-02
    new_values = new_data["trainings"]["2026-02-02"]["time"]["sections"]["1.km"]
    # original value should not be rewritten
    dict_02_02.update({"value": 200})
    assert new_values == dict_02_02
    # 2026-03-03
    new_values = new_data["trainings"]["2026-03-03"]["time"]["sections"]["1.km"]
    # original value should not be rewritten
    dict_03_03.update({"value": 300})
    assert new_values == dict_03_03