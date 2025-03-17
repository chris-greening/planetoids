import math
import random

import pygame

from planetoids.core.config import config

class Bullet:
    def __init__(self, game_state, x, y, angle, ricochet=False):
        self.game_state = game_state
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 8
        self.lifetime = 60
        self.ricochet = ricochet
        self.piercing = ricochet

    def update(self):
        """Moves the bullet forward using delta time scaling and handles lifetime."""
        angle_rad = math.radians(self.angle)

        self.x += math.cos(angle_rad) * self.speed * self.game_state.dt * 60
        self.y -= math.sin(angle_rad) * self.speed * self.game_state.dt * 60

        self.lifetime -= self.game_state.dt * 60

        self.x %= config.WIDTH
        self.y %= config.HEIGHT

    def on_hit_asteroid(self, asteroid):
        """Handles bullet behavior when hitting an asteroid."""
        if self.ricochet:
            # Change direction randomly upon ricochet
            self.angle = (self.angle + random.uniform(135, 225)) % 360
            self.bounced = True  # Track ricochet event
        # If not ricochet, just continue since piercing allows travel through

    def draw(self, screen):
        """Draw the bullet"""
        pygame.draw.circle(screen, config.RED, (int(self.x), int(self.y)), 5)
