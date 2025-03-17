import random
import math

import pygame

from planetoids.core.config import config

class Particle:
    def __init__(self, x, y, angle, speed, game_state):
        """Create a particle at the given position, moving in the given direction."""
        self.x = x
        self.y = y
        self.size = random.uniform(2, 4)  # Random initial size
        self.alpha = 255  # Full opacity at start
        self.lifetime = random.randint(15, 30)  # Frames before disappearing
        self.game_state = game_state

        # Particle moves slightly outward from the ship’s direction
        angle_rad = math.radians(angle + random.uniform(-15, 15))  # Slight angle variation
        self.velocity_x = math.cos(angle_rad) * speed * 0.5
        self.velocity_y = math.sin(angle_rad) * speed * 0.5

    def update(self):
        """Move the particle using delta time scaling and reduce size & opacity over time."""
        self.x -= self.velocity_x * self.game_state.dt * 60  # ✅ Scale movement with dt
        self.y -= self.velocity_y * self.game_state.dt * 60

        self.size *= 0.95 ** (self.game_state.dt * 60)  # ✅ Ensure consistent shrink rate across FPS
        self.alpha -= 10 * self.game_state.dt * 60  # ✅ Scale fade effect
        self.lifetime -= self.game_state.dt * 60  # ✅ Scale lifetime reduction

    def draw(self, screen):
        """Draw particle with fading effect."""
        if self.lifetime > 0 and self.alpha > 0:
            faded_color = (config.ORANGE[0], config.ORANGE[1], config.ORANGE[2], max(self.alpha, 0))
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, faded_color, (int(self.size), int(self.size)), int(self.size))
            screen.blit(particle_surface, (self.x, self.y))
