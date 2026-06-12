from pathlib import Path
from typing import Any

from libRunning.core.functions import read

folder = Path(__file__).parent.resolve()


def test_read_1_8_1() -> None:
    data: dict[str, Any] = {"trainings": {}}
    new_data = read(data, ["./tests/data/data_01.json"])
    assert len(new_data["trainings"]) == 1
    assert list(new_data["trainings"].keys()) == ["2026-02-14"]
    root = new_data["trainings"]["2026-02-14"]
    assert root["note"] == "this is note"
    assert list(root["sections"].keys()) == ["0.km", "1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km", "09.km"]
    assert root["sections"]["0.km"]["value"] == 453
    assert root["sections"]["1.km"]["value"] == 313
    assert root["sections"]["2.km"]["value"] == 392
    assert root["sections"]["3.km"]["value"] == 331
    assert root["sections"]["4.km"]["value"] == 384
    assert root["sections"]["5.km"]["value"] == 345
    assert root["sections"]["6.km"]["value"] == 381
    assert root["sections"]["7.km"]["value"] == 321
    assert root["sections"]["8.km"]["value"] == 374
    assert root["sections"]["09.km"]["value"] == 487


def test_read_filtered() -> None:
    data: dict[str, Any] = {"trainings": {}}
    new_data = read(data, ["./tests/data/data_02.json"], "2026-02-01", "2026-02-28")
    assert len(new_data["trainings"]) == 2
    assert list(new_data["trainings"].keys()) == ["2026-02-14", "2026-02-10"]


def test_read_with_disabled_training() -> None:
    data: dict[str, Any] = {"trainings": {}}
    new_data = read(data, ["./tests/data/data_03.json"])
    assert len(new_data["trainings"]) == 2
    assert list(new_data["trainings"].keys()) == ["2026-02-14", "2026-01-28"]


def test_read_data_immutable() -> None:
    data: dict[str, Any] = {"trainings": {}}
    new_data = read(data, ["./tests/data/data_03.json"])
    assert id(data) != id(new_data)


def test_read_training_with_interval() -> None:
    data: dict[str, Any] = {"trainings": {}}
    new_data = read(data, ["./tests/data/data_04.json"])
    assert len(new_data["trainings"]) == 1
    root = new_data["trainings"]["2025-11-19"]
    assert "intervals" in list(root.keys())
    intervals = root["intervals"]
    assert intervals["values"] == [156, 144, 145]
    assert intervals["type"] == 500
    assert list(root["sections"].keys()) == ["0.km", "1.km", "2.km", "3.km", "4.km", "09.km", "010.km"]
