"""Sprite sheet helpers."""

from pathlib import Path

import pygame


def load_sprite_sheet_frames(
    image_path: str | Path,
    columns: int,
    rows: int,
    target_height: int | None = None,
    trim_alpha: bool = True,
    cell_crop: tuple[int, int, int, int] | None = None,
) -> list[pygame.Surface]:
    """Load a sprite sheet and split it into frames."""
    sheet = pygame.image.load(str(image_path)).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()
    frame_width = sheet_width // columns
    frame_height = sheet_height // rows

    frames: list[pygame.Surface] = []

    for row in range(rows):
        for column in range(columns):
            frame_rect = pygame.Rect(
                column * frame_width,
                row * frame_height,
                frame_width,
                frame_height,
            )
            frame = sheet.subsurface(frame_rect).copy()

            if cell_crop is not None:
                crop_rect = pygame.Rect(cell_crop).clip(frame.get_rect())
                frame = frame.subsurface(crop_rect).copy()

            frames.append(_prepare_frame(frame, target_height, trim_alpha, smooth=True))

    return frames


def load_frame_sequence(
    image_paths: list[str | Path],
    target_height: int | None = None,
    trim_alpha: bool = True,
) -> list[pygame.Surface]:
    """Load animation frames from separate image files."""
    frames: list[pygame.Surface] = []

    for image_path in image_paths:
        frame = pygame.image.load(str(image_path)).convert_alpha()
        frames.append(_prepare_frame(frame, target_height, trim_alpha, smooth=False))

    return frames


def _prepare_frame(
    surface: pygame.Surface,
    target_height: int | None,
    trim_alpha: bool,
    smooth: bool,
) -> pygame.Surface:
    """Trim and scale one animation frame."""
    frame = surface

    if trim_alpha:
        frame = _trim_transparent_pixels(frame)

    if target_height is not None:
        frame = _scale_to_height(frame, target_height, smooth=smooth)

    return frame


def _trim_transparent_pixels(surface: pygame.Surface) -> pygame.Surface:
    """Remove fully transparent padding around a frame."""
    bounding_rect = surface.get_bounding_rect(min_alpha=1)
    if bounding_rect.width == 0 or bounding_rect.height == 0:
        return surface

    return surface.subsurface(bounding_rect).copy()


def _scale_to_height(
    surface: pygame.Surface,
    target_height: int,
    smooth: bool = True,
) -> pygame.Surface:
    """Scale a frame while keeping aspect ratio."""
    width, height = surface.get_size()
    if height == 0:
        return surface

    scale = target_height / height
    target_width = max(1, int(width * scale))
    target_size = (target_width, target_height)

    if smooth:
        return pygame.transform.smoothscale(surface, target_size)

    return pygame.transform.scale(surface, target_size)
