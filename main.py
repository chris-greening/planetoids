import pygame

from planetoids.ui.start_menu import StartMenu
from planetoids.core.game_state import GameState
from planetoids.effects import crt_effect
from planetoids.core import config, settings
from planetoids.core.logger import logger
from planetoids.ui.intro_animation import IntroAnimation

def main():
    logger.info("Game start")
    logger.debug("Debug mode activated")
    pygame.init()

    game_settings = settings.load_settings()

    # Initialize window
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Planetoids")
    clock = pygame.time.Clock()

    intro = IntroAnimation(screen, clock)
    intro.play()

    # Show the start menu
    start_menu = StartMenu(screen, clock, game_settings)
    game_settings = start_menu.show()  # Returns True or False

    # Create GameState instance
    game_state = GameState(screen, game_settings, clock)
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

        if game_state.settings["crt_enabled"]:
            crt_effect.apply_crt_effect(screen)
        pygame.display.flip()

    pygame.quit()

def _event_handler(game_state):
    """Handle key input events"""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_state.toggle_pause()
            elif event.key == pygame.K_SPACE and not game_state.paused:
                game_state.bullets.extend(game_state.player.shoot())
        game_state.handle_powerup_expiration(event)

if __name__ == "__main__":
    main()
