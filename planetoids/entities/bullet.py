import math
import random
import collections

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

        # 🔹 Stores the last few positions for the trail effect
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
        # 🔹 Draw fading trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))  # Gradual fade-out
            trail_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (255, 50, 50, alpha), (3, 3), 3)
            screen.blit(trail_surface, (int(tx) - 3, int(ty) - 3))

        # 🔹 Draw bullet
        pygame.draw.circle(screen, config.RED, (int(self.x), int(self.y)), 5)

    def on_hit_asteroid(self, asteroid):
        """Handles bullet behavior when hitting an asteroid."""
        if self.ricochet:
            # Change direction randomly upon ricochet
            self.angle = (self.angle + random.uniform(135, 225)) % 360
            self.bounced = True  # Track ricochet event
        # If not ricochet, just continue since piercing allows travel through