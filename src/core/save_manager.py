"""Save/load helpers for JSON data."""

import json
from pathlib import Path
from typing import Any


class SaveManager:
    """Read and write JSON save files."""

    def __init__(self, save_path: str = "data/save.json") -> None:
        self.save_path = Path(save_path)

    def load(self) -> dict[str, Any]:
        """Load save data from disk."""
        if not self.save_path.exists():
            return {}

        with self.save_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data: dict[str, Any]) -> None:
        """Save data to disk as formatted JSON."""
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
        with self.save_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")
