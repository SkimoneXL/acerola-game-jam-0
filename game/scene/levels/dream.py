import pygame
from pygame import Surface

from game.player.player import Player
from game.scene.registry import SceneRegistry
from game.scene.scene import Scene
from game.scene.textutils import TextGUI


class Dream_1(Scene):

    def __init__(self, player: Player):
        super().__init__(player)
        self.gui = TextGUI.create(SceneRegistry.DREAM_1)

    def render(self, surface: Surface):
        self.player.render(surface)
        self.gui.render(surface)

    def update(self):
        self.player.update()
        self.gui.update()
        keys = pygame.key.get_pressed()

    def get_next_scene(self):
        return SceneRegistry.SCHOOL_2

    def handle_event(self, event):
        self.player.handle_event(event)


class Dream_2(Scene):

    def __init__(self, player: Player):
        super().__init__(player)
        self.gui = TextGUI.create(SceneRegistry.DREAM_2)

    def render(self, surface: Surface):
        self.player.render(surface)
        self.gui.render(surface)

    def update(self):
        self.player.update()
        self.gui.update()
        keys = pygame.key.get_pressed()

    def get_next_scene(self):
        return SceneRegistry.MAIN_MENU

    def handle_event(self, event):
        self.player.handle_event(event)
