"""Main entry point for the game"""

# pylint: disable=no-member,invalid-name

import os
from typing import Tuple

import pygame
import dotenv

from planetoids.effects import crt_effect
from planetoids.core.config import config
from planetoids.core.game_state import GameState
from planetoids.core.settings import Settings, get_font_path
from planetoids.core.logger import logger
from planetoids.ui import IntroAnimation, GameOver, StartMenu

dotenv.load_dotenv()
DEBUG_MODE = os.getenv("DEBUG", "False").lower() in ("true", "1")

def main() -> None:
    """Main entry point for the game"""
    logger.info("Game start")
    pygame.init()

    settings = Settings()

    game_start = True
    while True:  # Main game loop that allows restarting
        pygame.mouse.set_visible(False)

        screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.FULLSCREEN)
        print(type(screen))

        pygame.display.set_caption("Planetoids")
        clock = pygame.time.Clock()

        # Intro animation if not debugging
        if not DEBUG_MODE and game_start:
            intro = IntroAnimation(screen, clock)
            intro.play()
            game_start = False

        # Show the start menu
        start_menu = StartMenu(screen, clock, settings)
        start_menu.show()

        # Create GameState instance
        game_state = GameState(screen, settings, clock)
        game_state.spawn_asteroids(10)

        # Display controls overlay for first few seconds
        show_controls_timer = 5  # Show for 3 seconds

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

            show_controls_timer =_show_controls(
                show_controls_timer,
                settings,
                screen,
                dt
            )

            _draw_crt_effects(settings, screen)
            pygame.display.flip()

            running = _check_for_game_over(
                game_state, settings, screen, dt, running
            )

def _check_for_game_over(
        game_state: GameState, settings: Settings,
        screen: pygame.Surface, dt: float,
        running: bool
    ) -> bool:
    """Return Boolean check for game running"""
    if game_state.life.lives <= 0:
        game_state.score.maybe_save_high_score()
        game_over_screen = GameOver(game_state, settings)
        restart_game = game_over_screen.game_over(screen, dt)

        if restart_game:
            running = False  # Exit game loop, return to start menu
    return running

def _draw_crt_effects(settings: Settings, screen: pygame.Surface) -> None:
    """Draw CRT effects if enabled"""
    if settings.get("crt_enabled"):
        crt_effect.apply_crt_effect(
            screen,
            intensity=settings.get("glitch_intensity"),
            pixelation=settings.get("pixelation")
        )

def _show_controls(
        show_controls_timer: float, settings: Settings,
        screen: pygame.Surface, dt: float
    ) -> float:
    """Return show_controls_timer and draws controls to the screen"""
    if show_controls_timer > 0:
        controls = (
            ("CONTROLS:", -80, 180, config.YELLOW),
            ("Arrow keys - Movement", -50, 220, config.GREEN),
            ("SPACE - Shoot", -50, 260, config.GREEN),
            ("P - Pause", -50, 300, config.GREEN)
        )
        half_width = config.WIDTH // 2
        third_height = config.HEIGHT // 3
        for control in controls:
            coords = (half_width - control[1], third_height + control[2])
            _draw_text(
                screen,
                control[0],
                coords,
                settings,
                control[3]
            )
        show_controls_timer -= dt  # Decrease timer
    return show_controls_timer

def _event_handler(game_state: GameState) -> None:
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

def _draw_text(
        screen: pygame.Surface, text: str, coords: Tuple[int, int],
        settings: Settings, color: Tuple[int, int, int]=config.WHITE
    ) -> None:
    """Helper function to render sharp, readable text."""
    font_size = {
            "minimum":36,
            "medium": 48,
            "maximum": 64
        }.get(settings.get("pixelation"), 36)
    font = pygame.font.Font(get_font_path(), font_size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, coords)

if __name__ == "__main__":
    main()
