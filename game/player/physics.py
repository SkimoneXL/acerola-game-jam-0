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


@define(kw_only=True)
class State:
    pos: Vec2 = Vec2(0.0, 0.0)
    vel: Vec2 = Vec2(0.0, 0.0)
    force: Vec2 = Vec2(0.0, 0.0)
    mass: float = 1.0
    speed: float = 1.0
    gravity: float = 0.01
    jump_speed: float = 2.0
    fixed_physics = FixedPhysics.default()

    def update(self):
        self.fixed_physics.update()

    def handle_event(self, event):
        if event.type == UserEvent.FIXED_PHYSICS_UPDATE:
            self.force.y = self.mass * self.gravity
            self.step(event.dict['time'])

    def step(self, time):
        Physics.euler(self, time)

    def move_left(self):
        self.vel.x = -self.speed

    def move_right(self):
        self.vel.x = self.speed

    def lateral_stop(self):
        self.vel.x = 0.0

    def vertical_stop(self):
        self.vel.y = 0.0

    def jump(self):
        self.vel.y = -self.jump_speed

    def detect_collision(self, player: Rect, rect: Rect) -> bool:
        # North
        if rect.collidepoint(player.midtop):
            #self.vertical_stop()
            self.snap_downward(player, rect)

        # South
        if rect.collidepoint(player.midbottom):
            #self.vertical_stop()
            self.snap_upward(player, rect)

        # East
        if rect.collidepoint(player.midright):
            self.lateral_stop()
            self.snap_left(player, rect)

        # West
        if rect.collidepoint(player.midleft):
            self.lateral_stop()
            self.snap_right(player, rect)

    def snap_upward(self, player: Rect, rect: Rect):
        self.pos.y = (player.bottom // rect.height) * rect.height - player.height

    def snap_downward(self, player: Rect, rect: Rect):
        self.pos.y = (player.top // rect.height) * rect.height + player.height

    def snap_left(self, player: Rect, rect: Rect):
        self.pos.x = (player.right // rect.width) * rect.width - player.width

    def snap_right(self, player: Rect, rect: Rect):
        self.pos.x = (player.left // rect.width) * rect.width + player.width


@define
class Physics:

    @staticmethod
    def euler(state: State, time: float):
        state.pos.data += state.vel.data * time
        state.vel.data += (state.force.data / state.mass) * time

    @staticmethod
    def midpoint(state: State, time: float):
        ...
