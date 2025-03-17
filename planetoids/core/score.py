import pygame

from planetoids.core.config import config

class Score:
    def __init__(self, settings):
        self.score = 0
        self.settings = settings

    @property
    def font(self):
        return pygame.font.Font(
            self.settings.FONT_PATH,
            {"minimum":36, "medium": 48, "maximum": 64}.get(self.settings.get("pixelation"), 36)
        )

    def update_score(self, asteroid):
        """Increase score based on asteroid size."""
        if asteroid.size >= 40:
            self.score += 100
        elif asteroid.size >= 20:
            self.score += 200
        else:
            self.score += 300
        print(f"Score: {self.score}")

    def draw(self, screen):
        """Displays the score in the top-right corner."""
        offset = {"minimum": 200, "medium": 300, "maximum": 400}.get(self.settings.get("pixelation"), 200)
        score_text = self.font.render(f"Score: {self.score}", True, config.WHITE)
        screen.blit(score_text, (config.WIDTH - offset, 20))  # Position in top-right
