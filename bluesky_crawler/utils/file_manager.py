import json
import os
from typing import IO, Any, Optional, Union

from loguru import logger

JsonObject = Union[list[Any], dict[Any, Any]]


def create_file(file_path) -> None:
    """Create a file"""
    file_dir = os.path.dirname(file_path)
    os.makedirs(file_dir, exist_ok=True)
    if not os.path.exists(file_path):
        logger.info(f"File created. ({file_path})")
        with open(file_path, "w"):
            pass


class JsonLinesFile:
    _file: Optional[IO]
    file_path: str

    def __init__(self, file_path: str, open: bool = True, mode: str = "a") -> None:
        self.file_path = file_path
        self._file = None
        if open:
            self.open(mode=mode)

    def open(self, mode: str = "a", force: bool = True) -> None:
        logger.info(f"A File opened. ({self.file_path})")
        if force:
            create_file(self.file_path)
        self._file = open(self.file_path, mode)

    def close(self) -> None:
        logger.info(f"A File closed. ({self.file_path})")
        self._file.close()

    def reopen(self, new_file_path: str, mode: str = "a") -> None:
        self.close()
        self.file_path = new_file_path
        self.open(mode=mode)

    def add_json(self, obj: JsonObject) -> None:
        self._file.write(json.dumps(obj, ensure_ascii=False))
        self._file.write("\n")
