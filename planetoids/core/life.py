import pygame

from planetoids.core.config import config

class Life:
    def __init__(self, settings):
        self.settings = settings
        self.lives = 3

    @property
    def font(self):
        return pygame.font.Font(
            self.settings.FONT_PATH,
            {"minimum":36, "medium": 48, "maximum": 64}.get(self.settings.get("pixelation"), 36)
        )

    def decrement(self):
        self.lives -= 1

    def get_lives(self):
        return self.lives

    def draw(self, screen):
        """Displays remaining player lives as small triangles in the top-right corner, Galaga-style."""
        ship_size = {"minimum": 15, "medium": 30, "maximum": 45}.get(self.settings.get("pixelation"), 15)
        spacing = {"minimum": 10, "medium": 20, "maximum": 30}.get(self.settings.get("pixelation"), 10)
        start_x = {"minimum": 10, "medium": 20, "maximum": 30}.get(self.settings.get("pixelation"), 10)
        start_y = {"minimum": 18, "medium": 36, "maximum": 54}.get(self.settings.get("pixelation"), 18)

        for i in range(self.lives - 1):
            x_offset = start_x + i * (ship_size + spacing)

            # Triangle points for the small ship
            front = (x_offset, start_y - ship_size)
            left = (x_offset - ship_size * 0.6, start_y + ship_size * 0.6)
            right = (x_offset + ship_size * 0.6, start_y + ship_size * 0.6)

            # Draw the mini ship
            pygame.draw.polygon(screen, config.WHITE, [front, left, right], 1)