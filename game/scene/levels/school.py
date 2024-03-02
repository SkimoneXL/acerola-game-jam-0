from pygame import Surface
import pygame
from game.scene.registry import FontRegistry, SceneRegistry
from game.scene.scene import Scene
from pygame.font import Font
from game.scene.textutils import ScrolledText


class School_1(Scene):

    def __init__(self):
        self.scroll_text = ScrolledText(
            text='School 1',
            font=FontRegistry.get(FontRegistry.SILVER, 50),
            color=(0, 0, 0),
            position=(400, 400),
        )

    def render(self, surface: Surface):
        self.scroll_text.render(surface)

    def update(self):
        self.scroll_text.update()
        keys = pygame.key.get_pressed()

    def get_next_scene(self):
        return SceneRegistry.DREAM_1

    def handle_event(self, event):
        ...


class School_2(Scene):

    def render(self, surface: Surface):
        font = Font()
        text: Surface = font.render('School 2', True, (100, 200, 100))
        text_rect = text.get_rect()
        text_rect.center = (500, 500)
        surface.blit(text, text_rect)

    def update(self):
        keys = pygame.key.get_pressed()

    def get_next_scene(self):
        return SceneRegistry.DREAM_2

    def handle_event(self, event):
        ...
