"""Helpers for resolving asset paths."""

from pathlib import Path


class AssetLoader:
    """Resolve paths inside the assets folder."""

    def __init__(self, assets_dir: str = "assets") -> None:
        self.assets_dir = Path(assets_dir)

    def get_path(self, *parts: str) -> Path:
        """Return an asset path without loading it yet."""
        return self.assets_dir.joinpath(*parts)
