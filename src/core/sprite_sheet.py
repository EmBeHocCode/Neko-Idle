"""Sprite sheet helpers."""

from pathlib import Path

import pygame


def load_sprite_sheet_frames(
    image_path: str | Path,
    columns: int | None = None,
    rows: int = 1,
    frame_count: int | None = None,
    target_height: int | None = None,
    trim_alpha: bool = True,
    cell_crop: tuple[int, int, int, int] | None = None,
    canvas_size: tuple[int, int] | None = None,
    smooth: bool = False,
) -> list[pygame.Surface]:
    """Load a sprite sheet and split it into frames."""
    sheet = pygame.image.load(str(image_path)).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()
    total_frames = frame_count or columns
    if total_frames is None:
        raise ValueError("Sprite sheet requires columns or frame_count.")

    columns = columns or total_frames
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

            frames.append(
                _prepare_frame(
                    surface=frame,
                    target_height=target_height,
                    trim_alpha=trim_alpha,
                    smooth=smooth,
                    canvas_size=canvas_size,
                )
            )

            if len(frames) >= total_frames:
                return frames

    return frames


def load_frame_sequence(
    image_paths: list[str | Path],
    target_height: int | None = None,
    trim_alpha: bool = True,
    canvas_size: tuple[int, int] | None = None,
) -> list[pygame.Surface]:
    """Load animation frames from separate image files."""
    frames: list[pygame.Surface] = []

    for image_path in image_paths:
        frame = pygame.image.load(str(image_path)).convert_alpha()
        frames.append(
            _prepare_frame(
                surface=frame,
                target_height=target_height,
                trim_alpha=trim_alpha,
                smooth=False,
                canvas_size=canvas_size,
            )
        )

    return frames


def _prepare_frame(
    surface: pygame.Surface,
    target_height: int | None,
    trim_alpha: bool,
    smooth: bool,
    canvas_size: tuple[int, int] | None,
) -> pygame.Surface:
    """Trim and scale one animation frame."""
    frame = surface

    if trim_alpha:
        frame = _trim_transparent_pixels(frame)

    if target_height is not None:
        frame = _scale_to_height(frame, target_height, smooth=smooth)

    if canvas_size is not None:
        frame = _place_on_canvas(frame, canvas_size)

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

def _place_on_canvas(
    surface: pygame.Surface,
    canvas_size: tuple[int, int],
) -> pygame.Surface:
    """Place a frame on a fixed transparent canvas using midbottom anchor."""
    canvas_width = max(1, max(canvas_size[0], surface.get_width()))
    canvas_height = max(1, max(canvas_size[1], surface.get_height()))
    canvas = pygame.Surface((canvas_width, canvas_height), pygame.SRCALPHA)
    frame_rect = surface.get_rect(midbottom=(canvas_width // 2, canvas_height))
    canvas.blit(surface, frame_rect)
    return canvas
