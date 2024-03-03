from pygame import Surface
import pygame
from pygame.sprite import Sprite

from game.timer import Timer


class Player(Sprite):

    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((100, 200))
        self.image.fill((0, 0, 0))
        self.x, self.y = (20, 20)
        self.fixed_update_timer = Timer(duration=10)

    @property
    def position(self):
        return self.x, self.y

    def update(self):
        self.fixed_update_timer.update()
        if self.fixed_update_timer.done:
            self.fixed_update()
            self.fixed_update_timer.reset()

    def fixed_update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= 10
        if keys[pygame.K_RIGHT]:
            self.x += 10

    def render(self, surface: Surface):
        surface.blit(self.image, self.position)
