from enum import IntEnum

import pygame


class UserEvent(IntEnum):
    SCENE_CHANGE = pygame.USEREVENT + 1
    FIXED_PHYSICS_UPDATE = pygame.USEREVENT + 2
    FIXED_ANIMATION_UPDATE = pygame.USEREVENT + 3
    FIXED_TEXT_UPDATE = pygame.USEREVENT + 4
    PLAYER_LAND = pygame.USEREVENT + 5
