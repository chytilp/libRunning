from core.data_wrapper import DataWrapper
from libRunning.config import get_config
from libRunning.core.index import read_index_routes, read_index_v4
from libRunning.core.read import read_data
from libRunning import RouteModel, DashboardModel, GradeModel, SectionsModel, CompareModel, TrainingModel
from libRunning.core.data_module import data


def get_routes() -> list[RouteModel]:
    # z indexu
    config = get_config()
    routes = read_index_routes(config.get_index_file_path(), version=4)
    return routes


def get_route_paths(route: RouteModel) -> list[str]:
    # z indexu
    config = get_config()
    index = read_index_v4(config.get_index_file_path(), route=route)
    return index.paths


def get_dates(route: RouteModel) -> list[str]:
    # z indexu a dat (jen read)
    config = get_config()
    index = read_index_v4(config.get_index_file_path(), route=route)
    wrapper: DataWrapper = read_data(data, index.files)
    return wrapper.trainings()


def get_dashboard_sections(route: RouteModel, path: str) -> list[str]:
    # z indexu
    config = get_config()
    index = read_index_v4(config.get_index_file_path(), route=route)
    return index.get_path_props(path).dashboard_sections


def get_dashboard_aggregations(route: RouteModel, path: str) -> list[str]:
    # z indexu
    config = get_config()
    index = read_index_v4(config.get_index_file_path(), route=route)
    return index.get_path_props(path).dashboard_aggregations


def get_sections(route: RouteModel) -> dict[str, list[str]]:
    # z indexu, rozdelene po path
    config = get_config()
    index = read_index_v4(config.get_index_file_path(), route=route)
    output: dict[str, list[str]] = {}
    for path in index.paths:
        sessions = index.get_path_props(path).session_keys
        output[path] = sessions
    return output


def get_aggregations(route: RouteModel) -> dict[str, list[str]]:
    # spocitat agregace
    config = get_config()
    index = read_index_v4(config.get_index_file_path(), route=route)
    output: dict[str, list[str]] = {}
    for path in index.paths:
        aggregations = index.get_path_props(path).aggregation_keys
        output[path] = aggregations
    return output


def get_dashboard(route: RouteModel, path: str, sections: list[str] | None = None,
                  aggregations: list[str] | None = None) -> DashboardModel:
    return DashboardModel()


def get_aggregation_grade(route: RouteModel, path: str, aggregation: str) -> list[GradeModel]:
    return []


def get_section_grade(route: RouteModel, path: str, section: str) -> list[GradeModel]:
    return []


def get_section(route: RouteModel, section: str, mark_date: str) -> SectionsModel:
    return SectionsModel()


def get_aggregation(route: RouteModel, aggregation: str, mark_date: str) -> SectionsModel:
    return SectionsModel()


def get_compare(route: RouteModel, date_1: str, date_2: str) -> CompareModel:
    return CompareModel()


def get_date(route: RouteModel, date: str) -> TrainingModel:
    return TrainingModel()
