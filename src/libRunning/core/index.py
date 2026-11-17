import json
from pathlib import Path
from typing import Any

from libRunning.config import Config
from libRunning.model.aggregation_desc import AggregationDesc, Filter, SortDefinition
from libRunning.model.index_data import IndexData, IndexDataV2, SectionProperties, PathProperties
from libRunning.model.printing import RouteModel


def read_index_routes(index_file: Path, version: int) -> list[RouteModel]:
    index_data = json.load(open(index_file))
    routes: list[RouteModel] = []
    if version < 3:
        root_routes = index_data
    else:
        root_routes = index_data["routes"]
    for key, value in root_routes.items():
        route = RouteModel(name=key, description=value["description"])
        routes.append(route)
    return routes


def _read_aggregation_templates(file_path: Path) -> dict[str, AggregationDesc]:
    templates: dict[str, AggregationDesc] = {}
    data = json.load(open(file_path))
    for agg_name, agg_desc in data.items():
        operations: dict = agg_desc["operations"]
        filters: list[dict] = operations.get("filters") or []
        filters_objs: list[Filter] = []
        for filter_ in filters:
            field: str = "value"
            if filter_.get("field") is not None:
                field = filter_["field"]

            filters_objs.append(Filter(
                operator=filter_["operator"],
                value=filter_["value"],
                field=field,
            ))
        sort_def: SortDefinition = SortDefinition.LESS_IS_BEST
        if agg_desc.get("sort_definition") is not None:
            sort_def = SortDefinition(agg_desc["sort_definition"])
        time_convertible: bool = True
        if agg_desc.get("time_convertible") is not None:
            time_convertible = agg_desc["time_convertible"]

        all_inputs_needed: bool = True
        if agg_desc.get("all_inputs_needed") is not None:
            all_inputs_needed = agg_desc["all_inputs_needed"]

        field = "value"
        if agg_desc.get("compute_with_field") is not None and agg_desc["compute_with_field"] != "value":
            field = agg_desc["compute_with_field"]

        agg_obj = AggregationDesc(
            name=agg_name,
            inputs=[],
            reducer=operations["reducer"],
            filters=filters_objs,
            sort_definition=sort_def,
            time_convertible=time_convertible,
            all_inputs_needed=all_inputs_needed,
            compute_with_field=field,
        )
        templates[agg_name] = agg_obj

    return templates


def _fix_asterisk(original_list: list[str], sections: list[str]) -> list[str]:
    if original_list == ["*"]:
        return sections
    return original_list


def read_index_v3(index_file: Path, route: RouteModel, version: int) -> IndexData:
    index_data = json.load(open(index_file))
    generic_aggs_path = index_data["generic_aggregations"]
    agg_templates = _read_aggregation_templates(Path(generic_aggs_path).resolve())
    # for template in agg_templates.values():
    #     print(f"template {template.name}")

    routes_root = index_data["routes"]

    files: list[str] = routes_root[route.name]["files"]
    sections: list[str] = routes_root[route.name]["sections"]
    dashboard_sections: list[str] = _fix_asterisk(routes_root[route.name]["dashboard_sections"], sections)
    dashboard_aggregations: list[str] = routes_root[route.name]["dashboard_aggregations"]
    aggregations: dict[str, AggregationDesc] = {}
    for agg_name, agg_values in routes_root[route.name]["aggregations"].items():
        if agg_values.get("basedOn") is not None:
            agg_template = agg_templates[agg_values["basedOn"]]
            inputs = _fix_asterisk(agg_values["inputs"], sections)
            agg = agg_template.copy(inputs, agg_name, "time")
            aggregations[agg_name] = agg

    return IndexData(
        version=version,
        files=files,
        aggregations=aggregations,
        sections=sections,
        dashboard_sections=dashboard_sections,
        dashboard_aggregations=dashboard_aggregations,
    )


def read_path_part_section_like(path: str, routes_root: dict[str, Any], route: str, aliases: dict[str, Any],
                                part_name: str) -> dict[str, SectionProperties]:
    sections: dict[str, SectionProperties] = {}
    if path in routes_root[route][part_name]:
        sections_dict: dict[str, Any] = routes_root[route][part_name][path]
        for key, value in sections_dict.items():
            if isinstance(value, str) and value.startswith("@"):
                sections_dict[key] = aliases[value]
            sections[key] = SectionProperties.from_dict(sections_dict[key])
    return sections

def read_path_part_list_like(path: str, routes_root: dict[str, Any], route: str, aliases: dict[str, Any], part_name: str
                             ) -> list[str]:
    if path in routes_root[route][part_name].keys():
        part_dict: dict[str, Any] = routes_root[route][part_name]
        value = part_dict[path]
        if isinstance(value, str) and value.startswith("@"):
            value = aliases[value]
        return value
    return []

def read_index_v4(index_file: Path, route: RouteModel) -> IndexDataV2:
    index_data = json.load(open(index_file))
    data_folder: str = index_data["data_folder"]
    generic_aggs_path: str = index_data["generic_aggregations"]
    aliases: dict[str, Any] = index_data["aliases"]

    agg_templates = _read_aggregation_templates(Path(data_folder + generic_aggs_path).resolve())
    # for template in agg_templates.values():
    #     print(f"template {template.name}")

    routes_root = index_data["routes"]
    # files
    files: list[str] = routes_root[route.name]["files"]
    files = [data_folder + file_ for file_ in files]
    # aliases
    route_aliases: dict[str, Any] = {}
    if "aliases" in routes_root[route.name]:
        route_aliases = routes_root[route.name]["aliases"]
    aliases.update(route_aliases)

    index = IndexDataV2(
        files=files,
        route=route.name,
    )
    # paths
    paths: list[str] = routes_root[route.name]["paths"]
    for path in paths:
        props = PathProperties(path=path)
        # sections
        props.sections = read_path_part_section_like(path, routes_root, route.name, aliases, "sections")
        # aggregations
        aggregations: dict[str, AggregationDesc] = {}
        for agg_name, agg_values in routes_root[route.name]["aggregations"].items():
            agg_template = agg_templates[agg_values["basedOn"]]
            inputs = agg_values["inputs"]
            if isinstance(inputs, str) and inputs.startswith("@"):
                inputs = aliases[inputs]
            agg_path = agg_values["path"]
            if agg_path.lower() == path.lower():
                agg = agg_template.copy(inputs, agg_name, path)
                aggregations[agg_name] = agg

        props.aggregations = aggregations
        # constants
        props.constants = read_path_part_section_like(path, routes_root, route.name, aliases, "constants")
        # dashboard sections
        props.dashboard_sections = read_path_part_list_like(path, routes_root, route.name, aliases,
                                                            "dashboard_sections")
        # dashboard aggregations
        props.dashboard_aggregations = read_path_part_list_like(path, routes_root, route.name, aliases,
                                                            "dashboard_aggregations")
        # dashboard constants
        props.dashboard_constants = read_path_part_list_like(path, routes_root, route.name, aliases,
                                                                "dashboard_constants")
        index.add_path_props(path, props)


    return index


def read_index(index_file: Path, route: RouteModel, version: int) -> IndexData:
    if version == 3:
        return read_index_v3(index_file, route, version)
    elif version == 4:
        return read_index_v4(index_file, route)

    index_data = json.load(open(index_file))
    if index_data.get(route.name) is None:
        raise ValueError(f"Unknown data type: {route.name}")

    files: list[str] = index_data[route.name]["files"]
    aggregations: dict[str, Any] = {}
    if version == 1:
        aggregations = index_data[route.name]["aggregations"]
    elif version == 2:
        aggregations = {}
        aggregation_desc: dict[str, Any] = index_data[route.name]["aggregations"]
        for aag_name, agg_desc in aggregation_desc.items():
            operations: dict = agg_desc["operations"]
            filters: list[dict] = operations.get("filters") or []
            filters_objs: list[Filter] = []
            for filter_ in filters:
                field: str = "value"
                if filter_.get("field") is not None:
                    field = filter_["field"]

                filters_objs.append(Filter(
                    operator=filter_["operator"],
                    value=filter_["value"],
                    field=field,
                ))
            sort_def: SortDefinition = SortDefinition.LESS_IS_BEST
            if agg_desc.get("sort_definition") is not None:
                sort_def = SortDefinition(agg_desc["sort_definition"])
            time_convertible: bool = True
            if agg_desc.get("time_convertible") is not None:
                time_convertible = agg_desc["time_convertible"]

            all_inputs_needed: bool = True
            if agg_desc.get("all_inputs_needed") is not None:
                all_inputs_needed = agg_desc["all_inputs_needed"]

            field = "value"
            if agg_desc.get("compute_with_field") is not None and agg_desc["compute_with_field"] != "value":
                field = agg_desc["compute_with_field"]

            agg_obj = AggregationDesc(
                name=aag_name,
                inputs=agg_desc["inputs"],
                reducer=operations["reducer"],
                filters=filters_objs,
                sort_definition=sort_def,
                time_convertible=time_convertible,
                all_inputs_needed=all_inputs_needed,
                compute_with_field=field,
            )
            aggregations[aag_name] = agg_obj
    else:
        raise Exception(f"Unknown version of aggregation description: {version}")

    sections: list[str] = index_data[route.name]["sections"]
    dashboard_sections: list[str] = index_data[route.name]["dashboard_sections"]
    dashboard_aggregations: list[str] = index_data[route.name]["dashboard_aggregations"]
    return IndexData(
        version=version,
        files=files,
        aggregations=aggregations,
        sections=sections,
        dashboard_sections=dashboard_sections,
        dashboard_aggregations=dashboard_aggregations,
    )


def read_index_file(config: Config, route_name: str, version: int = 1) -> IndexData:
    route: RouteModel = RouteModel(name=route_name, description="")
    return read_index(config.get_index_file_path(), route, version)
