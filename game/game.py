import pygame
from game.scene.manager import SceneManager
from game import game_clock


def main() -> None:
    pygame.init()
    pygame.font.init()

    surface = pygame.display.set_mode((1280, 720), flags=pygame.SCALED)
    running = True

    scene_manager = SceneManager(surface)

    while running:

        running = scene_manager.handle_events()
        surface.fill((50, 70, 100))

        scene_manager.update()
        scene_manager.render()

        pygame.display.flip()

        game_clock.tick()

    pygame.quit()
