from abc import ABC, abstractmethod
from typing import Literal

from attr import define
from pygame import Surface

from game.player.player import Player
from game.scene.registry import SceneIndex


@define
class Scene(ABC):

    player: Player

    @abstractmethod
    def render(self, surface: Surface):
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def get_next_scene(self) -> SceneIndex:
        ...

    @abstractmethod
    def handle_event(self, event):
        ...
