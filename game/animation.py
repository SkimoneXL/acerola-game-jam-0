from attr import define
from pygame import Surface
from game.constants import UserEvent
from game.scene.levels.tiling import Tile, TileSet
from pygame.event import Event

from game.timing import FixedUpdate


@define(kw_only=True)
class Animation:
    frames: TileSet
    current_frame: int = 0
    fixed_animation: FixedUpdate = FixedUpdate

    def handle_event(self, event: Event):
        if event.type == UserEvent.FIXED_ANIMATION_UPDATE:
            ...

    def update(self):
        self.fixed_animation.update()

    def render(self, surface: Surface):
        ...
