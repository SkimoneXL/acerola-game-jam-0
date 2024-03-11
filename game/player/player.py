import pygame
from pygame import Surface
from pygame.sprite import Sprite

from game.animation import AnimationState
from game.constants import UserEvent
from game.player.physics import PhysicsState
from game.scene.registry import AnimationPath


class Player(Sprite):

    def __init__(self):
        Sprite.__init__(self)
        self.animation = AnimationState.player()
        self.image = self.animation.current_image
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
        self.update_jump_state()
        self.image = self.animation.current_image
        self.animation.update()
        self.physics.update()
        self.rect.update(*self.position, self.rect.width, self.rect.height)
        self.update_if_idle()

    def handle_held_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and keys[pygame.K_d]:
            if self.last_keyup == pygame.K_a:
                self.move_left()
            elif self.last_keyup == pygame.K_d:
                self.move_right()
        elif keys[pygame.K_a]:
            self.move_left()
        elif keys[pygame.K_d]:
            self.move_right()

    def render(self, surface: Surface):
        surface.blit(self.image, self.position)

    def handle_event(self, event):
        match (event.type):
            case pygame.KEYUP:
                match (event.key):
                    case pygame.K_a | pygame.K_d:
                        self.physics.lateral_stop()
                        self.last_keyup = event.key
                        self.update_if_idle()
            case pygame.KEYDOWN:
                match (event.key):
                    case pygame.K_SPACE:
                        self.jump()
            case UserEvent.PLAYER_LAND:
                self.update_if_idle()
                self.jump_counter = 0
            case _:
                self.physics.handle_event(event)
                self.animation.handle_event(event)

    def update_if_idle(self):
        if self.physics.blocked.south:
            self.animation.set(self.animation.idle)

    def move_right(self):
        self.physics.move_right()
        self._set_animation_facing_right()

    def _set_animation_facing_right(self):
        if self.physics.blocked.south:
            self.animation.set(AnimationPath.RUN_RIGHT)
        elif self.jump_counter <= 1:
            self.animation.set(AnimationPath.JUMP_RIGHT)
        else:
            self.animation.set(AnimationPath.AIR_SPIN_RIGHT)

    def move_left(self):
        self.physics.move_left()
        self._set_animation_facing_left()

    def _set_animation_facing_left(self):
        if self.physics.blocked.south:
            self.animation.set(AnimationPath.RUN_LEFT)
        elif self.jump_counter <= 1:
            self.animation.set(AnimationPath.JUMP_LEFT)
        else:
            self.animation.set(AnimationPath.AIR_SPIN_LEFT)

    def jump(self):
        if self.can_jump:
            self.physics.jump()
            self.can_jump = False
            self.jump_counter += 1
            if self.jump_counter <= 1:
                self.animation.set(self.animation.jump)
            else:
                self.animation.set(self.animation.air_spin)

    def update_jump_state(self):
        blocked = self.physics.blocked
        self.can_jump = blocked.east or blocked.west or blocked.south or self.jump_counter < 2
        self.physics.blocked.set_all_false()
