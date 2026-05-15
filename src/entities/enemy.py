"""Enemy entity."""

from dataclasses import dataclass

from src.entities.base_entity import BaseEntity


@dataclass
class Enemy(BaseEntity):
    """Regular enemy data."""

    exp_reward: int = 0
    gold_reward: int = 0
