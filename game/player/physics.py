from pygame.event import Event, post
from attr import define
import numpy as np
from game.constants import UserEvent

from game.timer import Timer


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
        return self.x, self.y


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

    def stop_movement(self):
        self.vel.x = 0

    def jump(self):
        self.vel.y = -self.jump_speed


@define
class Physics:

    @staticmethod
    def euler(state: State, time: float):
        state.pos.data += state.vel.data * time
        state.vel.data += (state.force.data / state.mass) * time

    @staticmethod
    def midpoint(state: State, time: float):
        ...
