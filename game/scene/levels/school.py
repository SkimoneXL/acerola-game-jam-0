import pygame
from pygame import Surface

from game.player.player import Player
from game.scene.levels.tiling import TileMap
from game.scene.registry import SceneRegistry, TileMapRegistry
from game.scene.scene import Scene
from game.scene.textutils import TextGUI


class School_1(Scene):

    def __init__(self, player: Player):
        super().__init__(player)
        self.gui = TextGUI.create(SceneRegistry.SCHOOL_1)
        self.tilemap = TileMap(TileMapRegistry.SCHOOL_1)

    def render(self, surface: Surface):
        self.tilemap.render(surface)
        self.player.render(surface)
        #self.gui.render(surface)

    def update(self):
        self.player.update()
        self.detect_collisions()
        #self.gui.update()

    def detect_collisions(self) -> None:
        for rect in self.tilemap.get_tile_bounds():
            if self.player.physics.detect_collision(self.player.rect, rect):
                return

    def get_next_scene(self):
        return SceneRegistry.DREAM_1

    def handle_event(self, event):
        self.player.handle_event(event)
        self.tilemap.handle_event(event)


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
