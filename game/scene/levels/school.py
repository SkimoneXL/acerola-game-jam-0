import os
import pygame
from pygame import Surface

from game.player.player import Player
from game.scene.levels.tiling import TileMap, TileSet
from game.scene.registry import SceneRegistry
from game.scene.scene import Scene
from game.scene.textutils import TextGUI


class School_1(Scene):

    def __init__(self, player: Player):
        super().__init__(player)
        self.gui = TextGUI.create(SceneRegistry.SCHOOL_1)
        self.tilemap = TileMap(TileSet(file='game/assets/tilemaps/test.png'))
        #self.image = self.tilemap.tileset.image

    def render(self, surface: Surface):
        self.player.render(surface)
        #self.gui.render(surface)
        #surface.blit(self.image, (0, 0))
        self.tilemap.render(surface)

    def update(self):
        self.player.update()
        #self.gui.update()

    def get_next_scene(self):
        return SceneRegistry.DREAM_1

    def handle_event(self, event):
        self.player.handle_event(event)


class School_2(Scene):

    def __init__(self, player: Player):
        super().__init__(player)
        self.gui = TextGUI.create(SceneRegistry.SCHOOL_1)

    def render(self, surface: Surface):
        self.player.render(surface)
        self.gui.render(surface)

    def update(self):
        self.player.update()
        self.gui.update()
        keys = pygame.key.get_pressed()

    def get_next_scene(self):
        return SceneRegistry.DREAM_2

    def handle_event(self, event):
        self.player.handle_event(event)
