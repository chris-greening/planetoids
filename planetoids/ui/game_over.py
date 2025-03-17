import os

import pygame

from planetoids.core.config import config
from planetoids.effects import crt_effect

class GameOver:
    def __init__(self, game_state, settings):
        self.game_state = game_state
        self.settings = settings

    def game_over(self, screen, dt):
        """Ends the game and shows the Game Over screen. Returns True to restart or False to quit."""
        self._display_game_over(screen, dt)
        return True  # Indicate that we want to restart

    def _display_game_over(self, screen, dt):
        """Displays 'GAME OVER' while keeping asteroids moving in the background."""
        game_over_font = pygame.font.Font(self.settings.FONT_PATH, 64)

        text = game_over_font.render("GAME OVER", True, config.YELLOW)
        text_rect = text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2))

        game_over = True
        while game_over:
            screen.fill(config.BLACK)

            # Keep asteroids moving in the background
            for asteroid in self.game_state.asteroids:
                asteroid.update()
                asteroid.draw(screen)

            # Draw "GAME OVER" text
            screen.blit(text, text_rect)

            if self.game_state.settings.get("crt_enabled"):
                crt_effect.apply_crt_effect(screen, self.settings)

            pygame.display.flip()
            self.game_state.clock.tick(config.FPS)

            # Wait for a key press to return to the main menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:  # Any key press exits the Game Over screen
                    game_over = False  # Exit loop and return to main menu
