from typing import Any

data: dict[str, Any] = {
    "section_grades": {},
    "aggregation_grades": {},
    "trainings": {},
}


def get(data_: dict[str, Any], path: list[Any]) -> Any:
    path_1 = path[0]
    if path_1 not in data.keys():
        raise ValueError(f"{path_1} not in data")
    node = data_[path_1]
    for sub_path in path[1:]:
        if sub_path == "*":
            index = path.index(sub_path)
            children = _get_all_children(node)
            output: dict[Any, Any] = {}
            for child in children:
                recursive, node_value = _get_from_node(node, [child] + path[index + 1:])
                if node_value is not None:
                    if not recursive:
                        output[child] = node_value
                    else:
                        for key, value in node_value.items():
                            output[child, key] = value
            return output
        elif sub_path not in node:
            raise ValueError(f"{path_1}/{sub_path} not in data")
        else:
            node = node[sub_path]
    return node


def _get_all_children(node: dict[str, Any]) -> list[str]:
    output: list[str] = []
    for item in node:
        output.append(item)
    return output


def _get_from_node(node: dict[str, Any], path: list[str]) -> tuple[bool, Any]:
    """In return tuple, first item is if it is recursive, second is value."""
    tmp_node = node
    for path_part in path:
        if path_part == "*":
            output: dict[str, Any] = {}
            index = path.index(path_part)
            children = _get_all_children(tmp_node)
            for child in children:
               recursive, node_value = _get_from_node(tmp_node, [child] + path[index + 1:])
               if node_value is not None:
                   output[child] = node_value
            return True, output
        elif path_part == "key" and isinstance(tmp_node, dict):
            return False, list(tmp_node.keys())
        elif path_part not in tmp_node:
            # raise ValueError(f"{path_part} not in data")
            return False, None
        tmp_node = tmp_node[path_part]
    return False, tmp_node


def filter_sections(data_: dict[str, Any], sections: list[str]) -> dict[str, Any]:
    out_data: dict[str, Any] = {"sections": {}, "aggregations": data_["aggregations"]}
    for section, value in data_["sections"].items():
        if section in sections:
            out_data["sections"][section] = value
    return out_data


def filter_aggregations(data_: dict[str, Any], aggregations: list[str]) -> dict[str, Any]:
    out_data: dict[str, Any] = {"sections": data_["sections"], "aggregations": {}}
    for aggregation, value in data_["aggregations"].items():
        if aggregation in aggregations:
            out_data["aggregations"][aggregation] = value
    return out_data
