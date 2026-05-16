"""Player animation loading and playback."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pygame


DEFAULT_CANVAS_SIZE = (256, 256)


@dataclass
class AnimationClip:
    """Cached frames and playback settings for one animation."""

    frames: list[pygame.Surface]
    frame_duration: float
    loop: bool = True


@dataclass
class PreparedAnimationFrames:
    """Cut frames prepared for final scaling and canvas placement."""

    visible_frames: list[pygame.Surface]
    source_frame_size: tuple[int, int]


class PlayerAnimationSystem:
    """Load player sprite sheets once and play cached frames."""

    def __init__(self, animation_configs: dict[str, dict[str, Any]]) -> None:
        self.configs = animation_configs
        self.clips = self._load_clips(animation_configs)
        self.current_name = "idle" if "idle" in self.clips else next(iter(self.clips))
        self.current_frame_index = 0
        self.animation_timer = 0.0

    def set_animation(self, animation_name: str) -> None:
        """Switch animation while preserving cached frames."""
        if animation_name not in self.clips:
            animation_name = "idle"

        if animation_name == self.current_name:
            return

        self.current_name = animation_name
        self.current_frame_index = 0
        self.animation_timer = 0.0

    def update(self, delta_time: float) -> None:
        """Advance the current animation."""
        clip = self.clips[self.current_name]
        if len(clip.frames) <= 1:
            return

        self.animation_timer += delta_time
        frame_duration = max(0.01, clip.frame_duration)
        while self.animation_timer >= frame_duration:
            self.animation_timer -= frame_duration
            if clip.loop:
                self.current_frame_index = (
                    self.current_frame_index + 1
                ) % len(clip.frames)
            else:
                self.current_frame_index = min(
                    self.current_frame_index + 1,
                    len(clip.frames) - 1,
                )

    def get_current_frame(self) -> pygame.Surface:
        """Return the current rendered frame."""
        clip = self.clips[self.current_name]
        return clip.frames[self.current_frame_index]

    def get_config(self, animation_name: str) -> dict[str, Any]:
        """Return raw config for one animation."""
        return self.configs.get(animation_name, {})

    def get_current_half_width(self) -> int:
        """Return half of the current animation's widest visible frame."""
        clip = self.clips[self.current_name]
        widest_frame = max(
            frame.get_bounding_rect(min_alpha=1).width for frame in clip.frames
        )
        return max(1, widest_frame // 2)

    def _load_clips(
        self,
        animation_configs: dict[str, dict[str, Any]],
    ) -> dict[str, AnimationClip]:
        """Load all configured animations into memory."""
        prepared_frames = _load_prepared_animation_frames(animation_configs)
        consistent_scale_factor = _get_consistent_scale_factor(
            prepared_frames,
            animation_configs,
        )

        clips: dict[str, AnimationClip] = {}
        for animation_name, prepared in prepared_frames.items():
            config = animation_configs[animation_name]
            scale_factor = (
                consistent_scale_factor
                if _uses_consistent_scale(config)
                else None
            )
            frames = build_fixed_canvas_frames(
                prepared_frames=prepared,
                canvas_size=_read_canvas_size(config),
                target_height=int(config.get("target_height", 0)) or None,
                scale_mode=str(config.get("scale_mode", "visible")),
                scale_factor=scale_factor,
                smooth=bool(config.get("smooth_scale", False)),
            )
            clips[animation_name] = AnimationClip(
                frames=frames,
                frame_duration=float(config.get("frame_duration", 0.16)),
                loop=bool(config.get("loop", True)),
            )

        if not clips:
            raise ValueError("PlayerAnimationSystem requires at least one clip.")

        return clips


def _load_prepared_animation_frames(
    animation_configs: dict[str, dict[str, Any]],
) -> dict[str, PreparedAnimationFrames]:
    """Load every sprite sheet once at animation-system startup."""
    prepared_frames: dict[str, PreparedAnimationFrames] = {}
    for animation_name, config in animation_configs.items():
        image_path = Path(str(config.get("image", "")))
        if not image_path.exists():
            continue

        prepared_frames[animation_name] = cut_horizontal_sprite_sheet(
            image_path=image_path,
            frame_count=int(config["frame_count"]),
            trim_alpha=bool(config.get("trim_alpha", True)),
        )

    return prepared_frames


def load_fixed_canvas_sprite_sheet(
    image_path: Path,
    frame_count: int,
    canvas_size: tuple[int, int] = DEFAULT_CANVAS_SIZE,
    target_height: int | None = None,
    trim_alpha: bool = True,
    scale_mode: str = "visible",
    smooth: bool = False,
) -> list[pygame.Surface]:
    """Cut a horizontal sprite sheet and place frames on fixed canvases."""
    prepared_frames = cut_horizontal_sprite_sheet(
        image_path=image_path,
        frame_count=frame_count,
        trim_alpha=trim_alpha,
    )
    return build_fixed_canvas_frames(
        prepared_frames=prepared_frames,
        canvas_size=canvas_size,
        target_height=target_height,
        scale_mode=scale_mode,
        smooth=smooth,
    )


def cut_horizontal_sprite_sheet(
    image_path: Path,
    frame_count: int,
    trim_alpha: bool = True,
) -> PreparedAnimationFrames:
    """Cut one horizontal sprite sheet into animation frames."""
    sheet = _load_image(image_path)
    sheet_width, sheet_height = sheet.get_size()
    if frame_count <= 0:
        raise ValueError(f"Invalid frame count for {image_path}: {frame_count}")
    if sheet_width % frame_count != 0:
        raise ValueError(
            f"Sprite sheet width must divide by frame count: {image_path}"
        )

    frame_width = sheet_width // frame_count
    frame_height = sheet_height

    raw_frames = [
        sheet.subsurface(
            pygame.Rect(index * frame_width, 0, frame_width, frame_height)
        ).copy()
        for index in range(frame_count)
    ]
    visible_frames = [
        _trim_transparent_pixels(frame) if trim_alpha else frame
        for frame in raw_frames
    ]

    return PreparedAnimationFrames(
        visible_frames=visible_frames,
        source_frame_size=(frame_width, frame_height),
    )


def build_fixed_canvas_frames(
    prepared_frames: PreparedAnimationFrames,
    canvas_size: tuple[int, int] = DEFAULT_CANVAS_SIZE,
    target_height: int | None = None,
    scale_mode: str = "visible",
    scale_factor: float | None = None,
    smooth: bool = False,
) -> list[pygame.Surface]:
    """Scale prepared frames and place each on a transparent fixed canvas."""
    if scale_factor is None:
        scale_factor = _get_scale_factor(
            visible_frames=prepared_frames.visible_frames,
            source_frame_size=prepared_frames.source_frame_size,
            scale_mode=scale_mode,
            target_height=target_height,
            canvas_size=canvas_size,
        )

    return [
        _place_on_fixed_canvas(
            surface=_scale_uniform(frame, scale_factor, smooth=smooth),
            canvas_size=canvas_size,
        )
        for frame in prepared_frames.visible_frames
    ]


def _uses_consistent_scale(config: dict[str, Any]) -> bool:
    """Return whether this animation should share one character-wide scale."""
    return str(config.get("scale_mode", "")).lower() == "consistent"


def _get_consistent_scale_factor(
    prepared_frames: dict[str, PreparedAnimationFrames],
    animation_configs: dict[str, dict[str, Any]],
) -> float | None:
    """Return one scale factor shared by all consistent animation clips."""
    visible_frames: list[pygame.Surface] = []
    source_frame_size = (1, 1)
    target_height: int | None = None
    canvas_size = DEFAULT_CANVAS_SIZE

    for animation_name, frames in prepared_frames.items():
        config = animation_configs[animation_name]
        if not _uses_consistent_scale(config):
            continue

        visible_frames.extend(frames.visible_frames)
        source_frame_size = frames.source_frame_size
        if target_height is None:
            target_height = int(config.get("target_height", 0)) or None
        canvas_size = _read_canvas_size(config)

    if not visible_frames:
        return None

    return _get_scale_factor(
        visible_frames=visible_frames,
        source_frame_size=source_frame_size,
        scale_mode="visible",
        target_height=target_height,
        canvas_size=canvas_size,
    )


def _read_canvas_size(config: dict[str, Any]) -> tuple[int, int]:
    """Return fixed canvas size from config."""
    canvas_size = config.get("canvas_size", DEFAULT_CANVAS_SIZE)
    if not isinstance(canvas_size, list) or len(canvas_size) != 2:
        return DEFAULT_CANVAS_SIZE

    return int(canvas_size[0]), int(canvas_size[1])


def _load_image(image_path: Path) -> pygame.Surface:
    """Load an image, using alpha conversion when a display exists."""
    image = pygame.image.load(str(image_path))
    try:
        return image.convert_alpha()
    except pygame.error:
        return image


def _trim_transparent_pixels(surface: pygame.Surface) -> pygame.Surface:
    """Remove transparent padding from one frame."""
    bounding_rect = surface.get_bounding_rect(min_alpha=1)
    if bounding_rect.width == 0 or bounding_rect.height == 0:
        return surface

    return surface.subsurface(bounding_rect).copy()


def _get_scale_factor(
    visible_frames: list[pygame.Surface],
    source_frame_size: tuple[int, int],
    scale_mode: str,
    target_height: int | None,
    canvas_size: tuple[int, int],
) -> float:
    """Return one uniform scale factor for all frames in a clip."""
    if scale_mode.lower() == "consistent":
        max_width, max_height = source_frame_size
    else:
        max_width = max((frame.get_width() for frame in visible_frames), default=1)
        max_height = max((frame.get_height() for frame in visible_frames), default=1)

    if target_height is None:
        target_factor = 1.0
    else:
        target_factor = target_height / max_height

    fit_factor = min(canvas_size[0] / max_width, canvas_size[1] / max_height)
    return min(target_factor, fit_factor)


def _scale_uniform(
    surface: pygame.Surface,
    scale_factor: float,
    smooth: bool,
) -> pygame.Surface:
    """Scale one frame without distorting aspect ratio."""
    if scale_factor == 1.0:
        return surface

    target_size = (
        max(1, round(surface.get_width() * scale_factor)),
        max(1, round(surface.get_height() * scale_factor)),
    )
    if smooth:
        return pygame.transform.smoothscale(surface, target_size)

    return pygame.transform.scale(surface, target_size)


def _place_on_fixed_canvas(
    surface: pygame.Surface,
    canvas_size: tuple[int, int],
) -> pygame.Surface:
    """Place one frame on a transparent canvas using a midbottom baseline."""
    canvas = pygame.Surface(canvas_size, pygame.SRCALPHA)
    frame_rect = surface.get_rect(midbottom=(canvas_size[0] // 2, canvas_size[1]))
    canvas.blit(surface, frame_rect)
    return canvas
