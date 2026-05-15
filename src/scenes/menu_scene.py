"""Main menu scene."""

from pathlib import Path

import pygame

from src.core.sprite_sheet import load_sprite_sheet_frames
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
        self.neko_frames: list[pygame.Surface] = []
        self.current_frame_index = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.16

    def update(self, delta_time: float) -> None:
        """Update menu animations."""
        if not self.neko_frames:
            return

        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            self.current_frame_index = (self.current_frame_index + 1) % len(
                self.neko_frames
            )

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the main menu."""
        self._ensure_fonts()
        self._ensure_neko_frames()
        surface.fill(BACKGROUND_COLOR)

        panel_rect = pygame.Rect(120, 70, WINDOW_WIDTH - 240, WINDOW_HEIGHT - 120)
        pygame.draw.rect(surface, PANEL_COLOR, panel_rect, border_radius=8)
        pygame.draw.rect(surface, ACCENT_COLOR, panel_rect, width=3, border_radius=8)

        self._draw_centered_text(
            surface,
            "Neko Idle Quest",
            self.title_font,
            TEXT_COLOR,
            panel_rect.top + 78,
        )
        self._draw_centered_text(
            surface,
            "Hanh Trinh Tri Thuc",
            self.body_font,
            ACCENT_COLOR,
            panel_rect.top + 126,
        )
        self._draw_neko(surface, panel_rect)
        self._draw_centered_text(
            surface,
            "Neko idle sprite sheet is running",
            self.body_font,
            MUTED_TEXT_COLOR,
            panel_rect.bottom - 44,
        )

    def _ensure_fonts(self) -> None:
        """Create fonts after Pygame is initialized."""
        if self.title_font is None:
            self.title_font = pygame.font.Font(None, 64)
        if self.body_font is None:
            self.body_font = pygame.font.Font(None, 30)

    def _ensure_neko_frames(self) -> None:
        """Load Neko's idle sprite sheet once."""
        if self.neko_frames:
            return

        image_path = Path("assets/images/characters/neko-idle.png")
        if not image_path.exists():
            return

        self.neko_frames = load_sprite_sheet_frames(
            image_path=image_path,
            columns=3,
            rows=2,
            target_height=260,
            cell_crop=(0, 0, 455, 512),
        )

    def _draw_neko(self, surface: pygame.Surface, panel_rect: pygame.Rect) -> None:
        """Draw the animated Neko preview."""
        if not self.neko_frames:
            fallback_rect = pygame.Rect(0, 0, 96, 128)
            fallback_rect.midbottom = (panel_rect.centerx, panel_rect.bottom - 78)
            pygame.draw.rect(surface, ACCENT_COLOR, fallback_rect, border_radius=6)
            return

        frame = self.neko_frames[self.current_frame_index]
        frame_rect = frame.get_rect(
            midbottom=(panel_rect.centerx, panel_rect.bottom - 78)
        )

        surface.blit(frame, frame_rect)

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
