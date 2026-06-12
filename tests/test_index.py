from pathlib import Path

from libRunning.core.index import read_index, read_index_routes
from libRunning.model.aggregation_desc import AggregationDesc, Filter, SortDefinition
from libRunning.model.printing import RouteModel


def test_old_format() -> None:
    route = RouteModel(name="barr", description="barr")
    index_data = read_index(
        Path(__file__).parent / "data" / "indexOld.json", route, 1)
    assert index_data.files == ["./data/example_data_1.json"]
    assert index_data.sections == ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km", "9.km"]
    assert list(index_data.aggregations.keys()) == ["1.round", "2.round", "rounds", "first5", "first9", "1.2km", "2.2km", "3.2km",
                                         "4.2km", "1.3km", "2.3km", "3.3km", "intervals_3", "intervals_5"]
    assert index_data.aggregations["1.round"] == ["1.km", "2.km", "3.km", "4.km"]
    assert index_data.aggregations["2.round"] == ["5.km", "6.km", "7.km", "8.km"]
    assert index_data.aggregations["rounds"] == ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km"]
    assert index_data.dashboard_sections == ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km"]
    assert index_data.dashboard_aggregations == ["1.round", "2.round", "rounds"]


def assert_aggregation_desc(agg_desc: AggregationDesc, expected_inputs: list[str], expected_reducer: str,
                            expected_filters: list[Filter], expected_sort_def: SortDefinition,
                            expected_time_convertible: bool) -> None:
    assert agg_desc.inputs == expected_inputs
    assert agg_desc.reducer == expected_reducer
    assert agg_desc.filters == expected_filters
    assert agg_desc.sort_definition == expected_sort_def
    assert agg_desc.time_convertible == expected_time_convertible


def test_new_format() -> None:
    route = RouteModel(name="barr", description="barr")
    index_data = read_index(Path(__file__).parent / "data" / "indexNew.json", route, 2)
    assert index_data.files == ["./tests/data/example_data_1.json"]
    assert list(index_data.aggregations.keys()) == ["1.round", "under6", "woutFilters"]
    assert_aggregation_desc(index_data.aggregations["1.round"], ["1.km", "2.km", "3.km", "4.km"], "sum", [],
                            SortDefinition.LESS_IS_BEST, True)
    assert_aggregation_desc(index_data.aggregations["under6"],
                            ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km", "9.km", "10.km"], "len",
                            [Filter(operator="<", value=360)], SortDefinition.MORE_IS_BEST, False)
    assert_aggregation_desc(index_data.aggregations["woutFilters"],
                            ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km", "9.km", "10.km"], "max",
                            [], SortDefinition.LESS_IS_BEST, True)


def test_index_routes() -> None:
    path = Path(__file__).parent / "data" / "indexNew.json"
    routes = read_index_routes(path)
    assert len(routes) == 1
    assert routes[0] == RouteModel(name="barr", description="")
