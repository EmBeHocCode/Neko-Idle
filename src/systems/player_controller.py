"""Player state, movement, and action priority controller."""

from dataclasses import dataclass

from src.core.player_animation import PlayerAnimationSystem


STATE_DEATH = "death"
STATE_HURT = "hurt"
STATE_ATTACK = "attack"
STATE_DASH = "dash"
STATE_JUMP = "jump"
STATE_RUN = "run"
STATE_WALK = "walk"
STATE_IDLE = "idle"

LOCKED_STATES = {STATE_ATTACK, STATE_DASH, STATE_HURT, STATE_DEATH}


@dataclass
class PlayerMovementConfig:
    """Runtime movement values loaded from player config."""

    walk_speed: float = 360.0
    run_speed: float = 520.0
    gravity: float = 1800.0
    jump_force: float = 620.0
    dash_distance: float = 180.0
    dash_duration: float = 0.22


class PlayerController:
    """Coordinate player input, physics, and animation state priority."""

    def __init__(
        self,
        animation: PlayerAnimationSystem,
        movement_config: dict[str, float],
        x: float,
        ground_y: float,
    ) -> None:
        self.animation = animation
        self.movement = PlayerMovementConfig(**movement_config)
        self.x = x
        self.y = ground_y
        self.ground_y = ground_y
        self.direction = 1
        self.velocity_y = 0.0
        self.is_grounded = True
        self.is_jumping = False
        self.state = STATE_IDLE
        self.dash_timer = 0.0
        self.dash_speed = 0.0
        self.attack_damage_applied = False
        self.attack_hit_triggered = False

    def request_jump(self) -> None:
        """Start jump only from grounded, interruptible states."""
        if not self.is_grounded or not self._can_enter_state(STATE_JUMP):
            return

        self.state = STATE_JUMP
        self.is_grounded = False
        self.is_jumping = True
        self.velocity_y = -self.movement.jump_force
        self.animation.set_animation(STATE_JUMP, restart=True)

    def request_dash(self, move_direction: int) -> None:
        """Start grounded dodge dash if current state allows it."""
        if not self.is_grounded or not self._can_enter_state(STATE_DASH):
            return

        if move_direction != 0:
            self.direction = move_direction

        duration = max(0.01, self.movement.dash_duration)
        self.dash_timer = 0.0
        self.dash_speed = self.movement.dash_distance / duration
        self.state = STATE_DASH
        self.animation.set_animation(STATE_DASH, restart=True)

    def request_attack(self) -> None:
        """Start attack once; ignore spam until the animation finishes."""
        if not self.is_grounded or self.state == STATE_ATTACK:
            return

        if not self._can_enter_state(STATE_ATTACK):
            return

        self.state = STATE_ATTACK
        self.attack_damage_applied = False
        self.attack_hit_triggered = False
        self.animation.set_animation(STATE_ATTACK, restart=True)

    def update(
        self,
        delta_time: float,
        move_direction: int,
        run_pressed: bool,
        movement_bounds: tuple[int, int],
    ) -> None:
        """Update state, movement, physics, and animation."""
        self.attack_hit_triggered = False
        self._apply_horizontal_movement(delta_time, move_direction, run_pressed)
        self._apply_vertical_physics(delta_time)
        self._resolve_locomotion_state(move_direction, run_pressed)

        self.animation.update(delta_time)
        self._trigger_attack_hit_once()
        self._finish_completed_actions(move_direction, run_pressed)

        left_bound, right_bound = movement_bounds
        self.x = max(left_bound, min(right_bound, self.x))

    def _apply_horizontal_movement(
        self,
        delta_time: float,
        move_direction: int,
        run_pressed: bool,
    ) -> None:
        """Move player horizontally if the current state permits input."""
        if self.state == STATE_DASH:
            self.dash_timer += delta_time
            if self.dash_timer <= self.movement.dash_duration:
                self.x += self.dash_speed * self.direction * delta_time
            return

        if self.state in (STATE_ATTACK, STATE_HURT, STATE_DEATH):
            return

        if move_direction == 0:
            return

        self.direction = move_direction
        speed = self.movement.run_speed if run_pressed else self.movement.walk_speed
        self.x += speed * move_direction * delta_time

    def _apply_vertical_physics(self, delta_time: float) -> None:
        """Apply gravity while airborne and snap exactly to ground on landing."""
        if self.is_grounded:
            return

        self.velocity_y += self.movement.gravity * delta_time
        self.y += self.velocity_y * delta_time
        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.velocity_y = 0.0
            self.is_grounded = True
            self.is_jumping = False

    def _resolve_locomotion_state(self, move_direction: int, run_pressed: bool) -> None:
        """Select idle/walk/run/jump without overriding locked actions."""
        if self.state in LOCKED_STATES and not self.animation.is_current_finished():
            return

        if not self.is_grounded:
            self._set_state(STATE_JUMP)
            return

        if move_direction == 0:
            self._set_state(STATE_IDLE)
            return

        if run_pressed and self.animation.has_animation(STATE_RUN):
            self._set_state(STATE_RUN)
            return

        self._set_state(STATE_WALK)

    def _set_state(self, state: str, restart: bool = False) -> None:
        """Switch to a state animation when available."""
        if not self.animation.has_animation(state):
            state = STATE_IDLE

        self.state = state
        self.animation.set_animation(state, restart=restart)

    def _can_enter_state(self, next_state: str) -> bool:
        """Return whether next_state can interrupt current state."""
        if not self.animation.has_animation(next_state):
            return False

        current_definition = self.animation.get_definition(self.state)
        next_definition = self.animation.get_definition(next_state)
        if current_definition.interruptible:
            return True

        high_priority_forced_states = {STATE_DEATH, STATE_HURT}
        return (
            next_state in high_priority_forced_states
            and next_definition.priority > current_definition.priority
        )

    def _trigger_attack_hit_once(self) -> None:
        """Mark attack hit once per attack animation."""
        if self.state != STATE_ATTACK or self.attack_damage_applied:
            return

        if not self.animation.is_hit_frame_reached():
            return

        self.attack_damage_applied = True
        self.attack_hit_triggered = True

    def _finish_completed_actions(self, move_direction: int, run_pressed: bool) -> None:
        """Release non-looping action states after their clip finishes."""
        if self.state == STATE_DEATH:
            return

        if self.state not in LOCKED_STATES:
            return

        if self.state == STATE_DASH:
            self.dash_timer = min(self.dash_timer, self.movement.dash_duration)

        if not self.animation.is_current_finished():
            return

        self._resolve_locomotion_state(move_direction, run_pressed)
