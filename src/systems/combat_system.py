"""Auto combat system placeholder."""

from src.entities.base_entity import BaseEntity


class CombatSystem:
    """Calculate simple combat interactions."""

    @staticmethod
    def calculate_damage(attacker: BaseEntity, defender: BaseEntity) -> int:
        """Calculate minimum 1 damage after defense."""
        return max(1, attacker.attack - defender.defense)
