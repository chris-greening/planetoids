import math
import pygame
import config

# Bullet class
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 8
        self.lifetime = 60  # Frames

    def update(self):
        angle_rad = math.radians(self.angle)
        self.x += math.cos(angle_rad) * self.speed
        self.y -= math.sin(angle_rad) * self.speed

        # Screen wraparound
        self.x %= config.WIDTH
        self.y %= config.HEIGHT

        self.lifetime -= 1  # Reduce lifetime

    def draw(self, screen):
        pygame.draw.circle(screen, config.WHITE, (int(self.x), int(self.y)), 3)
