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
        "loop": False,
        "scale_mode": "consistent",
        "trim_alpha": True,
        "gravity": 1800,
        "jump_force": -650,
        "pose_mode": "velocity",
        "pose_frames": {
            "takeoff": 0,
            "rise": 4,
            "apex": 6,
            "fall": 8,
            "land": 10,
        },
        "landing_height": 24,
        "apex_velocity": 140,
    },
}


class MenuScene(BaseScene):
    """Render the first MVP menu screen."""

    def __init__(self) -> None:
        self.data_manager = DataManager()
        self.map_config = self._load_map_config()
        self.map_background_surface: pygame.Surface | None = None
        self.map_land_surface: pygame.Surface | None = None
        self.neko_animation_configs = self._load_neko_animation_configs()
        self.neko_animation_name = "idle"
        self.neko_frames: list[pygame.Surface] = []
        self.current_frame_index = 0
        self.animation_timer = 0.0
        self.neko_x = self._get_spawn_x("player", WINDOW_WIDTH // 2)
        self.ground_y = float(self._get_neko_ground_y())
        self.neko_y = self.ground_y
        self.neko_direction = 1
        self.is_neko_jumping = False
        self.velocity_y = 0.0
        self.jump_elapsed = 0.0
        self.jump_duration = self._get_jump_duration(
            self.neko_animation_configs["jump"]
        )
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
            if self.is_neko_jumping:
                self._sync_neko_jump_frame()
                return
        else:
            self._update_ground_animation()

        self._update_neko_animation_frame(delta_time)

    def _update_neko_animation_frame(self, delta_time: float) -> None:
        """Advance the active Neko animation by time."""
        if not self.neko_frames:
            return

        active_config = self._get_active_animation_config()
        frame_duration = max(0.01, float(active_config.get("frame_duration", 0.16)))
        should_loop = bool(active_config.get("loop", True))
        self.animation_timer += delta_time

        while self.animation_timer >= frame_duration:
            self.animation_timer -= frame_duration
            if should_loop:
                self.current_frame_index = (self.current_frame_index + 1) % len(
                    self.neko_frames
                )
            else:
                self.current_frame_index = min(
                    self.current_frame_index + 1,
                    len(self.neko_frames) - 1,
                )

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the main menu."""
        self._ensure_neko_frames()
        self._draw_map(surface)
        self._draw_neko(surface)

    def _draw_map(self, surface: pygame.Surface) -> None:
        """Draw the current map background and land layers."""
        self._ensure_map_surfaces()
        if self.map_background_surface is None:
            surface.fill(BACKGROUND_COLOR)
        else:
            surface.blit(self.map_background_surface, (0, 0))

        if self.map_land_surface is not None:
            surface.blit(self.map_land_surface, (0, 0))

    def _ensure_map_surfaces(self) -> None:
        """Load scaled map surfaces once after the display exists."""
        if self.map_background_surface is None:
            background_path = self.map_config.get("background")
            self.map_background_surface = self._load_map_surface(
                background_path,
                use_alpha=False,
                smooth=True,
            )

        if self.map_land_surface is None:
            land_config = self.map_config.get("land", {})
            land_path = (
                land_config.get("image") if isinstance(land_config, dict) else None
            )
            self.map_land_surface = self._load_map_surface(
                land_path,
                use_alpha=True,
                smooth=False,
            )

    def _load_map_surface(
        self,
        image_path: object,
        use_alpha: bool,
        smooth: bool,
    ) -> pygame.Surface | None:
        """Load and scale one map layer to the game window."""
        if not image_path:
            return None

        path = Path(str(image_path))
        if not path.exists():
            return None

        image = pygame.image.load(str(path))
        surface = image.convert_alpha() if use_alpha else image.convert()
        if surface.get_size() == (WINDOW_WIDTH, WINDOW_HEIGHT):
            return surface

        if smooth:
            return pygame.transform.smoothscale(surface, (WINDOW_WIDTH, WINDOW_HEIGHT))

        return pygame.transform.scale(surface, (WINDOW_WIDTH, WINDOW_HEIGHT))

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
                scale_mode=str(active_config.get("scale_mode", "per_frame")),
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
            scale_mode=str(active_config.get("scale_mode", "per_frame")),
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

    def _load_map_config(self) -> dict[str, Any]:
        """Load the current map config from JSON."""
        return self.data_manager.load_json("maps/forest_path.json", default={})

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
        land_config = self.map_config.get("land", {})
        if isinstance(land_config, dict) and "ground_y" in land_config:
            return round(float(land_config["ground_y"]) * self._get_map_scale_y())

        return WINDOW_HEIGHT - 72

    def _get_spawn_x(self, spawn_name: str, fallback: int) -> int:
        """Return a spawn X coordinate scaled from map data."""
        spawn_points = self.map_config.get("spawn_points", {})
        if not isinstance(spawn_points, dict):
            return fallback

        spawn_point = spawn_points.get(spawn_name)
        if not isinstance(spawn_point, list) or len(spawn_point) < 1:
            return fallback

        return round(float(spawn_point[0]) * self._get_map_scale_x())

    def _get_map_scale_x(self) -> float:
        """Return the source-to-window X scale."""
        source_width, _ = self._get_map_source_size()
        return WINDOW_WIDTH / source_width

    def _get_map_scale_y(self) -> float:
        """Return the source-to-window Y scale."""
        _, source_height = self._get_map_source_size()
        return WINDOW_HEIGHT / source_height

    def _get_map_source_size(self) -> tuple[float, float]:
        """Return source map size from config."""
        source_size = self.map_config.get("source_size", [])
        if isinstance(source_size, list) and len(source_size) == 2:
            return max(1.0, float(source_size[0])), max(1.0, float(source_size[1]))

        return float(WINDOW_WIDTH), float(WINDOW_HEIGHT)

    def _start_neko_jump(self) -> None:
        """Start Neko's jump physics and animation."""
        if self.is_neko_jumping:
            return

        jump_config = self.neko_animation_configs["jump"]
        self.is_neko_jumping = True
        self.jump_elapsed = 0.0
        self.jump_duration = self._get_jump_duration(jump_config)
        self.velocity_y = float(jump_config.get("jump_force", -650))
        self._set_neko_animation("jump")
        self.current_frame_index = 0

    def _update_jump_physics(self, delta_time: float) -> None:
        """Update Neko's vertical jump physics."""
        jump_config = self.neko_animation_configs["jump"]
        gravity = float(jump_config.get("gravity", 1800))

        self.jump_elapsed += delta_time
        self.velocity_y += gravity * delta_time
        self.neko_y += self.velocity_y * delta_time

        if self.neko_y >= self.ground_y:
            self.neko_y = self.ground_y
            self.velocity_y = 0.0
            self.is_neko_jumping = False
            self.jump_elapsed = 0.0
            self._update_ground_animation()

    def _sync_neko_jump_frame(self) -> None:
        """Select jump frame from jump progress instead of looping by timer."""
        if not self.neko_frames:
            self._ensure_neko_frames()
        if not self.neko_frames:
            return

        jump_config = self.neko_animation_configs["jump"]
        if jump_config.get("pose_mode") == "velocity":
            self.current_frame_index = self._get_velocity_jump_frame(jump_config)
            return

        jump_progress = min(1.0, self.jump_elapsed / max(0.01, self.jump_duration))
        self.current_frame_index = min(
            len(self.neko_frames) - 1,
            int(jump_progress * len(self.neko_frames)),
        )

    def _get_velocity_jump_frame(self, jump_config: dict[str, Any]) -> int:
        """Pick a stable jump pose from vertical velocity and height."""
        pose_frames = jump_config.get("pose_frames", {})
        if not isinstance(pose_frames, dict):
            pose_frames = {}

        air_height = max(0.0, self.ground_y - self.neko_y)
        landing_height = float(jump_config.get("landing_height", 24))
        apex_velocity = float(jump_config.get("apex_velocity", 140))

        if air_height <= landing_height and self.velocity_y <= 0:
            pose_name = "takeoff"
        elif air_height <= landing_height and self.velocity_y > 0:
            pose_name = "land"
        elif self.velocity_y < -apex_velocity:
            pose_name = "rise"
        elif self.velocity_y > apex_velocity:
            pose_name = "fall"
        else:
            pose_name = "apex"

        fallback_frame = 0
        frame_index = int(pose_frames.get(pose_name, fallback_frame))
        return max(0, min(len(self.neko_frames) - 1, frame_index))

    def _get_jump_duration(self, jump_config: dict[str, Any]) -> float:
        """Estimate total airtime so jump frames can follow physics."""
        if "animation_duration" in jump_config:
            return max(0.01, float(jump_config["animation_duration"]))

        gravity = float(jump_config.get("gravity", 1800))
        jump_force = abs(float(jump_config.get("jump_force", -650)))
        if gravity > 0 and jump_force > 0:
            return (jump_force * 2) / gravity

        frame_count = int(jump_config.get("frame_count", 1))
        frame_duration = float(jump_config.get("frame_duration", 0.06))
        return max(0.01, frame_count * frame_duration)

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
