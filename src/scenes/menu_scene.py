"""Main menu scene."""

from pathlib import Path
from typing import Any

import pygame

from src.core.data_manager import DataManager
from src.core.player_animation import DEFAULT_CANVAS_SIZE, PlayerAnimationSystem
from src.core.settings import BACKGROUND_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH
from src.scenes.base_scene import BaseScene
from src.systems.player_controller import PlayerController


DEFAULT_CHARACTER_ID = "hero_01"


class MenuScene(BaseScene):
    """Render the first MVP menu screen."""

    def __init__(self) -> None:
        self.data_manager = DataManager()
        self.map_config = self._load_map_config()
        self.player_config_data = self.data_manager.load_json(
            "player_animations.json",
            default={},
        )
        self.preview_character_ids = self._get_preview_character_ids()
        self.preview_character_index = self._get_initial_character_index()
        self.active_character_id = self.preview_character_ids[
            self.preview_character_index
        ]

        self.map_background_surface: pygame.Surface | None = None
        self.map_land_surface: pygame.Surface | None = None
        self.held_keys: set[int] = set()
        self.last_horizontal_key: int | None = None
        self.player = self._create_player_controller(
            x=float(self._get_spawn_x("player", WINDOW_WIDTH // 2)),
            ground_y=float(self._get_player_ground_y()),
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle player input events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.player.request_attack()
            return

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

        if event.key == pygame.K_SPACE:
            self.player.request_jump()

        if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
            self.player.request_dash(self._get_pressed_move_direction())

        if event.key == pygame.K_TAB:
            self._switch_preview_character()

    def update(self, delta_time: float) -> None:
        """Update player movement and animation."""
        self.player.update(
            delta_time=delta_time,
            move_direction=self._get_pressed_move_direction(),
            run_pressed=self._is_run_pressed(),
            movement_bounds=self._get_player_move_bounds(),
        )

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the current scene."""
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

    def _create_player_controller(
        self,
        x: float,
        ground_y: float,
    ) -> PlayerController:
        """Create the runtime player controller for the active character."""
        character_config = self._get_active_character_config()
        animation_configs = self._build_animation_configs(character_config)
        animation_system = PlayerAnimationSystem(animation_configs)
        movement_config = character_config.get("movement", {})
        if not isinstance(movement_config, dict):
            movement_config = {}

        return PlayerController(
            animation=animation_system,
            movement_config=movement_config,
            x=x,
            ground_y=ground_y,
        )

    def _get_active_character_config(self) -> dict[str, Any]:
        """Return config for the active player character."""
        characters = self.player_config_data.get("characters", {})
        character_config = characters.get(self.active_character_id, {})
        if not isinstance(character_config, dict):
            raise ValueError(f"Missing player config for {self.active_character_id}.")

        return character_config

    def _build_animation_configs(
        self,
        character_config: dict[str, Any],
    ) -> dict[str, dict[str, Any]]:
        """Merge shared character render settings into each animation config."""
        animations = character_config.get("animations", {})
        if not isinstance(animations, dict):
            raise ValueError("Player animation config must contain animations.")

        canvas_size = character_config.get(
            "canvas_size",
            [DEFAULT_CANVAS_SIZE[0], DEFAULT_CANVAS_SIZE[1]],
        )
        target_height = character_config.get("target_height")
        animation_configs: dict[str, dict[str, Any]] = {}
        for animation_name, animation_config in animations.items():
            if not isinstance(animation_config, dict):
                continue

            config = dict(animation_config)
            config.setdefault("canvas_size", canvas_size)
            if target_height is not None:
                config.setdefault("target_height", target_height)
            animation_configs[str(animation_name)] = config

        return animation_configs

    def _get_preview_character_ids(self) -> list[str]:
        """Return character IDs available for preview."""
        characters = self.player_config_data.get("characters", {})
        if isinstance(characters, dict) and characters:
            return [str(character_id) for character_id in characters]

        return [DEFAULT_CHARACTER_ID]

    def _get_initial_character_index(self) -> int:
        """Return the initial active character index."""
        active_character = self.player_config_data.get(
            "active_character",
            DEFAULT_CHARACTER_ID,
        )
        if active_character in self.preview_character_ids:
            return self.preview_character_ids.index(active_character)

        return 0

    def _switch_preview_character(self) -> None:
        """Switch preview character and rebuild runtime player state."""
        if len(self.preview_character_ids) <= 1:
            return

        self.preview_character_index = (
            self.preview_character_index + 1
        ) % len(self.preview_character_ids)
        self.active_character_id = self.preview_character_ids[
            self.preview_character_index
        ]
        self.player = self._create_player_controller(
            x=self.player.x,
            ground_y=float(self._get_player_ground_y()),
        )

    def _load_map_config(self) -> dict[str, Any]:
        """Load the current map config from JSON."""
        return self.data_manager.load_json("maps/forest_path.json", default={})

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

    def _is_run_pressed(self) -> bool:
        """Return whether the player is holding a run key."""
        return pygame.K_LSHIFT in self.held_keys or pygame.K_RSHIFT in self.held_keys

    def _get_player_move_bounds(self) -> tuple[int, int]:
        """Return horizontal movement bounds for the player."""
        half_width = self.player.animation.get_current_half_width()
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
        image = self.player.animation.get_current_frame()
        if self.player.direction < 0:
            image = pygame.transform.flip(image, True, False)

        rect = image.get_rect(midbottom=(self.player.x, self.player.y))
        surface.blit(image, rect)

    # Compatibility helpers for quick local tests from earlier iterations.
    def _set_neko_animation(self, animation_name: str) -> None:
        """Switch player animation."""
        self.player.animation.set_animation(animation_name)
        self.player.state = animation_name

    def _start_neko_jump(self) -> None:
        """Start player jump."""
        self.player.request_jump()

    def _get_neko_draw_y(self) -> int:
        """Return player's current draw baseline."""
        return round(self.player.y)
