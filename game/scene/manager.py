import pygame
from game.scene.level import Level
from game.scene.menu import MainMenu
from game.scene.registry import SceneRegistry
from game.scene.scene import Scene
from game.constants import UserEvent
from pygame import Surface


def get_scene(scene: SceneRegistry) -> Scene:
    match (scene):
        case SceneRegistry.MAIN_MENU:
            return MainMenu()
        case SceneRegistry.LEVEL_1:
            return Level()


class SceneManager:
    surface: Surface
    current_scene: Scene

    def __init__(
        self,
        surface: Surface,
        current_scene: SceneRegistry = SceneRegistry.MAIN_MENU,
    ) -> None:
        self.surface = surface
        self.current_scene = get_scene(current_scene)

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
                    scene = get_scene(reg)
                    self.change_scene(scene)

        return True

    def change_scene(self, new_scene: Scene) -> None:
        self.current_scene = new_scene
