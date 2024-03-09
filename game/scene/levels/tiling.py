import json
from functools import lru_cache

import numpy as np
import pygame
from attr import define
from pygame import Rect, Surface


@define(kw_only=True)
class Tile:
    image: Surface
    index: int
    collision: bool
    rect: Rect


@define(kw_only=True)
class TileSet:

    empty_tile_index: int
    file: str
    margin: int
    size: tuple[int, int]
    spacing: int
    has_collision: list[bool] = None
    tiles: list[Tile] = None

    @staticmethod
    def create(level_data: dict):
        tile_set = level_data['tile_set']
        return TileSet(
            empty_tile_index=tile_set['empty_tile_index'],
            file=tile_set['source_image'],
            margin=tile_set['margin'],
            size=(tile_set['tile_size_x'], tile_set['tile_size_y']),
            spacing=tile_set['spacing'],
            has_collision=tile_set['has_collision'],
        )

    def __attrs_post_init__(self):
        self.load_tiles()

    def load_tiles(self) -> list[Tile]:
        self.tiles = []
        image = pygame.image.load(self.file).convert_alpha()
        x0 = y0 = self.margin
        w, h = image.get_rect().size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for i, x in enumerate(range(x0, w, dx)):
            for j, y in enumerate(range(y0, h, dy)):
                tile = Surface(self.size, flags=pygame.SRCALPHA).convert_alpha()
                tile.blit(image, (0, 0), (x, y, *self.size))
                self.tiles.append(
                    Tile(
                        image=tile,
                        index=len(self.tiles),
                        collision=self.has_collision[j][i],
                        rect=tile.get_rect(),
                    ))


class TileMap:
    level_json_filename: str

    def __init__(self, level_json_filename: str):
        self.level_json_filename = level_json_filename
        self.load()

    def load(self):
        with open(self.level_json_filename, 'r', encoding='utf-8') as f:
            level_data = json.load(f)
        self.tileset = TileSet.create(level_data)
        self._parse(level_data)

    def _parse(self, level_data):
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
                if ti == self.tileset.empty_tile_index: continue
                self.image.blit(
                    self.tileset.tiles[ti].image,
                    (j * 32, i * 32),
                )

    def get_tile_bounds(self):
        m, n = self.map.shape
        result = []
        for i in range(m):
            for j in range(n):
                ti = self.map[i, j]
                if ti == self.tileset.empty_tile_index: continue
                x, y = self.tileset.size
                result.append(Rect(j * 32, i * 32, x, y))
        return result

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            self.load()
