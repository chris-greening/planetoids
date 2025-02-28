import math
import pygame
from config import RED

class Bullet:
    def __init__(self, x, y, angle, ricochet=False):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 8
        self.lifetime = 60
        self.ricochet = ricochet

    def update(self):
        """Move the bullet and reduce its lifetime"""
        angle_rad = math.radians(self.angle)
        self.x += math.cos(angle_rad) * self.speed
        self.y -= math.sin(angle_rad) * self.speed
        self.lifetime -= 1

    def draw(self, screen):
        """Draw the bullet"""
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 3)
