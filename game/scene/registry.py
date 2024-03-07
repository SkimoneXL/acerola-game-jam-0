from enum import IntEnum, StrEnum, unique

from pygame.font import Font


@unique
class SceneRegistry(IntEnum):
    MAIN_MENU = -1
    SCHOOL_1 = 0
    DREAM_1 = 1
    SCHOOL_2 = 2
    DREAM_2 = 3


@unique
class TileMapRegistry(StrEnum):
    SCHOOL_1 = 'game/assets/tilemaps/school_1.json'
    DREAM_1 = 'game/assets/tilemaps/dream_1.json'
    SCHOOL_2 = 'game/assets/tilemaps/school_2.json'
    DREAM_2 = 'game/assets/tilemaps/dream_2.json'


@unique
class FontRegistry(StrEnum):
    SILVER: str = 'game/assets/fonts/Silver.ttf'

    @staticmethod
    def get(font_name: str, size: int = 20):
        return Font(font_name, size=size)


@unique
class TextRegistry(StrEnum):
    """
    Probably never going to be translated,
    but it's easy enough to program it this way
    """
    ENGLISH: str = 'game/assets/text/en/script.json'
