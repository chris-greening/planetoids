import pygame
from start_menu import StartMenu
from game_state import GameState
import crt_effect
import config

def main():
    pygame.init()

    # Initialize window
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Planetoids!")
    clock = pygame.time.Clock()

    # Show the start menu
    start_menu = StartMenu(screen, clock)
    crt_enabled = start_menu.show()  # Returns True or False

    # Create GameState instance
    game_state = GameState(screen, crt_enabled, clock)
    print(crt_enabled)
    game_state.spawn_asteroids(5)

    running = True
    while running:
        screen.fill(config.BLACK)
        clock.tick(config.FPS)

        _event_handler(game_state)

        if game_state.paused:
            continue

        # Update game state
        keys = pygame.key.get_pressed()
        game_state.update_all(keys)
        game_state.check_for_clear_map()
        game_state.check_for_collisions(screen)

        # Draw everything
        game_state.draw_all(screen)

        if game_state.crt_enabled:
            crt_effect.apply_crt_effect(screen)
        pygame.display.flip()

    pygame.quit()

def _event_handler(game_state):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_state.toggle_pause()
            elif event.key == pygame.K_SPACE and not game_state.paused:
                game_state.bullets.extend(game_state.player.shoot())
        game_state.handle_powerup_expiration(event)

if __name__ == "__main__":
    main()

