"""Player entity."""

from dataclasses import dataclass

from src.entities.base_entity import BaseEntity


@dataclass
class Player(BaseEntity):
    """Neko player data."""

    level: int = 1
    exp: int = 0
    gold: int = 0
    velocity_y: float = 0.0
    gravity: float = 1800.0
    jump_force: float = -650.0
    is_jumping: bool = False
    ground_y: float = 0.0
