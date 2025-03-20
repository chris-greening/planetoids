import math
import random
import collections

import pygame

from planetoids.core.config import config

class Bullet:
    def __init__(self, game_state, x, y, angle, ricochet=False, color=config.RED, radius=7):
        self.game_state = game_state
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 15
        self.lifetime = 40
        self.ricochet = ricochet
        self.piercing = ricochet
        self.color = color
        self.radius = radius

        self.trail = collections.deque(maxlen=7)  # Number of previous frames to track

    def update(self):
        """Moves the bullet forward using delta time scaling and handles lifetime."""
        angle_rad = math.radians(self.angle)

        self.x += math.cos(angle_rad) * self.speed * self.game_state.dt * 60
        self.y -= math.sin(angle_rad) * self.speed * self.game_state.dt * 60

        self.lifetime -= self.game_state.dt * 60

        # 🔹 Store position for trail effect
        self.trail.append((self.x, self.y))

        # Screen wraparound
        self.x %= config.WIDTH
        self.y %= config.HEIGHT

    def draw(self, screen):
        """Draw the bullet with a glowing trail effect."""
        color = self.color
        radius = self.radius
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))  # Gradual fade-out
            trail_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (color[0], color[1], color[2], alpha), (3, 3), 3)
            screen.blit(trail_surface, (int(tx) - 3, int(ty) - 3))
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), radius)

    def on_hit_asteroid(self, asteroid):
        """Handles bullet behavior when hitting an asteroid."""
        if self.ricochet:
            # Change direction randomly upon ricochet
            self.angle = (self.angle + random.uniform(135, 225)) % 360
            self.bounced = True  # Track ricochet event
        # If not ricochet, just continue since piercing allows travel through