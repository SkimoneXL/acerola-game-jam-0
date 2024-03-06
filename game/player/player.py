from attr import define
from pygame import Rect, Surface
import pygame
from pygame.sprite import Sprite
from game.player.physics import State


@define
class Player(Sprite):
    image: Sprite
    physics: State

    def __init__(
            self,
            image=None,
            physics=State(),
    ):
        Sprite.__init__(self)
        self.image = Surface((10, 20))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.physics = physics
        self.last_keyup = 0

    @property
    def position(self):
        return self.physics.pos.xy

    def update(self):
        self.handle_held_keys()
        self.physics.update()
        self.rect.update(*self.position, self.rect.width, self.rect.height)

    def handle_held_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and keys[pygame.K_d]:
            if self.last_keyup == pygame.K_a:
                self.physics.move_left()
            elif self.last_keyup == pygame.K_d:
                self.physics.move_right()
        elif keys[pygame.K_a]:
            self.physics.move_left()
        elif keys[pygame.K_d]:
            self.physics.move_right()

    def render(self, surface: Surface):
        surface.blit(self.image, self.position)

    def handle_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.physics.stop_movement()
                self.last_keyup = pygame.K_a
            elif event.key == pygame.K_d:
                self.physics.stop_movement()
                self.last_keyup = pygame.K_d
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.physics.jump()
        else:
            self.physics.handle_event(event)
