from attr import define
from pygame import Surface
from pygame.event import Event

from game.constants import UserEvent
from game.scene.levels.tiling import Tile, TileSet
from game.scene.registry import AnimationPath
from game.timing import FixedUpdate


@define(kw_only=True, slots=True)
class Animation:
    frame_set: TileSet
    frame_data: list[Tile]
    current_frame: int = 0
    loop: bool = False
    flipped: bool = False

    @staticmethod
    def create(filename: AnimationPath, loop: bool = False, flipped: bool = False):
        tileset = TileSet.player(filename, flipped=flipped)
        frame_data = [tileset.tiles[i] for _ in range(2)
                      for i, _ in enumerate(tileset.tiles)]  # animate on 2s
        #TODO: Control total time of animation

        return Animation(
            frame_set=tileset,
            frame_data=frame_data,
            current_frame=0,
            loop=loop,
            flipped=flipped,
        )

    @property
    def current_image(self) -> Surface:
        return self.frame_data[self.current_frame].image

    def update(self) -> None:
        if self.loop:
            self.current_frame = (self.current_frame + 1) % len(self.frame_data)
        else:
            self.current_frame = min(self.current_frame + 1, len(self.frame_data) - 1)


@define(kw_only=True, slots=True)
class AnimationState:
    animations: list[Animation]
    fixed_animation: FixedUpdate
    current_animation: int = 0
    flipped: bool = False

    @staticmethod
    def player(fps: int = 24):
        animations = [
            Animation.create(AnimationPath.IDLE_RIGHT, loop=True),
            Animation.create(AnimationPath.IDLE_LEFT, loop=True, flipped=True),
            Animation.create(AnimationPath.RUN_RIGHT, loop=True),
            Animation.create(AnimationPath.RUN_LEFT, loop=True, flipped=True),
            Animation.create(AnimationPath.JUMP_RIGHT, loop=False),
            Animation.create(AnimationPath.JUMP_LEFT, loop=False, flipped=True),
            Animation.create(AnimationPath.AIR_SPIN_RIGHT, loop=True),
            Animation.create(AnimationPath.AIR_SPIN_LEFT, loop=True, flipped=True),
            Animation.create(AnimationPath.WALL_SLIDE_RIGHT, loop=True),
            Animation.create(AnimationPath.WALL_SLIDE_LEFT, loop=True, flipped=True),
        ]
        return AnimationState(
            animations=animations,
            fixed_animation=FixedUpdate.create(
                event_type=UserEvent.FIXED_ANIMATION_UPDATE,
                updates_per_second=fps,
            ),
            current_animation=0,
        )

    @property
    def current_image(self):
        return self.animations[self.current_animation].current_image

    @property
    def jump(self) -> AnimationPath:
        if self.animations[self.current_animation].flipped:
            return AnimationPath.JUMP_LEFT
        return AnimationPath.JUMP_RIGHT

    @property
    def idle(self) -> AnimationPath:
        if self.animations[self.current_animation].flipped:
            return AnimationPath.IDLE_LEFT
        return AnimationPath.IDLE_RIGHT

    @property
    def air_spin(self) -> AnimationPath:
        if self.animations[self.current_animation].flipped:
            return AnimationPath.AIR_SPIN_LEFT
        return AnimationPath.AIR_SPIN_RIGHT

    def set(self, new_path: AnimationPath):
        for i, path in enumerate(AnimationPath):
            if path.name == new_path.name:
                self.current_animation = i
                return

    def handle_event(self, event: Event) -> None:
        if event.type == UserEvent.FIXED_ANIMATION_UPDATE:
            self.animations[self.current_animation].update()

    def update(self):
        self.fixed_animation.update()
