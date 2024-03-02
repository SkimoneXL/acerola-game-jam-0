from enum import Enum, IntEnum, StrEnum, auto, unique
from pygame.font import Font


@unique
class SceneRegistry(IntEnum):
    __order__ = "MAIN_MENU SCHOOL_1 DREAM_1 SCHOOL_2 DREAM_2"
    MAIN_MENU = auto()
    SCHOOL_1 = auto()
    DREAM_1 = auto()
    SCHOOL_2 = auto()
    DREAM_2 = auto()


@unique
class FontRegistry(StrEnum):
    SILVER: str = 'game/assets/fonts/Silver.ttf'

    @staticmethod
    def get(font_name: str, size: int = 20):
        return Font(font_name, size=size)
