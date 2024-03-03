from attr import define
from pygame import Surface
import pygame
from pygame.sprite import Sprite
from game.constants import UserEvent
from game.player.physics import State


@define
class Player(Sprite):
    image: Sprite
    physics: State

    def __init__(
        self,
        image=None,
        physics=None,
    ):
        Sprite.__init__(self)
        self.image = Surface((100, 200))
        self.image.fill((0, 0, 0))
        self.physics = State()

    @property
    def position(self):
        return self.physics.pos.xy

    def update(self):
        self.physics.update()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.physics.move_left()
        if keys[pygame.K_d]:
            self.physics.move_right()

    def render(self, surface: Surface):
        surface.blit(self.image, self.position)

    def handle_event(self, event):
        match (event.type):
            case (UserEvent.FIXED_PHYSICS_UPDATE):
                self.handle_input()
                self.physics.step()
