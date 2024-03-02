from dataclasses import dataclass
from typing import Any
from pygame.font import Font


@dataclass(kw_only=True)
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

    def render(self, surface):
        txt_surf = self.font.render(self._str_buffer, True, self.color)
        surface.blit(txt_surf, self.position)
