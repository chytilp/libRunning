from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import toml

_config: Config | None = None
_config_file: str = "./config.toml"


def set_config_file(file: str) -> None:
    global _config_file
    _config_file = file


def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config.load()
    return _config


@dataclass
class Config:
    indexLocation: str
    indexLocation2: str
    defaultType: str

    @staticmethod
    def load() -> Config:
        path = Path(Path(__file__).parent, Path(_config_file)).resolve()
        config_data = toml.load(path)
        return Config(**config_data)

    def get_index_file_path(self) -> Path:
        folder = os.path.dirname(os.path.realpath(__file__))
        index_path: Path = Path(self.indexLocation).expanduser()
        if index_path.is_absolute() and index_path.is_file() and index_path.exists():
            file_path = index_path
        else:
            file_path = Path(folder, self.indexLocation)
        return file_path
