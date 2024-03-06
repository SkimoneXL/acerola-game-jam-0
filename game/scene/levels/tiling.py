from functools import lru_cache
import json
from typing import Any
from attr import define
import numpy as np
from pygame import Surface, Rect
import pygame


@define(kw_only=True)
class Tile:
    image: Surface
    index: int
    collision: bool
    rect: Rect


class TileSet:

    def __init__(
            self,
            file: str,
            size: tuple[int, int] = (32, 32),
            margin: int = 0,
            spacing: int = 0,
    ):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image: Surface = pygame.image.load(file).convert_alpha()
        self.rect: Rect = self.image.get_rect()
        self.tiles: list[Tile] = []
        self.load()

    def load(self):

        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = Surface(self.size, flags=pygame.SRCALPHA).convert_alpha()
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(Tile(image=tile, index=len(self.tiles), collision=True,
                                       rect=None))

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'


class TileMap:

    def __init__(
        self,
        tileset: TileSet,
        level_json_filename: str,
    ):
        self.tileset = tileset
        self.EMPTY_TILE_INDEX = 0
        self.level_json_filename = level_json_filename
        self.load()

    def load(self):
        with open(self.level_json_filename, 'r', encoding='utf-8') as f:
            level_data = json.load(f)
        self.map = np.array(level_data['tile_data'])
        self.size = self.map.shape
        self._construct_image()

    def render(self, surface: Surface):
        surface.blit(self.image, (0, 0))

    def _construct_image(self):
        h, w = self.size
        self.image = Surface((32 * w, 32 * h), flags=pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()

        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                ti = self.map[i, j]
                if ti == self.EMPTY_TILE_INDEX: continue
                self.image.blit(
                    self.tileset.tiles[ti].image,
                    (j * 32, i * 32),
                )
                self.tileset.tiles[ti].rect = Rect(j * 32, i * 32, 32, 32)

    @lru_cache
    def get_tile_bounds(self):
        m, n = self.map.shape
        result = []
        for i in range(m):
            for j in range(n):
                ti = self.map[i, j]
                if ti == self.EMPTY_TILE_INDEX: continue
                result.append(self.tileset.tiles[ti].rect)
        return result

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            self.load()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'
