import pygame
import math
from config import WIDTH, HEIGHT, WHITE

class Bullet:
    bullets = []  # Tracks all bullets

    def __init__(self, x, y, angle):
        """Initialize bullet instance."""
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 8
        self.lifetime = 60
        Bullet.bullets.append(self)  # Automatically track bullets

    @classmethod
    def create(cls, x, y, angle):
        """Factory method for instantiating a bullet."""
        return cls(x, y, angle)

    def update(self):
        """Move the bullet and reduce its lifetime."""
        angle_rad = math.radians(self.angle)
        self.x += math.cos(angle_rad) * self.speed
        self.y -= math.sin(angle_rad) * self.speed

        # Wraparound
        self.x %= WIDTH
        self.y %= HEIGHT

        self.lifetime -= 1

    def draw(self, screen):
        """Draw the bullet as a small circle."""
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 3)

    @classmethod
    def update_all(cls):
        """Update all bullets and remove expired ones."""
        for bullet in cls.bullets:
            bullet.update()
        cls.bullets = [bullet for bullet in cls.bullets if bullet.lifetime > 0]  # Cleanup

    @classmethod
    def draw_all(cls, screen):
        """Draw all bullets."""
        for bullet in cls.bullets:
            bullet.draw(screen)
