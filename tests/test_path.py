from typing import Any

import pytest

from libRunning.core.data_module import get

data: dict[str, Any] = {
    "section_grades": {
        '1.km': {1: (293, 307), 2: (307, 321), 3: (321, 335), 4: (335, 349), 5: (349, 364)},
        '2.km': {1: (367, 381), 2: (381, 395), 3: (395, 409), 4: (409, 423), 5: (423, 439)}
    },
    "aggregation_grades": {},
    "trainings": {
        "2026-01-01": {
            "sections": {
                "1.km": {"order": 1, "lost": 0, "grade": 1, "value": 300},
                "2.km": {"order": 2, "lost": 10, "grade": 2, "value": 310},
                "3.km": {"order": 3, "lost": 20, "grade": 3, "value": 320},
                "4.km": {"order": 4, "lost": 30, "grade": 4, "value": 330},
            },
            "aggregations": {
                "1.round": {"order": 1, "lost": 0, "grade": 1, "value": 1260},
            },
            "note": "something"
        },
        "2026-01-02": {
            "sections": {
                "1.km": {"order": 1, "lost": 0, "grade": 1, "value": 400},
                "2.km": {"order": 2, "lost": 10, "grade": 2, "value": 410},
                "3.km": {"order": 3, "lost": 20, "grade": 3, "value": 420},
                "4.km": {"order": 4, "lost": 30, "grade": 4, "value": 430},
            },
            "aggregations": {
                "1.round": {"order": 3, "lost": 400, "grade": 3, "value": 1660},
            },
            "note": "something else"
        },
        "2026-01-03": {
            "sections": {
                "1.km": {"order": 1, "lost": 0, "grade": 1, "value": 360},
                "2.km": {"order": 2, "lost": 10, "grade": 2, "value": 370},
                "3.km": {"order": 3, "lost": 20, "grade": 3, "value": 380},
                "4.km": {"order": 4, "lost": 30, "grade": 4, "value": 390},
            },
            "aggregations": {
                "1.round": {"order": 2, "lost": 240, "grade": 2, "value": 1500},
            },
            "note": "something else"
        }
    },
}


@pytest.mark.parametrize(
    "path, expected",
    (
        pytest.param(["trainings", "2026-01-01", "sections", "1.km"], {"order": 1, "lost": 0, "grade": 1, "value": 300}, id="1.km dict"),
        pytest.param(["trainings", "2026-01-01", "sections", "1.km", "value"], 300, id="1.km value"),
        pytest.param(["trainings", "*", "sections", "1.km"],
                     {
                         "2026-01-01": {"order": 1, "lost": 0, "grade": 1, "value": 300},
                         "2026-01-02": {"order": 1, "lost": 0, "grade": 1, "value": 400},
                         "2026-01-03": {"order": 1, "lost": 0, "grade": 1, "value": 360}
                     }, id="* as training, dict"),
        pytest.param(["trainings", "*", "sections", "1.km", "value"], {"2026-01-01": 300, "2026-01-02": 400, "2026-01-03": 360}, id="* as training, value"),
        pytest.param(["section_grades", "1.km"], {1: (293, 307), 2: (307, 321), 3: (321, 335), 4: (335, 349), 5: (349, 364)}, id="section grades 1.km, dict"),
        pytest.param(["section_grades", "1.km", 1], (293, 307), id="section grades 1.km grade 1"),
        pytest.param(["trainings", "*", "sections", "*"],
                     {
                         ("2026-01-01", "1.km"): {"grade": 1, "lost": 0, "order": 1, "value": 300},
                         ("2026-01-02", "1.km"): {"grade": 1, "lost": 0, "order": 1, "value": 400},
                         ("2026-01-03", "1.km"): {"grade": 1, "lost": 0, "order": 1, "value": 360},
                         ("2026-01-01", "2.km"): {"grade": 2, "lost": 10, "order": 2, "value": 310},
                         ("2026-01-02", "2.km"): {"grade": 2, "lost": 10, "order": 2, "value": 410},
                         ("2026-01-03", "2.km"): {"grade": 2, "lost": 10, "order": 2, "value": 370},
                         ("2026-01-01", "3.km"): {"grade": 3, "lost": 20, "order": 3, "value": 320},
                         ("2026-01-02", "3.km"): {"grade": 3, "lost": 20, "order": 3, "value": 420},
                         ("2026-01-03", "3.km"): {"grade": 3, "lost": 20, "order": 3, "value": 380},
                         ("2026-01-01", "4.km"): {"grade": 4, "lost": 30, "order": 4, "value": 330},
                         ("2026-01-02", "4.km"): {"grade": 4, "lost": 30, "order": 4, "value": 430},
                         ("2026-01-03", "4.km"): {"grade": 4, "lost": 30, "order": 4, "value": 390},
                     }, id="* as trainings, * as sections, dict"),
        pytest.param(["trainings", "*", "sections", "*", "value"],
                     {
                         ("2026-01-01", "1.km"): 300,
                         ("2026-01-02", "1.km"): 400,
                         ("2026-01-03", "1.km"): 360,
                         ("2026-01-01", "2.km"): 310,
                         ("2026-01-02", "2.km"): 410,
                         ("2026-01-03", "2.km"): 370,
                         ("2026-01-01", "3.km"): 320,
                         ("2026-01-02", "3.km"): 420,
                         ("2026-01-03", "3.km"): 380,
                         ("2026-01-01", "4.km"): 330,
                         ("2026-01-02", "4.km"): 430,
                         ("2026-01-03", "4.km"): 390,
                     }, id="* as trainings, * as sections, value"),
        pytest.param(["trainings", "*", "sections", "key"],
                     {
                        "2026-01-01": ["1.km", "2.km", "3.km", "4.km"],
                        "2026-01-02": ["1.km", "2.km", "3.km", "4.km"],
                        "2026-01-03": ["1.km", "2.km", "3.km", "4.km"],
                     }, id="* as trainings, sections, keys"),
    ),
)
def test_paths(path: list[str], expected: Any) -> None:
    output = get(data, path)
    assert output == expected
