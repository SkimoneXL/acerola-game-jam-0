import pygame

from game import game_clock
from game.player.player import Player
from game.scene.manager import SceneManager
from game.scene.registry import FontRegistry


def main() -> None:
    pygame.init()
    pygame.font.init()

    surface = pygame.display.set_mode((1280, 720), flags=pygame.SCALED)
    running = True

    player = Player()
    scene_manager = SceneManager(player, surface)

    while running:

        running = scene_manager.handle_events()
        surface.fill((50, 70, 100))

        scene_manager.update()
        scene_manager.render()

        surface.blit(
            FontRegistry.get(FontRegistry.SILVER).render(
                str(int(game_clock.get_fps())),
                True,
                (0, 0, 0),
            ),
            (1000, 0),
        )

        pygame.display.flip()

        game_clock.tick()

    pygame.quit()
