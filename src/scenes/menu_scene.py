"""Main menu scene."""

from pathlib import Path
from typing import Any

import pygame

from src.core.data_manager import DataManager
from src.core.sprite_sheet import load_frame_sequence, load_sprite_sheet_frames
from src.core.settings import (
    ACCENT_COLOR,
    BACKGROUND_COLOR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.scenes.base_scene import BaseScene


DEFAULT_NEKO_RENDER_HEIGHT = 160

DEFAULT_NEKO_ANIMATIONS = {
    "idle": {
        "frame_files": [
            "assets/images/characters/idle_1.png",
            "assets/images/characters/idle_2.png",
            "assets/images/characters/idle_3.png",
        ],
        "target_height": 160,
        "frame_duration": 0.22,
        "trim_alpha": False,
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
        "trim_alpha": False,
        "move_speed": 150,
    },
    "dash": {
        "frame_files": [
            "assets/images/characters/dash_1.png",
            "assets/images/characters/dash_2.png",
            "assets/images/characters/dash_3.png",
        ],
        "target_height": 160,
        "frame_duration": 0.08,
        "trim_alpha": False,
        "distance": 260,
        "duration": 0.22,
    },
}


class MenuScene(BaseScene):
    """Render the first MVP menu screen."""

    def __init__(self) -> None:
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
        self.held_keys: set[int] = set()
        self.last_horizontal_key: int | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle menu input events."""
        if event.type == pygame.KEYUP:
            self.held_keys.discard(event.key)
            if event.key == self.last_horizontal_key:
                self.last_horizontal_key = self._find_held_horizontal_key()
            return

        if event.type != pygame.KEYDOWN:
            return

        self.held_keys.add(event.key)
        if event.key in (pygame.K_a, pygame.K_d):
            self.last_horizontal_key = event.key

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
        self._ensure_neko_frames()
        surface.fill(BACKGROUND_COLOR)
        self._draw_neko(surface)

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
        neko_render_height = int(
            neko_data.get("render_height", DEFAULT_NEKO_RENDER_HEIGHT)
        )

        animation_configs: dict[str, dict[str, Any]] = {}
        for animation_name, default_config in DEFAULT_NEKO_ANIMATIONS.items():
            custom_config = neko_data.get(animation_name, {})
            animation_configs[animation_name] = {
                **default_config,
                **custom_config,
            }
            if "target_height" not in custom_config:
                animation_configs[animation_name]["target_height"] = neko_render_height

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
        if self.last_horizontal_key == pygame.K_d:
            return 1
        if self.last_horizontal_key == pygame.K_a:
            return -1

        return int(pygame.K_d in self.held_keys) - int(pygame.K_a in self.held_keys)

    def _find_held_horizontal_key(self) -> int | None:
        """Return a fallback held horizontal key."""
        if pygame.K_d in self.held_keys:
            return pygame.K_d
        if pygame.K_a in self.held_keys:
            return pygame.K_a

        return None

    def _get_neko_move_bounds(self) -> tuple[int, int]:
        """Return the horizontal movement bounds for the menu preview."""
        half_width = self._get_neko_half_width()
        return half_width, WINDOW_WIDTH - half_width

    def _get_neko_half_width(self) -> int:
        """Return half of Neko's current frame width for edge clamping."""
        self._ensure_neko_frames()
        if not self.neko_frames:
            return 48

        widest_frame = max(frame.get_width() for frame in self.neko_frames)
        return max(1, widest_frame // 2)

    def _get_neko_ground_y(self) -> int:
        """Return Neko's current ground line."""
        return WINDOW_HEIGHT - 72

    def _start_neko_dash(self) -> None:
        """Dash Neko forward by a fixed distance."""
        if self.is_neko_dashing:
            return

        dash_config = self.neko_animation_configs["dash"]
        move_direction = self._get_pressed_move_direction() or self.neko_direction
        distance = float(dash_config.get("distance", 260))
        self.neko_direction = move_direction
        self._set_neko_animation("dash")
        left_bound, right_bound = self._get_neko_move_bounds()

        dash_start_x = float(self.neko_x)
        is_dash_blocked_by_edge = (
            (move_direction < 0 and dash_start_x <= left_bound)
            or (move_direction > 0 and dash_start_x >= right_bound)
        )
        if is_dash_blocked_by_edge:
            self._update_neko_movement(0.0)
            return

        dash_target_x = max(
            left_bound,
            min(right_bound, self.neko_x + distance * move_direction),
        )
        if abs(dash_target_x - dash_start_x) < 1:
            self.is_neko_dashing = False
            self._update_neko_movement(0.0)
            return

        self.is_neko_dashing = True
        self.dash_elapsed = 0.0
        self.dash_start_x = dash_start_x
        self.dash_target_x = dash_target_x

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

    def _draw_neko(self, surface: pygame.Surface) -> None:
        """Draw the animated Neko preview."""
        if not self.neko_frames:
            fallback_rect = pygame.Rect(0, 0, 96, 128)
            fallback_rect.midbottom = (round(self.neko_x), self._get_neko_ground_y())
            pygame.draw.rect(surface, ACCENT_COLOR, fallback_rect, border_radius=6)
            return

        frame = self.neko_frames[self.current_frame_index]
        if self.neko_direction < 0:
            frame = pygame.transform.flip(frame, True, False)

        frame_rect = frame.get_rect(
            midbottom=(round(self.neko_x), self._get_neko_ground_y())
        )
        surface.blit(frame, frame_rect)
