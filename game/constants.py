from enum import IntEnum

import pygame


class UserEvent(IntEnum):
    SCENE_CHANGE = pygame.USEREVENT + 1
