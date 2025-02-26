import random
import math
import config
import pygame

# Asteroid class
class Asteroid:
    def __init__(self):
        self.x = random.choice([random.randint(0, 100), random.randint(config.WIDTH - 100, config.WIDTH)])
        self.y = random.choice([random.randint(0, 100), random.randint(config.HEIGHT - 100, config.HEIGHT)])
        self.size = random.randint(30, 50)
        self.angle = random.uniform(0, 360)
        self.speed = random.uniform(1, 3)

    def update(self):
        angle_rad = math.radians(self.angle)
        self.x += math.cos(angle_rad) * self.speed
        self.y -= math.sin(angle_rad) * self.speed

        # Screen wraparound
        self.x %= config.WIDTH
        self.y %= config.HEIGHT

    def draw(self, screen):
        pygame.draw.circle(screen, config.WHITE, (int(self.x), int(self.y)), self.size)
