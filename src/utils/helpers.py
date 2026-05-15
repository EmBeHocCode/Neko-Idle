"""Small shared helper functions."""


def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp a number between two bounds."""
    return max(minimum, min(value, maximum))
