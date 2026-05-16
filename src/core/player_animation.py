"""Player animation loading, validation, and playback."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pygame


DEFAULT_CANVAS_SIZE = (256, 256)


@dataclass(frozen=True)
class AnimationDefinition:
    """Data-driven animation config loaded from JSON."""

    name: str
    image_path: Path
    frame_count: int
    frame_duration: float
    loop: bool
    priority: int
    interruptible: bool
    canvas_size: tuple[int, int]
    target_height: int | None
    trim_alpha: bool
    scale_mode: str
    smooth_scale: bool
    hit_frame: int | None = None


@dataclass
class AnimationClip:
    """Cached frames and playback settings for one animation."""

    definition: AnimationDefinition
    frames: list[pygame.Surface]


@dataclass
class PreparedAnimationFrames:
    """Cut frames prepared for final scaling and canvas placement."""

    definition: AnimationDefinition
    visible_frames: list[pygame.Surface]
    source_frame_size: tuple[int, int]


class PlayerAnimationSystem:
    """Load player sprite sheets once and play cached frames."""

    def __init__(
        self,
        animation_configs: dict[str, dict[str, Any]],
        default_animation: str = "idle",
    ) -> None:
        self.definitions = _load_animation_definitions(animation_configs)
        self.clips = self._load_clips()
        if default_animation not in self.clips:
            default_animation = next(iter(self.clips))

        self.current_name = default_animation
        self.current_frame_index = 0
        self.animation_timer = 0.0

    def set_animation(self, animation_name: str, restart: bool = False) -> None:
        """Switch animation while preserving cached frames."""
        if animation_name not in self.clips:
            animation_name = "idle"

        if animation_name == self.current_name and not restart:
            return

        self.current_name = animation_name
        self.current_frame_index = 0
        self.animation_timer = 0.0

    def has_animation(self, animation_name: str) -> bool:
        """Return whether a clip exists for the animation name."""
        return animation_name in self.clips

    def update(self, delta_time: float) -> None:
        """Advance the current animation."""
        clip = self.clips[self.current_name]
        if len(clip.frames) <= 1:
            return

        self.animation_timer += delta_time
        frame_duration = max(0.01, clip.definition.frame_duration)
        while self.animation_timer >= frame_duration:
            self.animation_timer -= frame_duration
            if clip.definition.loop:
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
        return self.clips[self.current_name].frames[self.current_frame_index]

    def get_current_clip(self) -> AnimationClip:
        """Return current animation clip."""
        return self.clips[self.current_name]

    def get_definition(self, animation_name: str) -> AnimationDefinition:
        """Return one animation definition."""
        return self.clips[animation_name].definition

    def get_current_half_width(self) -> int:
        """Return half of the current animation's widest visible frame."""
        clip = self.clips[self.current_name]
        widest_frame = max(
            frame.get_bounding_rect(min_alpha=1).width for frame in clip.frames
        )
        return max(1, widest_frame // 2)

    def is_current_finished(self) -> bool:
        """Return whether the current non-looping clip reached its final frame."""
        clip = self.clips[self.current_name]
        return (
            not clip.definition.loop
            and self.current_frame_index >= len(clip.frames) - 1
        )

    def is_hit_frame_reached(self) -> bool:
        """Return whether current animation reached its configured hit frame."""
        hit_frame = self.get_current_clip().definition.hit_frame
        return hit_frame is not None and self.current_frame_index >= hit_frame

    def _load_clips(self) -> dict[str, AnimationClip]:
        """Load all configured animations into memory."""
        prepared_frames = {
            name: cut_horizontal_sprite_sheet(definition)
            for name, definition in self.definitions.items()
        }
        consistent_scale_factor = _get_consistent_scale_factor(prepared_frames)

        clips: dict[str, AnimationClip] = {}
        for animation_name, prepared in prepared_frames.items():
            scale_factor = (
                consistent_scale_factor
                if _uses_consistent_scale(prepared.definition)
                else None
            )
            frames = build_fixed_canvas_frames(
                prepared_frames=prepared,
                scale_factor=scale_factor,
            )
            clips[animation_name] = AnimationClip(
                definition=prepared.definition,
                frames=frames,
            )

        if not clips:
            raise ValueError("PlayerAnimationSystem requires at least one clip.")

        return clips


def _load_animation_definitions(
    animation_configs: dict[str, dict[str, Any]],
) -> dict[str, AnimationDefinition]:
    """Convert raw JSON animation config to typed definitions."""
    definitions: dict[str, AnimationDefinition] = {}
    for animation_name, config in animation_configs.items():
        if not isinstance(config, dict):
            continue

        path_text = str(config.get("path") or config.get("image") or "")
        if not path_text:
            raise ValueError(f"Animation '{animation_name}' is missing file path.")

        image_path = Path(path_text)
        if not image_path.is_file():
            raise FileNotFoundError(
                f"Animation '{animation_name}' file not found: {image_path}"
            )

        frame_count = int(config["frame_count"])
        frame_duration = _read_frame_duration(config)
        definitions[animation_name] = AnimationDefinition(
            name=animation_name,
            image_path=image_path,
            frame_count=frame_count,
            frame_duration=frame_duration,
            loop=bool(config.get("loop", True)),
            priority=int(config.get("priority", 0)),
            interruptible=bool(config.get("interruptible", True)),
            canvas_size=_read_canvas_size(config),
            target_height=_read_optional_int(config, "target_height"),
            trim_alpha=bool(config.get("trim_alpha", True)),
            scale_mode=str(config.get("scale_mode", "visible")),
            smooth_scale=bool(config.get("smooth_scale", False)),
            hit_frame=_read_optional_int(config, "hit_frame"),
        )

    return definitions


def _read_frame_duration(config: dict[str, Any]) -> float:
    """Read frame duration from either frame_duration or fps."""
    if "fps" in config:
        fps = float(config["fps"])
        if fps <= 0:
            raise ValueError(f"Invalid animation fps: {fps}")
        return 1.0 / fps

    return float(config.get("frame_duration", 0.12))


def _read_optional_int(config: dict[str, Any], key: str) -> int | None:
    """Read an optional integer config value."""
    value = config.get(key)
    if value is None:
        return None

    return int(value)


def cut_horizontal_sprite_sheet(
    definition: AnimationDefinition,
) -> PreparedAnimationFrames:
    """Cut one horizontal sprite sheet into animation frames."""
    sheet = _load_image(definition.image_path)
    sheet_width, sheet_height = sheet.get_size()
    if definition.frame_count <= 0:
        raise ValueError(
            f"Animation '{definition.name}' has invalid frame_count="
            f"{definition.frame_count}."
        )
    if sheet_width % definition.frame_count != 0:
        raise ValueError(
            "Invalid sprite sheet frame config: "
            f"animation='{definition.name}', "
            f"path='{definition.image_path}', "
            f"sheet_width={sheet_width}, "
            f"frame_count={definition.frame_count}. "
            "Reason: sheet_width không chia hết cho frame_count."
        )

    frame_width = sheet_width // definition.frame_count
    frame_height = sheet_height
    raw_frames = [
        sheet.subsurface(
            pygame.Rect(index * frame_width, 0, frame_width, frame_height)
        ).copy()
        for index in range(definition.frame_count)
    ]
    visible_frames = [
        _trim_transparent_pixels(frame) if definition.trim_alpha else frame
        for frame in raw_frames
    ]

    return PreparedAnimationFrames(
        definition=definition,
        visible_frames=visible_frames,
        source_frame_size=(frame_width, frame_height),
    )


def build_fixed_canvas_frames(
    prepared_frames: PreparedAnimationFrames,
    scale_factor: float | None = None,
) -> list[pygame.Surface]:
    """Scale prepared frames and place each on a transparent fixed canvas."""
    definition = prepared_frames.definition
    if scale_factor is None:
        scale_factor = _get_scale_factor(
            visible_frames=prepared_frames.visible_frames,
            source_frame_size=prepared_frames.source_frame_size,
            scale_mode=definition.scale_mode,
            target_height=definition.target_height,
            canvas_size=definition.canvas_size,
        )

    return [
        _place_on_fixed_canvas(
            surface=_scale_uniform(
                frame,
                scale_factor,
                smooth=definition.smooth_scale,
            ),
            canvas_size=definition.canvas_size,
        )
        for frame in prepared_frames.visible_frames
    ]


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


def _uses_consistent_scale(definition: AnimationDefinition) -> bool:
    """Return whether this animation should share one character-wide scale."""
    return definition.scale_mode.lower() == "consistent"


def _get_consistent_scale_factor(
    prepared_frames: dict[str, PreparedAnimationFrames],
) -> float | None:
    """Return one scale factor shared by all consistent animation clips."""
    visible_frames: list[pygame.Surface] = []
    source_frame_size = (1, 1)
    target_height: int | None = None
    canvas_size = DEFAULT_CANVAS_SIZE

    for frames in prepared_frames.values():
        if not _uses_consistent_scale(frames.definition):
            continue

        visible_frames.extend(frames.visible_frames)
        source_frame_size = frames.source_frame_size
        if target_height is None:
            target_height = frames.definition.target_height
        canvas_size = frames.definition.canvas_size

    if not visible_frames:
        return None

    return _get_scale_factor(
        visible_frames=visible_frames,
        source_frame_size=source_frame_size,
        scale_mode="visible",
        target_height=target_height,
        canvas_size=canvas_size,
    )


def _get_scale_factor(
    visible_frames: list[pygame.Surface],
    source_frame_size: tuple[int, int],
    scale_mode: str,
    target_height: int | None,
    canvas_size: tuple[int, int],
) -> float:
    """Return one uniform scale factor for all frames in a clip."""
    if scale_mode.lower() == "source":
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
