import os

import pygame

from planetoids.core import config
from planetoids.effects import crt_effect

class GameOver:
    def __init__(self, game_state):
        self.game_state = game_state

    def game_over(self, screen):
        """Ends the game and shows Game Over screen."""
        self._display_game_over(screen)  # For now, just print (will be replaced with a menu)
        pygame.quit()
        exit()

    def _display_game_over(self, screen):
        """Displays 'GAME OVER' while the game keeps running, showing moving asteroids in the background."""
        font_path = os.path.join("assets", "fonts", "VT323.ttf")  # ✅ Match Planetoids font
        game_over_font = pygame.font.Font(font_path, 64)  # ✅ Big text size

        text = game_over_font.render("GAME OVER", True, config.YELLOW)
        text_rect = text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2))

        game_over = True
        while game_over:
            screen.fill(config.BLACK)

            # Keep updating & drawing asteroids so they continue moving
            for asteroid in self.game_state.asteroids:
                asteroid.update(self.game_state)
                asteroid.draw(screen)

            # Draw the "GAME OVER" text
            screen.blit(text, text_rect)

            if self.game_state.settings.get("crt_enabled"):
                crt_effect.apply_crt_effect(screen)

            pygame.display.flip()
            self.game_state.clock.tick(config.FPS)

            # Wait for a key press to return to the main menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:  # Any key press exits the game over screen
                    game_over = False