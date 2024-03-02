from pygame import Surface
import pygame
from game.scene.registry import SceneRegistry
from game.scene.scene import Scene
from pygame.font import Font
from pygame.event import Event, post
from game.constants import UserEvent


class MainMenu(Scene):

    def render(self, surface: Surface):
        font = Font('game/assets/fonts/Silver.ttf', 50)
        text: Surface = font.render('Main Menu', True, (100, 200, 100))
        text_rect = text.get_rect()
        text_rect.center = (500, 500)
        surface.blit(text, text_rect)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            post(Event(UserEvent.SCENE_CHANGE))

    def get_next_scene(self):
        return SceneRegistry.SCHOOL_1

    def handle_event(self, event):
        ...
