from datetime import datetime
from typing import Any

from libRunning.utils.time import to_sec


def parse_date(dt: str) -> datetime:
    return datetime.strptime(dt, "%Y-%m-%d")


def try_parse_date(dt: str) -> datetime | None:
    try:
        return parse_date(dt)
    except ValueError:
        return None


def intervals_to_sec(min_values: list[str]) -> list[int]:
    return [to_sec(value) for value in min_values]


def get_sorted_section_or_aggregation_values(data: dict[str, Any], type_: str, key: str, reverse: bool = False) -> list[tuple[str, int]]:
    # key = get_key_by_type(type_)
    section_times: dict[str, int] = {}
    for training_key, training in data["trainings"].items():
        for section_key, section_value in training[key].items():
            if section_key == type_ and section_value["value"] != -1:
                section_times[training_key] = section_value["value"]
    return sorted(section_times.items(), key=lambda kv: kv[1], reverse=reverse)
