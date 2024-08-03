import pygame
from pygame import Surface

from game.player.player import Player
from game.scene.levels.tiling import TileMap
from game.scene.registry import SceneIndex, TileMapPath
from game.scene.scene import Scene
from game.scene.textutils import TextGUI


class School_1(Scene):

    def __init__(self, player: Player) -> None:
        super().__init__(player)
        # self.gui = TextGUI.create(SceneIndex.SCHOOL_1)
        self.tilemap = TileMap(TileMapPath.SCHOOL_1)

    def render(self, surface: Surface) -> None:
        self.tilemap.render(surface)
        self.player.render(surface)
        # self.gui.render(surface)

    def update(self) -> None:
        self.player.update()
        self.detect_collisions()
        # self.gui.update()

    def detect_collisions(self) -> None:
        for rect in self.player.get_nearby_tile_bounds(self.tilemap):
            self.player.physics.detect_collision(self.player.rect, rect)

    def get_next_scene(self) -> SceneIndex:
        return SceneIndex.DREAM_1

    def handle_event(self, event) -> None:
        self.player.handle_event(event)
        self.tilemap.handle_event(event)
        # self.gui.handle_event(event)


class School_2(Scene):

    def __init__(self, player: Player) -> None:
        super().__init__(player)
        self.gui = TextGUI.create(SceneIndex.SCHOOL_1)

    def render(self, surface: Surface) -> None:
        self.player.render(surface)
        self.gui.render(surface)

    def update(self) -> None:
        self.player.update()
        self.gui.update()
        keys = pygame.key.get_pressed()

    def get_next_scene(self) -> SceneIndex:
        return SceneIndex.DREAM_2

    def handle_event(self, event) -> None:
        self.player.handle_event(event)
