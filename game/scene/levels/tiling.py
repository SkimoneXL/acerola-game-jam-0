import numpy as np
from pygame import Surface, Rect
import pygame


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
        self.tiles: list[Surface] = []
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
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'


class TileMap:

    def __init__(self, tileset: TileSet, size: tuple[int, int] = (3, 8), rect: Rect = None):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)

        h, w = self.size
        self.image = Surface((32 * w, 32 * h), flags=pygame.SRCALPHA).convert_alpha()
        if rect:
            self.rect = Rect(rect)
        else:
            self.rect = self.image.get_rect()

        self.set_random()

    def render(self, surface: Surface):
        surface.blit(self.image, (0, 0))

    def construct_image(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j * 32, i * 32))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        self.construct_image()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        self.construct_image()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'
