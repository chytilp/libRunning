import os
from pathlib import Path

from libRunning.config import set_config_file
from libRunning.model.printing import (
    CellIdentModel,
    CompareModel,
    DashboardModel,
    GradeModel,
    RouteModel,
    SectionsModel,
    TrainingModel,
)
from libRunning.core.lib_funcs import (
    get_aggregation,
    get_aggregation_grades,
    get_compare,
    get_dashboard,
    get_date,
    get_dates,
    get_routes,
    get_section,
    get_section_grades,
)


def _prepare_config(config_rel_path: str) -> None:
    folder = os.path.dirname(os.path.realpath(__file__))
    new_config_file = str(Path(folder, config_rel_path))
    set_config_file(new_config_file)


def test_get_routes() -> None:
    _prepare_config("./data/config.toml")
    routes = get_routes()
    assert len(routes) == 1
    assert routes[0].name == "barr"


def test_get_dates() -> None:
    _prepare_config("data/config.toml")
    trainings = get_dates(RouteModel(name="barr", description=""))
    assert len(trainings.dates) == 3
    assert trainings.dates[0] == "2026-01-01"
    assert trainings.dates[1] == "2026-01-02"
    assert trainings.dates[2] == "2026-01-03"


def test_get_date() -> None:
    _prepare_config("data/config.toml")
    training: TrainingModel = get_date(RouteModel(name="barr", description=""), "2026-01-02")
    assert training.date == "2026-01-02"
    assert len(training.sections) == 10
    assert len(training.aggregations) == 3


def test_get_section() -> None:
    _prepare_config("data/config.toml")
    result: SectionsModel = get_section(RouteModel(name="barr", description=""), "1.km", mark_date="2026-01-02")
    assert result.mark_date == "2026-01-02"
    assert sorted(list(result.date_sections.keys())) == [
        "2026-01-01", "2026-01-02", "2026-01-03"
    ]


def test_get_aggregation() -> None:
    _prepare_config("data/config.toml")
    result: SectionsModel = get_aggregation(RouteModel(name="barr", description=""), "1.round", mark_date="2026-01-02")
    assert result.mark_date == "2026-01-02"
    assert sorted(list(result.date_sections.keys())) == [
        "2026-01-01", "2026-01-02", "2026-01-03"
    ]


def test_get_section_grades() -> None:
    _prepare_config("data/config.toml")
    result: list[GradeModel] = get_section_grades(RouteModel(name="barr", description=""), "1.km")
    assert len(result) == 5


def test_get_aggregation_grades() -> None:
    _prepare_config("data/config.toml")
    result: list[GradeModel] = get_aggregation_grades(RouteModel(name="barr", description=""), "1.round")
    assert len(result) == 5


def test_get_dashboard() -> None:
    _prepare_config("data/config.toml")
    result: DashboardModel = get_dashboard(RouteModel(name="barr", description=""), sections=["1.km", "2.km", "3.km", "4.km"],
                                           aggregations=["1.round"])
    assert result.sections == ["1.km", "2.km", "3.km", "4.km"]
    assert result.aggregations == ["1.round"]
    assert len(list(result.data.keys())) == 15
    assert sorted(list(result.data.keys())) == sorted([
        CellIdentModel("2026-01-01", "1.km", True),
        CellIdentModel("2026-01-01", "2.km", True),
        CellIdentModel("2026-01-01", "3.km", True),
        CellIdentModel("2026-01-01", "4.km", True),
        CellIdentModel("2026-01-01", "1.round", False),
        CellIdentModel("2026-01-02", "1.km", True),
        CellIdentModel("2026-01-02", "2.km", True),
        CellIdentModel("2026-01-02", "3.km", True),
        CellIdentModel("2026-01-02", "4.km", True),
        CellIdentModel("2026-01-02", "1.round", False),
        CellIdentModel("2026-01-03", "1.km", True),
        CellIdentModel("2026-01-03", "2.km", True),
        CellIdentModel("2026-01-03", "3.km", True),
        CellIdentModel("2026-01-03", "4.km", True),
        CellIdentModel("2026-01-03", "1.round", False),
    ])


def test_get_compare() -> None:
    _prepare_config("data/config.toml")
    result: CompareModel = get_compare(RouteModel(name="barr", description=""), date_1="2026-01-01", date_2="2026-01-02")
    assert len(result.data_1.sections) == len(result.data_2.sections) == 10
    assert len(result.data_1.aggregations) == len(result.data_2.aggregations) == 3
