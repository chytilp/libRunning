from collections import defaultdict
from typing import Any, cast, Protocol


class GetItemsFunc(Protocol):

    def __call__(self, path: str) -> list[str]:
        ...


class TrainingWrapper:

    def __init__(self, root: dict[str, Any], training: str) -> None:
        self.root: dict[str, Any] = root
        self.training: str = training

    @property
    def date(self) -> str:
        return self.training

    def has_path(self, path: str) -> bool:
        return path in self.root

    def paths(self) -> list[str]:
        keys = list(self.root.keys())
        paths = set(keys) - {"note", "constants"}
        return sorted(list(paths))

    def sections(self, path: str) -> list[str]:
        sections_node = self.root[path]["sections"]
        sections_node = cast(dict[str, Any], sections_node)
        return list(sections_node.keys())

    def section_obj(self, path: str, section: str) -> dict[str, Any] | None:
        root = self.root[path]["sections"]
        root = cast(dict[str, Any], root)
        if section not in root:
            return None
        obj = root[section]
        obj = cast(dict[str, Any], obj)
        return obj

    def aggregations(self, path: str) -> list[str]:
        aggregations_node = self.root[path]["aggregations"]
        aggregations_node = cast(dict[str, Any], aggregations_node)
        return list(aggregations_node.keys())

    def aggregation_obj(self, path: str, aggregation: str) -> dict[str, Any] | None:
        root = self.root[path]["aggregations"]
        root = cast(dict[str, Any], root)
        if aggregation not in root:
            return None
        obj = root[aggregation]
        obj = cast(dict[str, Any], obj)
        return obj

    def constants(self) -> list[str]:
        root = self.root["constants"]
        root = cast(dict[str, Any], root)
        return list(root.keys())

    def constant_obj(self) -> dict[str, Any]:
        root = self.root["constants"]
        root = cast(dict[str, Any], root)
        return root

    def note(self) -> str | None:
        return self.root.get("note")



class DataWrapper:
    def __init__(self, data=dict[str, Any]) -> None:
        self.data = data

    def trainings(self) -> list[str]:
        root = self.data["trainings"]
        root = cast(dict[str, Any], root)
        return list(root.keys())

    def get_training(self, date: str) -> TrainingWrapper | None:
        root: Any | None = self.data["trainings"].get(date)
        if root is None:
            return None
        root = cast(dict[str, Any], root)
        return TrainingWrapper(root, date)

    def _items(self, func: GetItemsFunc) -> dict[str, list[str]]:
        tmp: dict[str, set[str]] = defaultdict(set)
        for training in self.trainings():
            training_obj = self.get_training(training)
            for path in training_obj.paths():
                if path not in tmp:
                    tmp[path] = set()
                items = func(path)
                for item in items:
                    tmp[path].add(item)
        output: dict[str, list[str]] = defaultdict(list)
        for k, v in tmp.items():
            output[k] = sorted(list(v))
        return output

    def sections(self) -> dict[str, list[str]]:
        tmp: dict[str, set[str]] = defaultdict(set)
        for training in self.trainings():
            training_obj = self.get_training(training)
            for path in training_obj.paths():
                if path not in tmp:
                    tmp[path] = set()
                sections = training_obj.sections(path)
                for section in sections:
                    tmp[path].add(section)
        output: dict[str, list[str]] = defaultdict(list)
        for k, v in tmp.items():
            output[k] = sorted(list(v))
        return output

    def section_is_in(self, section: str) -> dict[str, list[str]]:
        # v kterych dates rozdelene po paths
        # tj path1: list[date1, date2...]
        #    path2: list[date1,...]
        return {}

    def aggregation_is_in(self, aggregation: str) -> dict[str, list[str]]:
        # v kterych dates rozdelene po paths
        # tj path1: list[date1, date2...]
        #    path2: list[date1,...]
        return {}

    # def has_path(self, training: str, path: str) -> bool:
    #     root = self.data["trainings"][training]
    #     root = cast(dict[str, Any], root)
    #     return path in root
    #
    # def path_sections(self, training: str, path: str) -> list[str]:
    #     root = self.data["trainings"][training]
    #     root = cast(dict[str, Any], root)
    #     sections_node = root[path]["sections"]
    #     sections_node = cast(dict[str, Any], sections_node)
    #     return list(sections_node.keys())
    #
    # def section_obj(self, training: str, path: str, section: str) -> dict[str, Any] | None:
    #     root = self.data["trainings"][training][path]["sections"]
    #     root = cast(dict[str, Any], root)
    #     if section not in root:
    #         return None
    #     obj = root[section]
    #     obj = cast(dict[str, Any], obj)
    #     return obj
    #
    # def path_aggregations(self, training: str, path: str) -> list[str]:
    #     root = self.data["trainings"][training]
    #     root = cast(dict[str, Any], root)
    #     aggregations_node = root[path]["aggregations"]
    #     aggregations_node = cast(dict[str, Any], aggregations_node)
    #     return list(aggregations_node.keys())
    #
    # def aggregation_obj(self, training: str, path: str, aggregation: str) -> dict[str, Any] | None:
    #     root = self.data["trainings"][training][path]["aggregations"]
    #     root = cast(dict[str, Any], root)
    #     if aggregation not in root:
    #         return None
    #     obj = root[aggregation]
    #     obj = cast(dict[str, Any], obj)
    #     return obj
    #
    # def constants(self, training: str) -> list[str]:
    #     root = self.data["trainings"][training]["constants"]
    #     root = cast(dict[str, Any], root)
    #     return list(root.keys())
    #
    # def constant_obj(self, training: str) -> dict[str, Any]:
    #     root = self.data["trainings"][training]["constants"]
    #     root = cast(dict[str, Any], root)
    #     return root
    #
    # def note(self, training: str) -> str | None:
    #     root = self.data["trainings"][training]
    #     root = cast(dict[str, Any], root)
    #     return root.get("note")