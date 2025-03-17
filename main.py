import os

import pygame
import dotenv

from planetoids.effects import crt_effect
from planetoids.core.config import config
from planetoids.core.game_state import GameState
from planetoids.core.settings import Settings
from planetoids.core.logger import logger
from planetoids.ui import IntroAnimation, GameOver, StartMenu

dotenv.load_dotenv()
DEBUG_MODE = os.getenv("DEBUG", "False").lower() in ("true", "1")

def main():
    logger.info("Game start")
    pygame.init()

    settings = Settings()
    fullscreen = settings.get("fullscreen_enabled")
    # fullscreen = False

    while True:  # Main game loop that allows restarting
        pygame.mouse.set_visible(False)

        # ✅ Apply Fullscreen or Windowed Mode
        screen_mode = pygame.FULLSCREEN if settings.get("fullscreen_enabled") else 0
        if fullscreen:
            screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.FULLSCREEN)
        else:
            fixed_size = (960, 540)  # Fixed window size
            screen = pygame.display.set_mode(fixed_size, pygame.RESIZABLE)

        pygame.display.set_caption("Planetoids")
        clock = pygame.time.Clock()

        # Intro animation if not debugging
        if not DEBUG_MODE:
            intro = IntroAnimation(screen, clock)
            intro.play()

        # Show the start menu
        start_menu = StartMenu(screen, clock, settings)
        start_menu.show()

        # Create GameState instance
        game_state = GameState(screen, settings, clock)
        game_state.spawn_asteroids(5)

        running = True
        while running:
            screen.fill(config.BLACK)
            dt = clock.tick(60) / 1000.0
            game_state.update_dt(dt)
            _event_handler(game_state)

            if game_state.paused:
                continue

            # Update game state
            keys = pygame.key.get_pressed()
            game_state.update_all(keys, dt)
            game_state.check_for_clear_map()
            game_state.check_for_collisions(screen)

            # Draw everything
            game_state.draw_all(screen)

            if settings.get("crt_enabled"):
                crt_effect.apply_crt_effect(screen, settings)
            pygame.display.flip()

            # Check for Game Over condition
            if game_state.life.lives <= 0:
                game_over_screen = GameOver(game_state, settings)
                restart_game = game_over_screen.game_over(screen, dt)

                if restart_game:
                    running = False  # Exit game loop, return to start menu

def _event_handler(game_state):
    """Handle key input events"""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_state.toggle_pause()
            elif event.key == pygame.K_SPACE and not game_state.paused:
                game_state.bullets.extend(game_state.player.shoot())
        elif event.type == pygame.VIDEORESIZE:  # 🔹 Detect window resizing
            new_width, new_height = event.w, event.h
            config.update_dimensions(new_width, new_height)  # 🔹 Update game dimensions
            pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.RESIZABLE)
        game_state.handle_powerup_expiration(event)

if __name__ == "__main__":
    main()
