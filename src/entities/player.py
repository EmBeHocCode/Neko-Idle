"""Player entity."""

from dataclasses import dataclass

from src.entities.base_entity import BaseEntity


@dataclass
class Player(BaseEntity):
    """Neko player data."""

    level: int = 1
    exp: int = 0
    gold: int = 0
