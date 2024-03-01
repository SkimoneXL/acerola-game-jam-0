from enum import IntEnum, auto, unique


@unique
class SceneRegistry(IntEnum):
    __order__ = "MAIN_MENU LEVEL_1"
    MAIN_MENU = auto()
    LEVEL_1 = auto()
