from pygame import Surface
import pygame
from game.constants import UserEvent
from game.scene.registry import SceneRegistry
from game.scene.scene import Scene
from pygame.font import Font
from pygame.event import Event, post


class Dream_1(Scene):

    def render(self, surface: Surface):
        font = Font()
        text: Surface = font.render('Dream 1', True, (100, 200, 100))
        text_rect = text.get_rect()
        text_rect.center = (500, 500)
        surface.blit(text, text_rect)

    def update(self):
        keys = pygame.key.get_pressed()

    def get_next_scene(self):
        return SceneRegistry.SCHOOL_2

    def handle_event(self, event):
        ...


class Dream_2(Scene):

    def render(self, surface: Surface):
        font = Font()
        text: Surface = font.render('Dream 2', True, (100, 200, 100))
        text_rect = text.get_rect()
        text_rect.center = (500, 500)
        surface.blit(text, text_rect)

    def update(self):
        keys = pygame.key.get_pressed()

    def get_next_scene(self):
        return SceneRegistry.MAIN_MENU

    def handle_event(self, event):
        ...
