import pygame
from pygame import Surface
from pygame.event import Event, post
from pygame.font import Font

from game.constants import UserEvent
from game.player.player import Player
from game.scene.registry import SceneRegistry
from game.scene.scene import Scene


class MainMenu(Scene):

    def __init__(self, player: Player):
        super().__init__(player)

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
