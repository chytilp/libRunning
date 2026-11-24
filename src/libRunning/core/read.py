import json
from copy import copy, deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from libRunning.core.data_wrapper import DataWrapper
from libRunning.core.auxiliary import (
    intervals_to_sec,
    parse_date,
    try_parse_date,
)
from libRunning.core.data_module import data as original_data

from libRunning.utils.time import to_sec

def read_data(data: dict[str, Any], files: list[str], from_: str = "", to_: str = "") -> DataWrapper:
    new_data: dict[str, Any] = copy(data)
    dt_from: datetime | None = try_parse_date(from_)
    dt_to: datetime | None = try_parse_date(to_)
    if dt_from is None:
        dt_from = datetime(2020, 1, 1)
    if dt_to is None:
        dt_to = datetime.now()
    file_data: dict[str, dict[str, Any]] = json.load(open(Path(files[0]).resolve()))

    trainings = new_data["trainings"]
    for date, values in file_data.items():
        train_dt: datetime = parse_date(date)
        training_key = train_dt.strftime("%Y-%m-%d")
        disabled: bool | None = values.get("disabled")
        if disabled is True:
            continue

        if dt_from <= train_dt <= dt_to:
            has: dict = {"time": "time" in values.keys(), "tf": "tf" in values.keys()}

            has_constants = "constants" in values.keys()
            trainings[training_key] = {"note": ""}
            for path in ["time", "tf"]:
                if has[path]:
                    trainings[training_key].update({path: {"sections": {}, "aggregations": {}}})

            if has_constants:
                trainings[training_key].update({"constants": {}})
            # note
            note = values.get("note")
            if note is not None:
                trainings[training_key]["note"] = note

            for path in ["time", "tf"]:
                if has[path]:
                    for section, value in values[path].items():
                        trainings[training_key][path]["sections"][section] = {"order": -1, "lost": -1, "grade": -1, "value": -1}
                        if path in {"time",}:
                            trainings[training_key][path]["sections"][section]["value"] = to_sec(value)
                        else:
                            trainings[training_key][path]["sections"][section]["value"] = value
            if has_constants:
                trainings[training_key]["constants"] = values["constants"]

    return DataWrapper(new_data)


def read(data: dict[str, Any], files: list[str], from_: str = "", to_: str = "") -> dict[str, Any]:
    new_data: dict[str, Any] = deepcopy(data)
    dt_from: datetime | None = try_parse_date(from_)
    dt_to: datetime | None = try_parse_date(to_)
    if dt_from is None:
        dt_from = datetime(2020, 1, 1)
    if dt_to is None:
        dt_to = datetime.now()
    file_data: dict[str, dict[str, Any]] = json.load(open(Path(files[0]).resolve()))

    trainings = new_data["trainings"]
    for date, values in file_data.items():
        train_dt: datetime = parse_date(date)
        training_key = train_dt.strftime("%Y-%m-%d")
        disabled: bool | None = values.get("disabled")
        if disabled is True:
            continue

        if dt_from <= train_dt <= dt_to:
            trainings[training_key] = {"note": "", "sections": {}, "aggregations": {}}
            # note
            note = values.get("note")
            if note is not None:
                trainings[training_key]["note"] = note
            # sections
            for section, value in values["sections"].items():
                trainings[training_key]["sections"][section] = {"order": -1, "lost": -1, "grade": -1, "value": -1}
                trainings[training_key]["sections"][section]["value"] = to_sec(value)

            # intervals
            intervals = values.get("intervals")
            if intervals is not None:
                trainings[training_key]["intervals"] = {"values": intervals_to_sec(intervals["values"]),
                                                        "type": int(intervals["type"])}
    return new_data


def filter_(data: dict[str, Any], from_: str = "", to_: str = "") -> dict[str, Any]:
    if from_ == "" and to_ == "":
        return data
    date_from = datetime(1970, 1, 1)
    if from_:
        date_from = datetime.strptime(from_, "%Y-%m-%d")
    now = datetime.today()
    date_to = datetime(now.year, now.month, now.day)
    if to_:
        date_to = datetime.strptime(to_, "%Y-%m-%d")
    new_data = deepcopy(original_data)
    for date_key, values in data["trainings"].items():
        dt = datetime.strptime(date_key, "%Y-%m-%d")
        if date_from <= dt < date_to:
            new_data["trainings"][date_key] = values
    return new_data