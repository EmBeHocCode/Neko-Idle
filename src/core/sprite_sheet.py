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
    scale_mode: str = "per_frame",
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

            frames.append(frame)

            if len(frames) >= total_frames:
                return _prepare_frames(
                    surfaces=frames,
                    target_height=target_height,
                    trim_alpha=trim_alpha,
                    smooth=smooth,
                    canvas_size=canvas_size,
                    scale_mode=scale_mode,
                )

    return _prepare_frames(
        surfaces=frames,
        target_height=target_height,
        trim_alpha=trim_alpha,
        smooth=smooth,
        canvas_size=canvas_size,
        scale_mode=scale_mode,
    )


def load_frame_sequence(
    image_paths: list[str | Path],
    target_height: int | None = None,
    trim_alpha: bool = True,
    canvas_size: tuple[int, int] | None = None,
    scale_mode: str = "per_frame",
) -> list[pygame.Surface]:
    """Load animation frames from separate image files."""
    frames: list[pygame.Surface] = []

    for image_path in image_paths:
        frames.append(pygame.image.load(str(image_path)).convert_alpha())

    return _prepare_frames(
        surfaces=frames,
        target_height=target_height,
        trim_alpha=trim_alpha,
        smooth=False,
        canvas_size=canvas_size,
        scale_mode=scale_mode,
    )


def _prepare_frames(
    surfaces: list[pygame.Surface],
    target_height: int | None,
    trim_alpha: bool,
    smooth: bool,
    canvas_size: tuple[int, int] | None,
    scale_mode: str,
) -> list[pygame.Surface]:
    """Prepare an animation while optionally keeping one scale across frames."""
    if scale_mode == "consistent":
        trimmed_frames = [
            _trim_transparent_pixels(surface) if trim_alpha else surface
            for surface in surfaces
        ]
        reference_height = max(
            (frame.get_height() for frame in trimmed_frames),
            default=0,
        )
        scale_factor = None
        if target_height is not None and reference_height > 0:
            scale_factor = target_height / reference_height

        return [
            _prepare_frame(
                surface=frame,
                target_height=None,
                trim_alpha=False,
                smooth=smooth,
                canvas_size=canvas_size,
                scale_factor=scale_factor,
            )
            for frame in trimmed_frames
        ]

    return [
        _prepare_frame(
            surface=surface,
            target_height=target_height,
            trim_alpha=trim_alpha,
            smooth=smooth,
            canvas_size=canvas_size,
        )
        for surface in surfaces
    ]


def _prepare_frame(
    surface: pygame.Surface,
    target_height: int | None,
    trim_alpha: bool,
    smooth: bool,
    canvas_size: tuple[int, int] | None,
    scale_factor: float | None = None,
) -> pygame.Surface:
    """Trim and scale one animation frame."""
    frame = surface

    if trim_alpha:
        frame = _trim_transparent_pixels(frame)

    if scale_factor is not None:
        frame = _scale_by_factor(frame, scale_factor, smooth=smooth)
    elif target_height is not None:
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


def _scale_by_factor(
    surface: pygame.Surface,
    scale_factor: float,
    smooth: bool = True,
) -> pygame.Surface:
    """Scale a frame by an animation-wide factor."""
    width, height = surface.get_size()
    target_width = max(1, int(width * scale_factor))
    target_height = max(1, int(height * scale_factor))
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
