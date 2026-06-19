from pathlib import Path

from libRunning.core.functions import calculate_aggregations
from libRunning.core.index import read_index
from libRunning.model.aggregation_desc import AggregationDesc
from libRunning.model.printing import RouteModel

ROUND_1: str = "1.round"
ROUND_2: str = "2.round"
BOTH_ROUNDS: str = "rounds"
FIRST_5: str = "first5"
FIRST_9: str = "first9"
KM_DOUBLE_1: str = "1.2km"
KM_DOUBLE_2: str = "2.2km"
KM_DOUBLE_3: str = "3.2km"
KM_DOUBLE_4: str = "4.2km"
KM_DOUBLE_5: str = "5.2km"
KM_TRIAD_1: str = "1.3km"
KM_TRIAD_2: str = "2.3km"
KM_TRIAD_3: str = "3.3km"
INTERVALS_TOTAL: str = "intervals_5"
INTERVALS_FIRST_3: str = "intervals_3"


data = {
    "trainings": {
        "2026-02-02": {
            "sections": {
                "0.km": {"value": 484},
                "1.km": {"value": 324},
                "2.km": {"value": 392},
                "3.km": {"value": 350},
                "4.km": {"value": 405},
                "5.km": {"value": 348},
                "6.km": {"value": 362},
                "7.km": {"value": 332},
                "8.km": {"value": 382},
                "9.km": {"value": 385},
                "010.km": {"value": 486}
            },
            "note": "this is note"
        }
    }
}

data_2 = {
    "trainings": {
        "2026-02-02": {
            "sections": {
                "1.km": {"value": 306},
                "2.km": {"value": 383},
                "3.km": {"value": 330},
                "4.km": {"value": 388},
                "9.km": {"value": 414},
                "10.km": {"value": 351}
            },
            "note": "this is note",
            "intervals": {
                "values": [146, 177, 148, 175, 169],
                "type": 500,
            }
        }
    }
}

data_3 = {
    "trainings": {
        "2026-02-02": {
            "sections": {
                "1.km": {"value": 306},
                "2.km": {"value": 383},
                "3.km": {"value": 330},
                "4.km": {"value": 388},
                "9.km": {"value": 414},
                "10.km": {"value": 351}
            },
            "note": "this is note",
            "intervals": {
                "values": [146, 177, 148],
                "type": 500,
            }
        }
    }
}


def get_aggregations_def() -> dict[str, AggregationDesc]:
    route = RouteModel(name="barr", description="barr")
    index_data = read_index(Path(__file__).parent / "data" / "index.json", route, 2)
    return index_data.aggregations


def filter_aggregations(aggregations: dict[str, AggregationDesc], wanted: list[str]) -> dict[str, AggregationDesc]:
    output: dict[str, AggregationDesc] = {}
    for key, value in aggregations.items():
        if key in wanted:
            output[key] = value
    return output


def test_calculate_aggregations() -> None:
    aggregations = get_aggregations_def()
    new_data = calculate_aggregations(data, aggregations)
    root = new_data["trainings"]["2026-02-02"]["aggregations"]
    assert root[ROUND_1]["value"] == 1471
    assert root[ROUND_2]["value"] == 1424
    assert root[BOTH_ROUNDS]["value"] == 2895
    assert root[FIRST_5]["value"] == 1819
    assert root[FIRST_9]["value"] == 3280
    assert root[KM_DOUBLE_1]["value"] == 716
    assert root[KM_DOUBLE_2]["value"] == 755
    assert root[KM_DOUBLE_3]["value"] == 710
    assert root[KM_DOUBLE_4]["value"] == 714
    assert KM_DOUBLE_5 not in list(root.keys())
    assert root[KM_TRIAD_1]["value"] == 1066
    assert root[KM_TRIAD_2]["value"] == 1115
    assert root[KM_TRIAD_3]["value"] == 1099
    assert len(root.keys()) == 12
    assert id(data) != id(new_data)


def test_calculate_intervals_aggregations() -> None:
    aggregations_all = get_aggregations_def()
    aggregations = filter_aggregations(aggregations_all, [ROUND_1, ROUND_2, INTERVALS_TOTAL, INTERVALS_FIRST_3])
    new_data = calculate_aggregations(data_2, aggregations)
    root = new_data["trainings"]["2026-02-02"]["aggregations"]
    assert ROUND_2 not in list(root.keys())
    assert root[ROUND_1]["value"] == 1407
    assert root[INTERVALS_FIRST_3]["value"] == 471
    assert root[INTERVALS_TOTAL]["value"] == 815
    assert id(data_2) != id(new_data)


def test_calculate_intervals_aggregations_with_3_values() -> None:
    aggregations_all = get_aggregations_def()
    aggregations = filter_aggregations(aggregations_all, [ROUND_1, ROUND_2, INTERVALS_TOTAL, INTERVALS_FIRST_3])
    new_data = calculate_aggregations(data_3, aggregations)
    root = new_data["trainings"]["2026-02-02"]["aggregations"]
    assert ROUND_2 not in list(root.keys())
    assert INTERVALS_TOTAL not in list(root.keys())
    assert root[ROUND_1]["value"] == 1407
    assert root[INTERVALS_FIRST_3]["value"] == 471
    assert id(data_3) != id(new_data)
