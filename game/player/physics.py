import numpy as np
from attr import define
from pygame import Rect
from pygame.event import Event, post

from game.constants import UserEvent
from game.timing import FixedUpdate


@define(slots=True)
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


@define(slots=True)
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


@define(kw_only=True, slots=True)
class PhysicsState:
    pos: Vec2 = Vec2(0.0, 0.0)
    vel: Vec2 = Vec2(0.0, 0.0)
    force: Vec2 = Vec2(0.0, 0.0)
    mass: float = 1.0
    speed: float = 0.15
    gravity: float = 0.003
    jump_speed: float = 0.8
    fixed_physics: FixedUpdate = FixedUpdate.create(
        event_type=UserEvent.FIXED_PHYSICS_UPDATE,
        updates_per_second=240,
    )
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
        self.vel.y -= self.jump_speed
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
            post(Event(UserEvent.PLAYER_LAND))

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


def euler(state: PhysicsState, time: float):
    state.pos.data += state.vel.data * time
    state.vel.data += (state.force.data / state.mass) * time
