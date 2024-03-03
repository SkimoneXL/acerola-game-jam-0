from pygame.event import Event, post
from game import game_clock
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

    @property
    def y(self):
        return self.data[1]

    @property
    def xy(self):
        return self.x, self.y

    def __mul__(self, other):
        return self.data * other.data

    def __imul__(self, other):
        self.data *= other.data
        return self

    def __add__(self, other):
        return self.data + other.data

    def __iadd__(self, other):
        self.data += other.data
        return self

    def __sub__(self, other):
        return self.data - other.data

    def __isub__(self, other):
        self.data -= other.data
        return self

    def __div__(self, other):
        return self.data / other.data

    def __idiv__(self, other):
        self.data /= other.data
        return self


@define(kw_only=True)
class FixedPhysics:
    updates_per_second = 60
    fixed_update_timer = Timer(duration=1 / updates_per_second)
    fixed_update_func = lambda: ...

    def update(self):
        self.fixed_update_timer.update()
        if self.fixed_update_timer.done:
            post(Event(UserEvent.FIXED_PHYSICS_UPDATE))
            self.fixed_update_timer.reset()


@define(kw_only=True)
class State:
    pos: Vec2 = Vec2(0, 0)
    vel: Vec2 = Vec2(0, 0)
    acc: Vec2 = Vec2(0, 0)
    speed: int = 1
    fixed_physics = FixedPhysics()

    def update(self):
        self.fixed_physics.update()

    def step(self):
        Physics.euler(self, game_clock.get_time())

    def add_force(self, force: Vec2):
        self.acc.data += force.data

    def move_left(self):
        self.vel = Vec2(-self.speed, 0)

    def move_right(self):
        self.vel = Vec2(self.speed, 0)


@define
class Physics:

    @staticmethod
    def euler(state: State, time: float):
        state.pos += state.vel.data * time
        state.vel += state.acc.data * time

    @staticmethod
    def midpoint(self):
        ...
