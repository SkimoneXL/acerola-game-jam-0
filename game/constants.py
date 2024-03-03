from enum import IntEnum
import pygame


class UserEvent(IntEnum):
    SCENE_CHANGE = pygame.USEREVENT + 1
    SKIP_TEXT_THROTTLE_TIMEOUT = pygame.USEREVENT + 2
