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
        game_over_font = pygame.font.Font(self.settings.FONT_PATH, 256)
        font_size = {"minimum":36, "medium": 48, "maximum": 64}.get(self.settings.get("pixelation"), 36)
        prompt_font = pygame.font.Font(self.settings.FONT_PATH, font_size)

        text = game_over_font.render("GAME OVER", True, config.YELLOW)
        text_rect = text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2))

        prompt_text = prompt_font.render("Press any key to continue", True, config.DIM_GRAY)
        prompt_rect = prompt_text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 + 120))

        start_time = pygame.time.get_ticks()
        game_over = True

        accuracy = (
            (self.game_state.shots_hit / self.game_state.shots_fired) * 100
            if self.game_state.shots_fired > 0 else 0
        )

        # Time survived calculation
        elapsed_ms = pygame.time.get_ticks() - self.game_state.start_time
        seconds = elapsed_ms // 1000
        minutes = seconds // 60
        hours = minutes // 60
        formatted_time = f"{hours:02}:{minutes % 60:02}:{seconds % 60:02}"

        while game_over:
            screen.fill(config.BLACK)

            for asteroid in self.game_state.asteroids:
                asteroid.update()
                asteroid.draw(screen)

            self.game_state.score.draw(screen, show_multiplier=False)
            self.game_state.level.draw(screen)

            screen.blit(text, text_rect)

            # Show prompt only after 3 seconds (3000 milliseconds)
            if pygame.time.get_ticks() - start_time > 3000:
                screen.blit(prompt_text, prompt_rect)

            if self.settings.get("crt_enabled"):
                crt_effect.apply_crt_effect(
                    screen,
                    intensity=self.settings.get("glitch_intensity"),
                    pixelation=self.settings.get("pixelation")
                )

            # Additional stats display
            stat_font = pygame.font.Font(self.settings.FONT_PATH, font_size)
            stats = [
                f"Time Survived: {formatted_time}",
                f"Shots Fired: {self.game_state.shots_fired}",
                f"Asteroids Destroyed: {self.game_state.asteroids_destroyed}",
                f"Accuracy: {accuracy:.1f}%"
            ]

            for i, line in enumerate(stats):
                stat_text = stat_font.render(line, True, config.WHITE)
                stat_rect = stat_text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 + 200 + i * 40))
                screen.blit(stat_text, stat_rect)

            pygame.display.flip()
            self.game_state.clock.tick(config.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Only allow exit after 3 seconds
                if event.type == pygame.KEYDOWN and pygame.time.get_ticks() - start_time > 3000:
                    game_over = False
