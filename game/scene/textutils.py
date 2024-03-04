import json
from functools import cache
from typing import Any

import pygame
from attrs import define
from pygame import Surface
from pygame.font import Font
from pygame.sprite import Sprite

from game.scene.registry import FontRegistry, SceneRegistry
from game.timer import Timer


@define(kw_only=True)
class ScrolledText:
    text: str
    font: Font
    color: Any
    position: tuple[int, int]
    done: bool = False
    index: int = 0
    _str_buffer: str = ''

    @property
    def text_length(self):
        return len(self.text)

    def update(self):
        if self.done: return
        self._str_buffer = self.text[:self.index]
        self.index += 1
        if self.index == len(self.text) + 1:
            self.done = True

    def render(self, surface: Surface):
        text_surface = self.font.render(self._str_buffer, True, self.color)
        surface.blit(text_surface, self.position)

    def done(self) -> bool:
        return self._index >= len(self.text)


@define(kw_only=True)
class Utterance:
    lines: tuple[ScrolledText, ...]
    current_line: int
    done: bool
    _line_buffer: list[ScrolledText]

    def __init__(self, lines: tuple[str], font: Font, fontsize: int):
        color = (0, 0, 0)
        x, y = (0, 0)
        self.lines = tuple(
            ScrolledText(
                text=line,
                font=font,
                color=color,
                position=(x, y + i * fontsize),
                done=False,
            ) for i, line in enumerate(lines))
        self.current_line = 0
        self.done = False
        self._line_buffer = [self.lines[0]]

    def update(self):
        if self.done: return

        current_line = self.lines[self.current_line]

        if current_line.done:
            self.current_line += 1
            if self.current_line == len(self.lines):
                self.done = True
                return
            self._line_buffer.append(self.lines[self.current_line])

        for _line in self._line_buffer:
            _line.update()

    def render(self, surface: Surface):
        for line in self._line_buffer:
            line.render(surface)


@define(kw_only=True)
class TextGUI:
    font: Font
    fixed_update_timer: Timer
    throttle_timer: Timer
    utterances: tuple[Utterance, ...]
    box: Sprite = None
    current_utterance: int = 0
    done: bool = False
    throttle_input: bool = False

    @staticmethod
    def create(scene: SceneRegistry):
        fontsize = 20
        font = FontRegistry.get(FontRegistry.SILVER, fontsize)

        return TextGUI(
            font=font,
            utterances=tuple(
                Utterance(lines=utterance, font=font, fontsize=fontsize)
                for utterance in parse_script(scene.value)),
            throttle_timer=Timer(duration_millis=1500),
            throttle_input=True,
            fixed_update_timer=Timer(duration_millis=10),
        )

    def update(self):
        if self.done: return

        if self.throttle_input:
            self.throttle_timer.update()
        if self.throttle_timer.done:
            self.throttle_input = False

        self.fixed_update_timer.update()
        if not self.fixed_update_timer.done: return

        self.utterances[self.current_utterance].update()
        self.handle_keypress()

        self.fixed_update_timer.reset()

    def render(self, surface: Surface):
        if not self.done:
            self.utterances[self.current_utterance].render(surface)

    def handle_keypress(self):
        if self.throttle_input: return

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.throttle_input = True
            self.current_utterance += 1
            if self.current_utterance == len(self.utterances):
                self.done = True
            else:
                self.throttle_timer.reset()


@cache
def load_script(filename: str = 'game/assets/text/en/script.json') -> dict:
    with open(filename, encoding='utf-8', mode='r') as f:
        return json.load(f)


@cache
def parse_script(index: int) -> tuple[tuple[str, ...], ...]:
    script = load_script()
    return tuple(script['scenes'][index]['lines'])
