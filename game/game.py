import pygame

from game import game_clock
from game.player.player import Player
from game.scene.manager import SceneManager


def main() -> None:
    pygame.init()
    pygame.font.init()

    surface = pygame.display.set_mode((1280, 720), flags=pygame.SCALED)
    running = True

    player = Player()
    scene_manager = SceneManager(player, surface)

    while running:
        running = scene_manager.handle_events()
        scene_manager.update()
        scene_manager.render()
        pygame.display.flip()
        game_clock.tick()

    pygame.quit()
