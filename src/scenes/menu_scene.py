"""Main menu scene placeholder."""

import pygame

from src.core.settings import (
    ACCENT_COLOR,
    BACKGROUND_COLOR,
    MUTED_TEXT_COLOR,
    PANEL_COLOR,
    TEXT_COLOR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.scenes.base_scene import BaseScene


class MenuScene(BaseScene):
    """Render the first MVP menu screen."""

    def __init__(self) -> None:
        self.title_font: pygame.font.Font | None = None
        self.body_font: pygame.font.Font | None = None

    def update(self, delta_time: float) -> None:
        """Update menu animations later."""

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the main menu."""
        self._ensure_fonts()
        surface.fill(BACKGROUND_COLOR)

        panel_rect = pygame.Rect(120, 110, WINDOW_WIDTH - 240, WINDOW_HEIGHT - 220)
        pygame.draw.rect(surface, PANEL_COLOR, panel_rect, border_radius=8)
        pygame.draw.rect(surface, ACCENT_COLOR, panel_rect, width=3, border_radius=8)

        self._draw_centered_text(
            surface,
            "Neko Idle Quest",
            self.title_font,
            TEXT_COLOR,
            panel_rect.centery - 70,
        )
        self._draw_centered_text(
            surface,
            "Hanh Trinh Tri Thuc",
            self.body_font,
            ACCENT_COLOR,
            panel_rect.centery - 18,
        )
        self._draw_centered_text(
            surface,
            "MVP-1: Pygame window and menu scene ready",
            self.body_font,
            MUTED_TEXT_COLOR,
            panel_rect.centery + 42,
        )

    def _ensure_fonts(self) -> None:
        """Create fonts after Pygame is initialized."""
        if self.title_font is None:
            self.title_font = pygame.font.Font(None, 64)
        if self.body_font is None:
            self.body_font = pygame.font.Font(None, 30)

    @staticmethod
    def _draw_centered_text(
        surface: pygame.Surface,
        text: str,
        font: pygame.font.Font | None,
        color: tuple[int, int, int],
        y_position: int,
    ) -> None:
        """Draw one line of centered text."""
        if font is None:
            return

        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(WINDOW_WIDTH // 2, y_position))
        surface.blit(rendered_text, text_rect)
