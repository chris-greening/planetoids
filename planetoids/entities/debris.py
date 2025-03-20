import random
import pygame
import math

from planetoids.core.config import config

class Debris:
    """Small asteroid fragments that scatter upon impact."""
    def __init__(self, x, y, angle, speed, lifetime=30):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.lifetime = lifetime
        self.size = random.randint(2, 4)  # Small fragment sizes

        # Random color similar to asteroids
        self.color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))

    def update(self, dt):
        """Move debris in the given direction and fade out over time."""
        angle_rad = math.radians(self.angle)
        self.x += math.cos(angle_rad) * self.speed * dt * 60
        self.y -= math.sin(angle_rad) * self.speed * dt * 60
        self.lifetime -= dt * 60  # Reduce lifetime

    def draw(self, screen):
        """Draw debris as tiny asteroid fragments."""
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
