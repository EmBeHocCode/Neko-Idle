"""Main menu scene."""

from pathlib import Path
from typing import Any

import pygame

from src.core.data_manager import DataManager
from src.core.sprite_sheet import load_frame_sequence, load_sprite_sheet_frames
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


DEFAULT_NEKO_ANIMATIONS = {
    "idle": {
        "frame_files": [
            "assets/images/characters/idle_1.png",
            "assets/images/characters/idle_2.png",
            "assets/images/characters/idle_3.png",
        ],
        "target_height": 180,
        "frame_duration": 0.22,
    },
    "walk": {
        "frame_files": [
            "assets/images/characters/walk_1.png",
            "assets/images/characters/walk_2.png",
            "assets/images/characters/walk_3.png",
            "assets/images/characters/walk_4.png",
            "assets/images/characters/walk_5.png",
        ],
        "target_height": 160,
        "frame_duration": 0.12,
        "move_speed": 90,
    },
    "dash": {
        "frame_files": [
            "assets/images/characters/dash_1.png",
            "assets/images/characters/dash_2.png",
            "assets/images/characters/dash_3.png",
        ],
        "target_height": 96,
        "frame_duration": 0.08,
        "trim_alpha": False,
        "distance": 260,
        "duration": 0.22,
    },
}


class MenuScene(BaseScene):
    """Render the first MVP menu screen."""

    def __init__(self) -> None:
        self.title_font: pygame.font.Font | None = None
        self.body_font: pygame.font.Font | None = None
        self.data_manager = DataManager()
        self.neko_animation_configs = self._load_neko_animation_configs()
        self.neko_animation_name = "idle"
        self.neko_frames: list[pygame.Surface] = []
        self.current_frame_index = 0
        self.animation_timer = 0.0
        self.neko_x = WINDOW_WIDTH // 2
        self.neko_direction = 1
        self.is_neko_dashing = False
        self.dash_elapsed = 0.0
        self.dash_start_x = float(self.neko_x)
        self.dash_target_x = float(self.neko_x)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle menu input events."""
        if event.type != pygame.KEYDOWN:
            return

        if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
            self._start_neko_dash()

    def update(self, delta_time: float) -> None:
        """Update menu animations."""
        if self.is_neko_dashing:
            self._update_neko_dash(delta_time)
        else:
            self._update_neko_movement(delta_time)

        if not self.neko_frames:
            return

        active_config = self._get_active_animation_config()
        frame_duration = float(active_config.get("frame_duration", 0.16))
        self.animation_timer += delta_time

        if self.animation_timer >= frame_duration:
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
            "Neko is ready for adventure",
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
        """Load Neko's active animation frames once."""
        if self.neko_frames:
            return

        active_config = self._get_active_animation_config()
        frame_paths = self._get_frame_paths(active_config)

        if frame_paths:
            self.neko_frames = load_frame_sequence(
                image_paths=frame_paths,
                target_height=int(active_config["target_height"]),
                trim_alpha=bool(active_config.get("trim_alpha", True)),
            )
            return

        image_path = Path(str(active_config.get("image", "")))
        if not image_path.exists():
            return

        self.neko_frames = load_sprite_sheet_frames(
            image_path=image_path,
            columns=int(active_config["columns"]),
            rows=int(active_config["rows"]),
            target_height=int(active_config["target_height"]),
            trim_alpha=bool(active_config.get("trim_alpha", True)),
            cell_crop=self._get_cell_crop(active_config),
        )

    def _load_neko_animation_configs(self) -> dict[str, dict[str, Any]]:
        """Load Neko animation config from JSON."""
        character_data = self.data_manager.load_json(
            "animations/characters.json",
            default={},
        )
        neko_data = character_data.get("neko", {})

        animation_configs: dict[str, dict[str, Any]] = {}
        for animation_name, default_config in DEFAULT_NEKO_ANIMATIONS.items():
            animation_configs[animation_name] = {
                **default_config,
                **neko_data.get(animation_name, {}),
            }

        return animation_configs

    def _get_active_animation_config(self) -> dict[str, Any]:
        """Return config for the active Neko animation."""
        return self.neko_animation_configs[self.neko_animation_name]

    def _get_cell_crop(
        self,
        animation_config: dict[str, Any],
    ) -> tuple[int, int, int, int] | None:
        """Return optional frame crop from config."""
        crop = animation_config.get("cell_crop")
        if not isinstance(crop, list) or len(crop) != 4:
            return None

        return tuple(int(value) for value in crop)

    def _get_frame_paths(self, animation_config: dict[str, Any]) -> list[Path]:
        """Return separate frame image paths if configured."""
        frame_files = animation_config.get("frame_files", [])
        if not isinstance(frame_files, list):
            return []

        frame_paths = [Path(str(path)) for path in frame_files]
        if not all(path.exists() for path in frame_paths):
            return []

        return frame_paths

    def _set_neko_animation(self, animation_name: str) -> None:
        """Switch Neko animation and reset frame playback."""
        if animation_name == self.neko_animation_name:
            return

        self.neko_animation_name = animation_name
        self.neko_frames = []
        self.current_frame_index = 0
        self.animation_timer = 0.0
        self._ensure_neko_frames()

    def _get_pressed_move_direction(self) -> int:
        """Return the current horizontal input direction."""
        pressed_keys = pygame.key.get_pressed()
        return int(pressed_keys[pygame.K_d]) - int(pressed_keys[pygame.K_a])

    def _get_neko_move_bounds(self) -> tuple[int, int]:
        """Return the horizontal movement bounds for the menu preview."""
        return WINDOW_WIDTH // 2 - 260, WINDOW_WIDTH // 2 + 260

    def _start_neko_dash(self) -> None:
        """Dash Neko forward by a fixed distance."""
        if self.is_neko_dashing:
            return

        dash_config = self.neko_animation_configs["dash"]
        move_direction = self._get_pressed_move_direction() or self.neko_direction
        distance = float(dash_config.get("distance", 260))
        left_bound, right_bound = self._get_neko_move_bounds()

        self.neko_direction = move_direction
        self.is_neko_dashing = True
        self.dash_elapsed = 0.0
        self.dash_start_x = float(self.neko_x)
        self.dash_target_x = max(
            left_bound,
            min(right_bound, self.neko_x + distance * move_direction),
        )
        self._set_neko_animation("dash")

    def _update_neko_dash(self, delta_time: float) -> None:
        """Move Neko along the current dash burst."""
        dash_config = self.neko_animation_configs["dash"]
        dash_duration = max(0.01, float(dash_config.get("duration", 0.22)))

        self.dash_elapsed += delta_time
        progress = min(1.0, self.dash_elapsed / dash_duration)
        self.neko_x = self.dash_start_x + (
            self.dash_target_x - self.dash_start_x
        ) * progress

        if progress >= 1.0:
            self.is_neko_dashing = False
            self._update_neko_movement(0.0)

    def _update_neko_movement(self, delta_time: float) -> None:
        """Move Neko only when the player holds A or D."""
        move_direction = self._get_pressed_move_direction()

        if move_direction == 0:
            self._set_neko_animation("idle")
            return

        self.neko_direction = move_direction
        self._set_neko_animation("walk")

        walk_config = self.neko_animation_configs["walk"]
        move_speed = float(walk_config.get("move_speed", 0))
        if move_speed <= 0:
            return

        left_bound, right_bound = self._get_neko_move_bounds()
        self.neko_x += move_speed * move_direction * delta_time
        self.neko_x = max(left_bound, min(right_bound, self.neko_x))

    def _draw_neko(self, surface: pygame.Surface, panel_rect: pygame.Rect) -> None:
        """Draw the animated Neko preview."""
        if not self.neko_frames:
            fallback_rect = pygame.Rect(0, 0, 96, 128)
            fallback_rect.midbottom = (panel_rect.centerx, panel_rect.bottom - 78)
            pygame.draw.rect(surface, ACCENT_COLOR, fallback_rect, border_radius=6)
            return

        frame = self.neko_frames[self.current_frame_index]
        if self.neko_direction < 0:
            frame = pygame.transform.flip(frame, True, False)

        frame_rect = frame.get_rect(
            midbottom=(round(self.neko_x), panel_rect.bottom - 78)
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
