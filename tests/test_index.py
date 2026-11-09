from pathlib import Path

from libRunning.core.index import read_index, read_index_routes, read_index_v4
from libRunning.model.aggregation_desc import AggregationDesc, Filter, SortDefinition
from libRunning.model.index_data import IndexDataV2, SectionProperties
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
    routes = read_index_routes(path, version=2)
    assert len(routes) == 1
    assert routes[0] == RouteModel(name="barr", description="")


def test_index_v3_routes() -> None:
    path = Path(__file__).parent / "data" / "indexV3.json"
    routes = read_index_routes(path, version=3)
    assert len(routes) == 1
    assert routes[0] == RouteModel(name="tich", description="Osada ticha")


def test_v3_index_format() -> None:
    route = RouteModel(name="tich", description="")
    path = Path(__file__).parent / "data" / "indexV3.json"
    index_data = read_index(path, route, 3)
    assert index_data.files == ["/home/pchytil/data/running/tich.json"]
    assert list(index_data.aggregations.keys()) == ["total", "ten", "first5", "last5", "down3", "down2",
                                                    "up3", "up2", "last3", "first3", "in-top5",
                                                    "less-than-10sec"]
    all_sections = ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km", "9.km", "10.km", "11.km"]
    assert index_data.version == 3
    assert index_data.dashboard_sections == all_sections
    assert index_data.dashboard_aggregations == ["down2", "up2", "ten"]
    total_agg = index_data.aggregations["total"]
    assert total_agg.inputs == all_sections
    assert total_agg.reducer == "sum"
    assert total_agg.sort_definition == SortDefinition.LESS_IS_BEST
    assert total_agg.time_convertible == True
    assert total_agg.compute_with_field == "value"
    assert total_agg.all_inputs_needed == True
    assert total_agg.path == "time"


def test_index_v4_routes() -> None:
    path = Path(__file__).parent / "data" / "indexV4.json"
    routes = read_index_routes(path, version=4)
    assert len(routes) == 1
    assert routes[0] == RouteModel(name="tich", description="Osada ticha")

def test_v4_index_format() -> None:
    route = RouteModel(name="tich", description="")
    file_path = Path(__file__).parent / "data" / "indexV4.json"
    index_data: IndexDataV2 = read_index_v4(file_path, route, 4)
    assert index_data.files == ["./tests/data/tich.json"]
    assert index_data.version == 4
    assert index_data.route == "tich"
    all_sections = ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km", "9.km", "10.km", "11.km"]
    # time path
    time_props = index_data.get_path_props("time")
    # -- sections
    assert list(time_props.sections.keys()) == all_sections
    assert time_props.sections["1.km"] == SectionProperties.from_dict({"sort_definition": "less_is_best", "time_convertible": True})
    # -- constants
    assert list(time_props.constants.keys()) == []
    # -- aggregations
    assert list(time_props.aggregations.keys()) == ["total", "ten"]
    total_agg = time_props.aggregations["total"]
    assert total_agg.inputs == all_sections
    assert total_agg.reducer == "sum"
    assert total_agg.sort_definition == SortDefinition.LESS_IS_BEST
    assert total_agg.time_convertible == True
    assert total_agg.compute_with_field == "value"
    assert total_agg.all_inputs_needed == True
    assert total_agg.path == "time"
    # -- dashboard sections
    assert time_props.dashboard_sections == all_sections
    # -- dashboard aggregations
    assert time_props.dashboard_aggregations == ["total", "ten"]
    # -- dashboard constants
    assert time_props.dashboard_constants == []
    # tf path
    tf_props = index_data.get_path_props("tf")
    # -- sections
    assert list(tf_props.sections.keys()) == all_sections
    assert tf_props.sections["1.km"] == SectionProperties.from_dict(
        {"sort_definition": "less_is_best", "time_convertible": False})
    # -- constants
    assert list(tf_props.constants.keys()) == ["constants/tf_max", "constants/tf_avg"]
    # -- aggregations
    assert list(tf_props.aggregations.keys()) == []
    # -- dashboard sections
    assert tf_props.dashboard_sections == all_sections
    # -- dashboard aggregations
    assert tf_props.dashboard_aggregations == []
    # -- dashboard constants
    assert tf_props.dashboard_constants == ["constants/tf_max", "constants/tf_avg"]
