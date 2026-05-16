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
DEFAULT_NEKO_CANVAS_RATIO = 2

DEFAULT_NEKO_ANIMATIONS = {
    "idle": {
        "image": "res/images/characters/idle.png",
        "frame_count": 4,
        "target_height": 160,
        "frame_duration": 0.22,
        "trim_alpha": True,
    },
    "walk": {
        "image": "res/images/characters/walk.png",
        "frame_count": 8,
        "target_height": 160,
        "frame_duration": 0.12,
        "trim_alpha": True,
        "move_speed": 150,
    },
    "jump": {
        "image": "res/images/characters/jump.png",
        "frame_count": 12,
        "target_height": 160,
        "frame_duration": 0.06,
        "trim_alpha": True,
        "gravity": 1800,
        "jump_force": -650,
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
        self.ground_y = float(self._get_neko_ground_y())
        self.neko_y = self.ground_y
        self.neko_direction = 1
        self.is_neko_jumping = False
        self.velocity_y = 0.0
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

        if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
            self._start_neko_jump()

    def update(self, delta_time: float) -> None:
        """Update menu animations."""
        self._update_horizontal_movement(delta_time)

        if self.is_neko_jumping:
            self._update_jump_physics(delta_time)
        else:
            self._update_ground_animation()

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
                canvas_size=self._get_canvas_size(active_config),
            )
            return

        image_path = Path(str(active_config.get("image", "")))
        if not image_path.exists():
            return

        self.neko_frames = load_sprite_sheet_frames(
            image_path=image_path,
            columns=int(active_config.get("columns", active_config["frame_count"])),
            rows=int(active_config.get("rows", 1)),
            frame_count=int(active_config["frame_count"]),
            target_height=int(active_config["target_height"]),
            trim_alpha=bool(active_config.get("trim_alpha", True)),
            cell_crop=self._get_cell_crop(active_config),
            canvas_size=self._get_canvas_size(active_config),
            smooth=bool(active_config.get("smooth_scale", False)),
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
        default_canvas_size = self._get_default_canvas_size(
            neko_data,
            neko_render_height,
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
            if "canvas_size" not in custom_config:
                animation_configs[animation_name]["canvas_size"] = default_canvas_size

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

    def _get_canvas_size(
        self,
        animation_config: dict[str, Any],
    ) -> tuple[int, int] | None:
        """Return optional fixed canvas size from config."""
        canvas_size = animation_config.get("canvas_size")
        if not isinstance(canvas_size, list) or len(canvas_size) != 2:
            return None

        return int(canvas_size[0]), int(canvas_size[1])

    def _get_default_canvas_size(
        self,
        neko_data: dict[str, Any],
        render_height: int,
    ) -> list[int]:
        """Return global Neko canvas size, scaled with render height."""
        canvas_size = neko_data.get("canvas_size")
        if isinstance(canvas_size, list) and len(canvas_size) == 2:
            return [int(canvas_size[0]), int(canvas_size[1])]

        canvas_length = render_height * DEFAULT_NEKO_CANVAS_RATIO
        return [canvas_length, canvas_length]

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
            self._ensure_neko_frames()
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

        widest_frame = max(
            frame.get_bounding_rect(min_alpha=1).width for frame in self.neko_frames
        )
        return max(1, widest_frame // 2)

    def _get_neko_ground_y(self) -> int:
        """Return Neko's current ground line."""
        return WINDOW_HEIGHT - 72

    def _start_neko_jump(self) -> None:
        """Start Neko's jump physics and animation."""
        if self.is_neko_jumping:
            return

        jump_config = self.neko_animation_configs["jump"]
        self.is_neko_jumping = True
        self.velocity_y = float(jump_config.get("jump_force", -650))
        self._set_neko_animation("jump")

    def _update_jump_physics(self, delta_time: float) -> None:
        """Update Neko's vertical jump physics."""
        jump_config = self.neko_animation_configs["jump"]
        gravity = float(jump_config.get("gravity", 1800))

        self.velocity_y += gravity * delta_time
        self.neko_y += self.velocity_y * delta_time

        if self.neko_y >= self.ground_y:
            self.neko_y = self.ground_y
            self.velocity_y = 0.0
            self.is_neko_jumping = False
            self._update_ground_animation()

    def _update_horizontal_movement(self, delta_time: float) -> None:
        """Move Neko horizontally when the player holds A or D."""
        move_direction = self._get_pressed_move_direction()

        if move_direction == 0:
            return

        self.neko_direction = move_direction
        walk_config = self.neko_animation_configs["walk"]
        move_speed = float(walk_config.get("move_speed", 0))
        if move_speed <= 0:
            return

        left_bound, right_bound = self._get_neko_move_bounds()
        self.neko_x += move_speed * move_direction * delta_time
        self.neko_x = max(left_bound, min(right_bound, self.neko_x))

    def _update_ground_animation(self) -> None:
        """Set idle or walk animation while Neko is on the ground."""
        if self._get_pressed_move_direction() == 0:
            self._set_neko_animation("idle")
            return

        self._set_neko_animation("walk")

    def _draw_neko(self, surface: pygame.Surface) -> None:
        """Draw the animated Neko preview."""
        if not self.neko_frames:
            fallback_rect = pygame.Rect(0, 0, 96, 128)
            fallback_rect.midbottom = (round(self.neko_x), self._get_neko_draw_y())
            pygame.draw.rect(surface, ACCENT_COLOR, fallback_rect, border_radius=6)
            return

        frame = self.neko_frames[self.current_frame_index]
        if self.neko_direction < 0:
            frame = pygame.transform.flip(frame, True, False)

        frame_rect = frame.get_rect(
            midbottom=(round(self.neko_x), self._get_neko_draw_y())
        )
        surface.blit(frame, frame_rect)

    def _get_neko_draw_y(self) -> int:
        """Return Neko's current draw baseline."""
        return round(self.neko_y)
