import pygame

from planetoids.core.config import config

class Level:
    def __init__(self, settings):
        self.settings = settings
        self.level = 1

    @property
    def font(self):
        return pygame.font.Font(
            self.settings.FONT_PATH,
            {"minimum":36, "medium": 48, "maximum": 64}.get(self.settings.get("pixelation"), 36)
        )

    def increment_level(self):
        self.level += 1

    def get_level(self):
        return self.level

    def draw(self, screen):
        """Display current level number."""
        x_offset = {"minimum": 120, "medium": 170, "maximum": 320}.get(self.settings.get("pixelation"), 200)
        y_offset = {"minimum": 30, "medium": 40, "maximum": 55}.get(self.settings.get("pixelation"), 200)
        text = self.font.render(f"Level: {self.level}", True, config.WHITE)
        screen.blit(text, (config.WIDTH - x_offset, config.HEIGHT - y_offset))  # Display bottom-right
