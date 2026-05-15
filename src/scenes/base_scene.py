"""Base scene contract."""

import pygame


class BaseScene:
    """Base class for future game scenes."""

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle a single input event."""

    def update(self, delta_time: float) -> None:
        """Update scene state."""

    def draw(self, surface: pygame.Surface) -> None:
        """Draw scene content."""
