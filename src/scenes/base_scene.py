"""Base scene contract."""


class BaseScene:
    """Base class for future game scenes."""

    def handle_event(self, event: object) -> None:
        """Handle a single input event."""

    def update(self, delta_time: float) -> None:
        """Update scene state."""

    def draw(self, surface: object) -> None:
        """Draw scene content."""
