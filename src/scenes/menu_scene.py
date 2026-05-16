"""Main menu scene."""

from pathlib import Path
from typing import Any

import pygame

from src.core.data_manager import DataManager
from src.core.player_animation import DEFAULT_CANVAS_SIZE, PlayerAnimationSystem
from src.core.settings import (
    ACCENT_COLOR,
    BACKGROUND_COLOR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.scenes.base_scene import BaseScene


DEFAULT_CHARACTER_ID = "neko"
DEFAULT_RENDER_HEIGHT = 60
DEFAULT_PLAYER_ANIMATIONS = {
    "idle": {
        "image": "res/images/characters/idle.png",
        "frame_count": 4,
        "frame_duration": 0.22,
        "loop": True,
    },
    "walk": {
        "image": "res/images/characters/walk.png",
        "frame_count": 8,
        "frame_duration": 0.12,
        "loop": True,
        "move_speed": 400,
    },
    "jump": {
        "image": "res/images/characters/jump.png",
        "frame_count": 6,
        "frame_duration": 0.08,
        "loop": False,
        "gravity": 1800,
        "jump_force": -650,
    },
}


class MenuScene(BaseScene):
    """Render the first MVP menu screen."""

    def __init__(self) -> None:
        self.data_manager = DataManager()
        self.map_config = self._load_map_config()
        self.character_animation_data = self.data_manager.load_json(
            "animations/characters.json",
            default={},
        )
        self.preview_character_ids = self._get_preview_character_ids()
        self.preview_character_index = 0
        self.active_character_id = self.preview_character_ids[0]
        self.player_animation_configs = self._load_character_animation_configs(
            self.active_character_id
        )
        self.player_animation = PlayerAnimationSystem(self.player_animation_configs)

        self.map_background_surface: pygame.Surface | None = None
        self.map_land_surface: pygame.Surface | None = None
        self.x = float(self._get_spawn_x("player", WINDOW_WIDTH // 2))
        self.ground_y = float(self._get_player_ground_y())
        self.y = self.ground_y
        self.direction = 1
        self.velocity_y = 0.0
        self.gravity = self._get_jump_config_value("gravity", 1800)
        self.jump_force = self._get_jump_config_value("jump_force", -650)
        self.is_jumping = False
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
            self._start_player_jump()

        if event.key == pygame.K_TAB:
            self._switch_preview_character()

    def update(self, delta_time: float) -> None:
        """Update player movement and animation."""
        self._update_horizontal_movement(delta_time)

        if self.is_jumping:
            self._update_jump_physics(delta_time)
        else:
            self._update_ground_animation()

        self.player_animation.update(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the main menu."""
        self._draw_map(surface)
        self._draw_player(surface)

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
        """Load scaled map surfaces once."""
        if self.map_background_surface is None:
            self.map_background_surface = self._load_map_surface(
                self.map_config.get("background"),
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
        try:
            surface = image.convert_alpha() if use_alpha else image.convert()
        except pygame.error:
            surface = image

        if surface.get_size() == (WINDOW_WIDTH, WINDOW_HEIGHT):
            return surface

        if smooth:
            return pygame.transform.smoothscale(surface, (WINDOW_WIDTH, WINDOW_HEIGHT))

        return pygame.transform.scale(surface, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def _load_character_animation_configs(
        self,
        character_id: str,
    ) -> dict[str, dict[str, Any]]:
        """Load one character's animation config from JSON."""
        character_data = self.character_animation_data.get(character_id, {})
        if not isinstance(character_data, dict):
            character_data = {}

        render_height = int(character_data.get("render_height", DEFAULT_RENDER_HEIGHT))
        default_canvas = self._read_canvas_size(character_data)
        animation_names = set(DEFAULT_PLAYER_ANIMATIONS)
        for key, value in character_data.items():
            if isinstance(value, dict) and "image" in value:
                animation_names.add(key)

        animation_configs: dict[str, dict[str, Any]] = {}
        for animation_name in sorted(animation_names):
            default_config = DEFAULT_PLAYER_ANIMATIONS.get(animation_name, {})
            custom_config = character_data.get(animation_name, {})
            if not isinstance(custom_config, dict):
                custom_config = {}
            if not default_config and not custom_config:
                continue

            config = {**default_config, **custom_config}
            config.setdefault("target_height", render_height)
            config.setdefault("canvas_size", default_canvas)
            config.setdefault("trim_alpha", True)
            animation_configs[animation_name] = config

        return animation_configs

    def _read_canvas_size(self, character_data: dict[str, Any]) -> list[int]:
        """Return fixed player canvas size from character data."""
        canvas_size = character_data.get("canvas_size")
        if isinstance(canvas_size, list) and len(canvas_size) == 2:
            return [int(canvas_size[0]), int(canvas_size[1])]

        return [DEFAULT_CANVAS_SIZE[0], DEFAULT_CANVAS_SIZE[1]]

    def _get_preview_character_ids(self) -> list[str]:
        """Return character IDs available for preview."""
        configured_ids = self.map_config.get("preview_characters", [])
        if not isinstance(configured_ids, list) or not configured_ids:
            configured_ids = [self.map_config.get("player_character")]

        available_ids = [
            str(character_id)
            for character_id in configured_ids
            if character_id in self.character_animation_data
        ]
        if available_ids:
            return available_ids

        if DEFAULT_CHARACTER_ID in self.character_animation_data:
            return [DEFAULT_CHARACTER_ID]

        return [next(iter(self.character_animation_data), DEFAULT_CHARACTER_ID)]

    def _load_map_config(self) -> dict[str, Any]:
        """Load the current map config from JSON."""
        return self.data_manager.load_json("maps/forest_path.json", default={})

    def _switch_preview_character(self) -> None:
        """Switch preview character and preload its animations."""
        if len(self.preview_character_ids) <= 1:
            return

        self.preview_character_index = (
            self.preview_character_index + 1
        ) % len(self.preview_character_ids)
        self.active_character_id = self.preview_character_ids[
            self.preview_character_index
        ]
        self.player_animation_configs = self._load_character_animation_configs(
            self.active_character_id
        )
        self.player_animation = PlayerAnimationSystem(self.player_animation_configs)
        self.velocity_y = 0.0
        self.gravity = self._get_jump_config_value("gravity", 1800)
        self.jump_force = self._get_jump_config_value("jump_force", -650)
        self.is_jumping = False
        self.y = self.ground_y

    def _get_jump_config_value(self, key: str, fallback: float) -> float:
        """Return one numeric value from jump config."""
        return float(self.player_animation_configs.get("jump", {}).get(key, fallback))

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

    def _update_horizontal_movement(self, delta_time: float) -> None:
        """Move player horizontally when A or D is held."""
        move_direction = self._get_pressed_move_direction()
        if move_direction == 0:
            return

        self.direction = move_direction
        walk_config = self.player_animation.get_config("walk")
        move_speed = float(walk_config.get("move_speed", 0))
        if move_speed <= 0:
            return

        left_bound, right_bound = self._get_player_move_bounds()
        self.x += move_speed * move_direction * delta_time
        self.x = max(left_bound, min(right_bound, self.x))

    def _update_ground_animation(self) -> None:
        """Set idle or walk animation while player is grounded."""
        if self._get_pressed_move_direction() == 0:
            self.player_animation.set_animation("idle")
            return

        self.player_animation.set_animation("walk")

    def _start_player_jump(self) -> None:
        """Start jump physics and animation."""
        if self.is_jumping:
            return

        self.is_jumping = True
        self.velocity_y = self.jump_force
        self.player_animation.set_animation("jump")

    def _update_jump_physics(self, delta_time: float) -> None:
        """Update vertical jump physics."""
        self.velocity_y += self.gravity * delta_time
        self.y += self.velocity_y * delta_time

        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.velocity_y = 0.0
            self.is_jumping = False
            self._update_ground_animation()

    def _get_player_move_bounds(self) -> tuple[int, int]:
        """Return horizontal movement bounds for the player."""
        half_width = self.player_animation.get_current_half_width()
        return half_width, WINDOW_WIDTH - half_width

    def _get_player_ground_y(self) -> int:
        """Return player's current ground line."""
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

    def _draw_player(self, surface: pygame.Surface) -> None:
        """Draw the animated player using a midbottom anchor."""
        image = self.player_animation.get_current_frame()
        if self.direction < 0:
            image = pygame.transform.flip(image, True, False)

        rect = image.get_rect(midbottom=(self.x, self.y))
        surface.blit(image, rect)

    # Compatibility helpers for quick local tests from earlier iterations.
    def _set_neko_animation(self, animation_name: str) -> None:
        """Switch player animation."""
        self.player_animation.set_animation(animation_name)

    def _start_neko_jump(self) -> None:
        """Start player jump."""
        self._start_player_jump()

    def _get_neko_draw_y(self) -> int:
        """Return player's current draw baseline."""
        return round(self.y)
