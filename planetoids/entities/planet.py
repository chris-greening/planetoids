import random

import pygame

from planetoids.core.config import WIDTH, HEIGHT

class Planet:
    def __init__(self):
        """Generate a random planet with a position, color, and craters."""
        self.radius = random.randint(50, 150)  # Base planet size
        self.x = random.randint(200, WIDTH - 200)
        self.y = random.randint(200, HEIGHT - 200)
        self.base_color = (
            random.randint(50, 255),  # R
            random.randint(50, 255),  # G
            random.randint(50, 255),  # B
        )
        self.surface = self._generate_planet_surface()

    def _generate_planet_surface(self):
        """Creates a Pygame surface with a jittered, rough edge for the planet."""
        planet_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

        # Create a rough edge using random jitter
        num_points = 50  # More points = smoother jittered edge
        points = []
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi  # Full circle
            jitter = random.randint(-8, 8)  # Amount of variation on the edge
            r = self.radius + jitter  # Jittered radius
            x = self.radius + math.cos(angle) * r
            y = self.radius + math.sin(angle) * r
            points.append((x, y))

        # Draw the jittered edge as a polygon
        pygame.draw.polygon(planet_surface, self.base_color, points)

        # Draw some random craters
        for _ in range(random.randint(3, 7)):
            crater_x = random.randint(10, self.radius * 2 - 10)
            crater_y = random.randint(10, self.radius * 2 - 10)
            crater_radius = random.randint(5, self.radius // 4)
            crater_color = (
                max(self.base_color[0] - 40, 0),
                max(self.base_color[1] - 40, 0),
                max(self.base_color[2] - 40, 0)
            )
            pygame.draw.circle(planet_surface, crater_color, (crater_x, crater_y), crater_radius)

        return planet_surface

    def draw(self, screen):
        """Draw the planet on the given Pygame screen."""
        screen.blit(self.surface, (self.x - self.radius, self.y - self.radius))
