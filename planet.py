import pygame
import random
from config import WIDTH, HEIGHT

class Planet:
    def __init__(self):
        """Generate a random planet with a position, color, and craters."""
        self.radius = random.randint(50, 150)  # Random size
        self.x = random.randint(200, WIDTH - 200)
        self.y = random.randint(200, HEIGHT - 200)
        self.base_color = (
            random.randint(50, 255),  # R
            random.randint(50, 255),  # G
            random.randint(50, 255),  # B
        )
        self.surface = self._generate_planet_surface()

    def _generate_planet_surface(self):
        """Creates a Pygame surface for the planet with a gradient and craters."""
        planet_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

        # Draw a gradient effect for depth
        for i in range(self.radius, 0, -1):
            alpha = int(255 * (i / self.radius))  # Fade edges
            pygame.draw.circle(planet_surface, (*self.base_color, alpha), (self.radius, self.radius), i)

        # Add random craters
        for _ in range(random.randint(3, 7)):
            crater_x = random.randint(10, self.radius * 2 - 10)
            crater_y = random.randint(10, self.radius * 2 - 10)
            crater_radius = random.randint(5, self.radius // 4)
            crater_color = (max(self.base_color[0] - 40, 0), max(self.base_color[1] - 40, 0), max(self.base_color[2] - 40, 0))
            pygame.draw.circle(planet_surface, crater_color, (crater_x, crater_y), crater_radius)

        return planet_surface

    def draw(self, screen):
        """Draw the planet on the given Pygame screen."""
        screen.blit(self.surface, (self.x - self.radius, self.y - self.radius))
