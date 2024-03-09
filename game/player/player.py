import pygame
from attr import define
from pygame import Surface
from pygame.sprite import Sprite

from game.player.physics import PhysicsState
from game.scene.levels.tiling import TileMap


@define
class Player(Sprite):
    image: Sprite
    physics: PhysicsState

    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((10, 20))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.physics = PhysicsState()
        self.last_keyup = 0
        self.jump_counter = 0
        self.can_jump = True

    @property
    def position(self):
        return self.physics.pos.xy

    def update(self):
        self.handle_held_keys()
        self.physics.update()
        self.rect.update(*self.position, self.rect.width, self.rect.height)
        self.update_jump_state()

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
                self.physics.lateral_stop()
                self.last_keyup = pygame.K_a
            elif event.key == pygame.K_d:
                self.physics.lateral_stop()
                self.last_keyup = pygame.K_d
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()
        else:
            self.physics.handle_event(event)

    def jump(self):
        if self.can_jump:
            self.physics.jump()
            self.can_jump = False
            self.jump_counter += 1

    def update_jump_state(self):
        blocked = self.physics.blocked
        self.can_jump = blocked.east or blocked.west or blocked.south or self.jump_counter < 1
        self.jump_counter = 0 if self.jump_counter >= 2 else self.jump_counter
        self.physics.blocked.set_all_false()
