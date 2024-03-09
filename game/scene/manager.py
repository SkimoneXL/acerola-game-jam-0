import pygame
from pygame import Surface

from game.constants import UserEvent
from game.player.player import Player
from game.scene.levels.dream import Dream_1, Dream_2
from game.scene.levels.school import School_1, School_2
from game.scene.menu import MainMenu
from game.scene.registry import SceneIndex
from game.scene.scene import Scene


def get_scene(scene: SceneIndex, player: Player) -> Scene:
    match (scene):
        case SceneIndex.MAIN_MENU:
            return MainMenu(player)
        case SceneIndex.SCHOOL_1:
            return School_1(player)
        case SceneIndex.SCHOOL_2:
            return School_2(player)
        case SceneIndex.DREAM_1:
            return Dream_1(player)
        case SceneIndex.DREAM_2:
            return Dream_2(player)


class SceneManager:
    current_scene: Scene
    player: Player
    surface: Surface

    def __init__(
        self,
        player: Player,
        surface: Surface,
        current_scene: SceneIndex = SceneIndex.MAIN_MENU,
    ) -> None:
        self.surface = surface
        self.player = player
        self.current_scene = get_scene(current_scene, self.player)

    def render(self):
        self.current_scene.render(self.surface)

    def update(self):
        self.current_scene.update()

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            match (event.type):
                case pygame.QUIT:
                    return False
                case UserEvent.SCENE_CHANGE:
                    reg = self.current_scene.get_next_scene()
                    scene = get_scene(reg, self.player)
                    self.change_scene(scene)
                case _:
                    self.current_scene.handle_event(event)

        return True

    def change_scene(self, new_scene: Scene) -> None:
        self.current_scene = new_scene
