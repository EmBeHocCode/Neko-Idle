"""Main game coordinator."""

import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame

from src.core.settings import FPS, GAME_TITLE, WINDOW_HEIGHT, WINDOW_WIDTH
from src.scenes.menu_scene import MenuScene


class Game:
    """Coordinate the Pygame window, main loop, and active scene."""

    def __init__(self) -> None:
        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None
        self.active_scene = MenuScene()
        self.is_running = False

    def run(self, max_frames: int | None = None) -> None:
        """Start Pygame and run the main loop."""
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True

        frame_count = 0

        while self.is_running:
            delta_time = self.clock.tick(FPS) / 1000
            self._handle_events()
            self.active_scene.update(delta_time)
            self._draw()

            frame_count += 1
            if max_frames is not None and frame_count >= max_frames:
                self.is_running = False

        pygame.quit()

    def _handle_events(self) -> None:
        """Handle input and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return

            self.active_scene.handle_event(event)

    def _draw(self) -> None:
        """Draw the active scene."""
        if self.screen is None:
            return

        self.active_scene.draw(self.screen)
        pygame.display.flip()
