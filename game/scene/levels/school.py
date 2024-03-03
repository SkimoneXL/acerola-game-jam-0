from pygame import Surface
import pygame
from game.constants import UserEvent
from game.scene.registry import SceneRegistry
from game.scene.scene import Scene
from game.scene.textutils import TextGUI


class School_1(Scene):

    def __init__(self):
        self.gui = TextGUI.create(SceneRegistry.SCHOOL_1)

    def render(self, surface: Surface):
        self.gui.render(surface)

    def update(self):
        self.gui.update()
        keys = pygame.key.get_pressed()

    def get_next_scene(self):
        return SceneRegistry.DREAM_1

    def handle_event(self, event):
        ...


class School_2(Scene):

    def __init__(self):
        self.gui = TextGUI.create(SceneRegistry.SCHOOL_1)

    def render(self, surface: Surface):
        self.gui.render(surface)

    def update(self):
        self.gui.update()
        keys = pygame.key.get_pressed()

    def get_next_scene(self):
        return SceneRegistry.DREAM_2

    def handle_event(self, event):
        ...
