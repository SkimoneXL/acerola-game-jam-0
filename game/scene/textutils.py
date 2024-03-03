from functools import cache
import json
from attrs import define
from typing import Any
from pygame import Surface
from pygame.font import Font
from pygame.sprite import Sprite

from game.scene.registry import FontRegistry, SceneRegistry


@define(kw_only=True)
class ScrolledText:
    text: str
    font: Font
    color: Any
    position: tuple[int, int]
    _str_buffer: str = ''
    _index: int = 0

    def update(self):
        self._str_buffer = self.text[:self._index % (len(self.text) - 1)]
        self._index += 1

    def render(self, surface: Surface):
        text_surface = self.font.render(self._str_buffer, True, self.color)
        surface.blit(text_surface, self.position)

    def done(self) -> bool:
        return self._index >= len(self.text)


@define(kw_only=True)
class Utterance:
    lines: tuple[ScrolledText, ...]
    current_line: int

    def __init__(self, lines: tuple[str], font: Font, fontsize: int):
        color = (0, 0, 0)
        x, y = (0, 0)
        self.lines = tuple(
            ScrolledText(
                text=line,
                font=font,
                color=color,
                position=(x, y + i * fontsize),
            ) for i, line in enumerate(lines))
        self.current_line = 0

    def update(self):
        self.lines[self.current_line].update()

    def render(self, surface: Surface):
        self.lines[self.current_line].render(surface)


@define(kw_only=True)
class TextGUI:
    box: Sprite
    current_utterance: int
    font: Font
    utterances: tuple[Utterance, ...]

    @staticmethod
    def create(scene: SceneRegistry):
        fontsize = 20
        font = FontRegistry.get(FontRegistry.SILVER, fontsize)

        return TextGUI(
            font=font,
            utterances=tuple(
                Utterance(lines=utterance, font=font, fontsize=fontsize)
                for utterance in parse_script(scene.value)),
            box=None,
            current_utterance=0,
        )

    def update(self):
        self.utterances[self.current_utterance].update()

    def render(self, surface: Surface):
        self.utterances[self.current_utterance].render(surface)


@cache
def load_script(filename: str = 'game/assets/text/en/script.json') -> dict:
    with open(filename, encoding='utf-8', mode='r') as f:
        return json.load(f)


@cache
def parse_script(index: int) -> tuple[tuple[str, ...], ...]:
    script = load_script()
    return tuple(script['scenes'][index]['lines'])
