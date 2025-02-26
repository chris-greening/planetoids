import random
import math
import constants
import pygame

# Asteroid class
class Asteroid:
    def __init__(self):
        self.x = random.choice([random.randint(0, 100), random.randint(constants.WIDTH - 100, constants.WIDTH)])
        self.y = random.choice([random.randint(0, 100), random.randint(constants.HEIGHT - 100, constants.HEIGHT)])
        self.size = random.randint(30, 50)
        self.angle = random.uniform(0, 360)
        self.speed = random.uniform(1, 3)

    def update(self):
        angle_rad = math.radians(self.angle)
        self.x += math.cos(angle_rad) * self.speed
        self.y -= math.sin(angle_rad) * self.speed

        # Screen wraparound
        self.x %= constants.WIDTH
        self.y %= constants.HEIGHT

    def draw(self, screen):
        pygame.draw.circle(screen, constants.WHITE, (int(self.x), int(self.y)), self.size)
