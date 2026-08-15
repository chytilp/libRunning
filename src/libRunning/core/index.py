import json
from pathlib import Path
from typing import Any

from libRunning.config import Config
from libRunning.model.aggregation_desc import AggregationDesc, Filter, SortDefinition
from libRunning.model.index_data import IndexData
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

        field: str = "value"
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
            agg = agg_template.copy(inputs, agg_name)
            aggregations[agg_name] = agg

    return IndexData(
        version=version,
        files=files,
        aggregations=aggregations,
        sections=sections,
        dashboard_sections=dashboard_sections,
        dashboard_aggregations=dashboard_aggregations,
    )


def read_index(index_file: Path, route: RouteModel, version: int) -> IndexData:
    if version >= 3:
        return read_index_v3(index_file, route, version)

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

            field: str = "value"
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
