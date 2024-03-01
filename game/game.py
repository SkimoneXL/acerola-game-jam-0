import pygame
from game.scene.manager import SceneManager


def main() -> None:
    pygame.init()
    surface = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    scene_manager = SceneManager(surface)

    while running:

        running = scene_manager.handle_events()
        # fill the screen with a color to wipe away anything from last frame
        surface.fill("purple")

        scene_manager.update()
        scene_manager.render()

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
