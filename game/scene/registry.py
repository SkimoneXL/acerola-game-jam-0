from enum import IntEnum, unique
from aenum import NoAlias, StrEnum

from pygame.font import Font


class AnimationPath(StrEnum):
    _settings_ = NoAlias

    IDLE_RIGHT = 'game/assets/animations/player Idle 48x48.png'
    IDLE_LEFT = 'game/assets/animations/player Idle 48x48.png'
    RUN_RIGHT = 'game/assets/animations/player run 48x48.png'
    RUN_LEFT = 'game/assets/animations/player run 48x48.png'
    JUMP_RIGHT = 'game/assets/animations/player jump 48x48.png'
    JUMP_LEFT = 'game/assets/animations/player jump 48x48.png'
    AIR_SPIN_RIGHT = 'game/assets/animations/player air spin 48x48.png'
    AIR_SPIN_LEFT = 'game/assets/animations/player air spin 48x48.png'
    WALL_SLIDE_RIGHT = 'game/assets/animations/player wall slide 48x48.png'
    WALL_SLIDE_LEFT = 'game/assets/animations/player wall slide 48x48.png'


@unique
class FontPath(StrEnum):
    SILVER: str = 'game/assets/fonts/Silver.ttf'

    @staticmethod
    def get(font_name: str, size: int = 20):
        return Font(font_name, size=size)


@unique
class SceneIndex(IntEnum):
    MAIN_MENU = -1
    SCHOOL_1 = 0
    DREAM_1 = 1
    SCHOOL_2 = 2
    DREAM_2 = 3


@unique
class ScriptPath(StrEnum):
    """
    Probably never going to be translated,
    but it's easy enough to program it this way
    """
    ENGLISH: str = 'game/assets/text/en/script.json'


@unique
class TileMapPath(StrEnum):
    SCHOOL_1 = 'game/assets/tilemaps/school_1.json'
    DREAM_1 = 'game/assets/tilemaps/dream_1.json'
    SCHOOL_2 = 'game/assets/tilemaps/school_2.json'
    DREAM_2 = 'game/assets/tilemaps/dream_2.json'
