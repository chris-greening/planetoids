import pygame
from start_menu import StartMenu
from bullet import Bullet
from game_state import GameState
import config

def main():
    pygame.init()

    # Initialize window
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.FULLSCREEN)
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

        # Handle events (always process inputs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_state.toggle_pause()
                elif event.key == pygame.K_c:
                    game_state.clear_asteroids()
                elif event.key == pygame.K_SPACE and not game_state.paused:
                    game_state.bullets.extend(game_state.player.shoot())  # Handle trishot
                
            elif event.type == pygame.USEREVENT + 1:  # Trishot expiration event
                game_state.player.trishot_active = False  # Disable trishot

        # If paused, show pause screen but allow event processing
        if game_state.paused:
            show_pause_screen(screen)
            pygame.display.flip()
            continue  # Skip game updates but allow event processing

        # Update game state
        keys = pygame.key.get_pressed()
        game_state.update_all(keys)
        game_state.check_for_clear_map()
        game_state.check_for_collisions(screen)

        # Draw everything
        game_state.draw_all(screen)

        pygame.display.flip()

    pygame.quit()


def show_pause_screen(screen):
    """Displays a semi-transparent pause overlay."""
    font = pygame.font.Font(None, 50)
    text = font.render("PAUSED - Press P to Resume", True, config.WHITE)

    # Draw a semi-transparent overlay
    overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # 150 alpha for slight transparency
    screen.blit(overlay, (0, 0))

    # Draw the text centered
    screen.blit(text, (config.WIDTH // 2 - 200, config.HEIGHT // 2))

if __name__ == "__main__":
    main()

