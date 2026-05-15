"""Base entity data model."""

from dataclasses import dataclass


@dataclass
class BaseEntity:
    """Common combat stats shared by players and enemies."""

    name: str
    max_hp: int
    attack: int
    defense: int
    crit_rate: float = 0.05

    def __post_init__(self) -> None:
        self.current_hp = self.max_hp

    @property
    def is_alive(self) -> bool:
        """Return whether the entity can still fight."""
        return self.current_hp > 0
