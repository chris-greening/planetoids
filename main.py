import pygame
from player import Player
from bullet import Bullet
from game_state import GameState  # New centralized game manager
import config
import start_menu

def main() -> None:
    pygame.init()

    # Initialize window
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Asteroids Clone")
    clock = pygame.time.Clock()

    # Show start menu before the game starts
    start_menu.show_start_menu(screen, clock)

    # Create GameState instance to track all objects
    game_state = GameState()
    game_state.spawn_asteroids(5)  # Initial asteroids

    player = Player()

    running = True
    while running:
        screen.fill(config.BLACK)
        clock.tick(config.FPS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state.bullets.append(Bullet(player.x, player.y, player.angle))

        # Update game state
        keys = pygame.key.get_pressed()
        player.update(keys)
        game_state.update_all()
        game_state.check_for_collisions()

        # Draw everything
        player.draw(screen)
        game_state.draw_all(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
