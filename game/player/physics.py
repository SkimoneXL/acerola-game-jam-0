from pygame import Rect
from pygame.event import Event, post
from attr import define
import numpy as np
from game.constants import UserEvent

from game.timer import Timer


@define
class Vec2:
    data: np.ndarray

    def __init__(self, x, y):
        self.data = np.array([x, y])

    @property
    def x(self):
        return self.data[0]

    @x.setter
    def x(self, new_x):
        self.data[0] = new_x

    @property
    def y(self):
        return self.data[1]

    @y.setter
    def y(self, new_y):
        self.data[1] = new_y

    @property
    def xy(self):
        return int(self.x), int(self.y)


@define(frozen=True, kw_only=True)
class FixedPhysics:
    fixed_update_timer: Timer
    updates_per_second: int

    @property
    def millis_per_update(self):
        return 1000 / self.updates_per_second

    @staticmethod
    def default():
        updates_per_second = 240
        return FixedPhysics(
            fixed_update_timer=Timer(duration_millis=1000 / updates_per_second),
            updates_per_second=updates_per_second,
        )

    def update(self):
        self.fixed_update_timer.update()
        if self.fixed_update_timer.done:
            post(
                Event(
                    UserEvent.FIXED_PHYSICS_UPDATE,
                    time=self.fixed_update_timer.cumulative_millis,
                ))
            self.fixed_update_timer.reset()


@define
class BlockedState:
    north: bool = False
    south: bool = False
    east: bool = False
    west: bool = False

    def set_all_false(self):
        self.north = False
        self.south = False
        self.east = False
        self.west = False


@define(kw_only=True)
class State:
    pos: Vec2 = Vec2(0.0, 0.0)
    vel: Vec2 = Vec2(0.0, 0.0)
    force: Vec2 = Vec2(0.0, 0.0)
    mass: float = 1.0
    speed: float = 0.15
    gravity: float = 0.003
    jump_speed: float = 0.8
    fixed_physics = FixedPhysics.default()
    blocked: BlockedState = BlockedState()

    def update(self):
        self.fixed_physics.update()

    def handle_event(self, event):
        if event.type == UserEvent.FIXED_PHYSICS_UPDATE:
            self.force.y = self.mass * self.gravity
            self.step(event.dict['time'])

    def step(self, time):
        euler(self, time)

    def move_left(self):
        self.vel.x = -self.speed
        self.pos.x -= 1

    def move_right(self):
        self.vel.x = self.speed
        self.pos.x += 1

    def jump(self):
        self.vel.y = -self.jump_speed
        self.pos.y -= 1

    def lateral_stop(self):
        self.vel.x = 0.0

    def vertical_stop(self):
        self.vel.y = 0.0

    def detect_collision(self, player: Rect, rect: Rect) -> bool:

        # North
        if rect.collidepoint(player.midtop):
            self.vertical_stop()
            self.snap_downward(player, rect)
            self.blocked.north = True

        # South
        if rect.collidepoint(player.midbottom):
            self.vertical_stop()
            self.snap_upward(player, rect)
            self.blocked.south = True

        # East
        if rect.collidepoint(player.midright):
            self.lateral_stop()
            self.snap_left(player, rect)
            self.blocked.east = True

        # West
        if rect.collidepoint(player.midleft):
            self.lateral_stop()
            self.snap_right(player, rect)
            self.blocked.west = True

    def snap_upward(self, player: Rect, rect: Rect):
        self.pos.y = (player.bottom // rect.height) * rect.height - player.height

    def snap_downward(self, player: Rect, rect: Rect):
        self.pos.y = (player.top // rect.height) * rect.height + rect.height

    def snap_left(self, player: Rect, rect: Rect):
        self.pos.x = (player.right // rect.width) * rect.width - player.width

    def snap_right(self, player: Rect, rect: Rect):
        self.pos.x = (player.left // rect.width) * rect.width + rect.width


def euler(state: State, time: float):
    state.pos.data += state.vel.data * time
    state.vel.data += (state.force.data / state.mass) * time


def midpoint(state: State, time: float):
    ...
