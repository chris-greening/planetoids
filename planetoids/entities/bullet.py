import math
import random

import pygame

from planetoids.core.config import RED, WIDTH, HEIGHT

class Bullet:
    def __init__(self, x, y, angle, ricochet=False):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 8
        self.lifetime = 60
        self.ricochet = ricochet
        self.piercing = ricochet

    def update(self, dt):
        """Moves the bullet forward using delta time scaling and handles lifetime."""
        angle_rad = math.radians(self.angle)

        # ✅ Scale movement using dt to ensure consistent speed
        self.x += math.cos(angle_rad) * self.speed * dt * 60
        self.y -= math.sin(angle_rad) * self.speed * dt * 60

        # ✅ Scale bullet lifetime decrement by dt
        self.lifetime -= dt * 60

        # ✅ Screen wraparound (bullets also loop)
        self.x %= WIDTH
        self.y %= HEIGHT

    def on_hit_asteroid(self, asteroid):
        """Handles bullet behavior when hitting an asteroid."""
        if self.ricochet:
            # Change direction randomly upon ricochet
            self.angle = (self.angle + random.uniform(135, 225)) % 360
            self.bounced = True  # Track ricochet event
        # If not ricochet, just continue since piercing allows travel through

    def draw(self, screen):
        """Draw the bullet"""
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)
