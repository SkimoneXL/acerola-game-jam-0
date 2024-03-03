from pygame import Surface
import pygame
from game.scene.registry import SceneRegistry
from game.scene.scene import Scene

from game.scene.textutils import TextGUI


class Dream_1(Scene):

    def __init__(self):
        self.gui = TextGUI.create(SceneRegistry.DREAM_1)

    def render(self, surface: Surface):
        self.gui.render(surface)

    def update(self):
        self.gui.update()
        keys = pygame.key.get_pressed()

    def get_next_scene(self):
        return SceneRegistry.SCHOOL_2

    def handle_event(self, event):
        ...


class Dream_2(Scene):

    def __init__(self):
        self.gui = TextGUI.create(SceneRegistry.DREAM_2)

    def render(self, surface: Surface):
        self.gui.render(surface)

    def update(self):
        self.gui.update()
        keys = pygame.key.get_pressed()

    def get_next_scene(self):
        return SceneRegistry.MAIN_MENU

    def handle_event(self, event):
        ...
