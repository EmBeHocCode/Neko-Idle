"""Boss entity."""

from dataclasses import dataclass

from src.entities.enemy import Enemy


@dataclass
class Boss(Enemy):
    """Boss enemy data."""

    unlock_area_id: str | None = None
