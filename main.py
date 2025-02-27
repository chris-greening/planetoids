import pygame
from start_menu import StartMenu
from bullet import Bullet
from game_state import GameState
import config

def main():
    pygame.init()

    # Initialize window
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption("Planetoids!")
    clock = pygame.time.Clock()

    # Show the start menu
    start_menu = StartMenu(screen, clock)
    start_menu.show()

    # Create GameState instance
    game_state = GameState()
    game_state.spawn_asteroids(5)  # Initial asteroids

    running = True
    while running:
        screen.fill(config.BLACK)
        clock.tick(config.FPS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state.bullets.append(
                    Bullet(
                        x=game_state.player.x,
                        y=game_state.player.y,
                        angle=game_state.player.angle
                    )
                )

        # Update game state
        keys = pygame.key.get_pressed()
        game_state.update_all(keys)
        game_state.check_for_clear_map()
        game_state.check_for_collisions(screen)

        # Draw everything
        game_state.draw_all(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

