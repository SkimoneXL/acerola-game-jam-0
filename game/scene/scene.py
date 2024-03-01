from abc import ABC, abstractmethod
from pygame import Surface


class Scene(ABC):

    @abstractmethod
    def render(self, surface: Surface):
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def get_next_scene(self):
        ...

    @abstractmethod
    def handle_event(self, event):
        ...
