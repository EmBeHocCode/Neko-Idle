"""JSON data loading helpers."""

import json
from pathlib import Path
from typing import Any


class DataManager:
    """Load and cache project JSON data files."""

    def __init__(self, data_dir: str = "data") -> None:
        self.data_dir = Path(data_dir)
        self._cache: dict[Path, Any] = {}

    def load_json(self, relative_path: str, default: Any | None = None) -> Any:
        """Load a JSON file relative to the data folder."""
        path = self.data_dir / relative_path
        if not path.exists():
            return default

        if path not in self._cache:
            with path.open("r", encoding="utf-8") as file:
                self._cache[path] = json.load(file)

        return self._cache[path]
