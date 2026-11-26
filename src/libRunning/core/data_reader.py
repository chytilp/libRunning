from typing import Any


class DataReader:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def get_time_section_node(self, training: str, section: str) -> dict[str, Any]:
        return self.data["trainings"][training]["time"]["sections"][section]