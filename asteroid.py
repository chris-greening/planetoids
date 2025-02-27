import pygame
import random
import math
from config import WIDTH, HEIGHT, WHITE

class Asteroid:
    def __init__(self, x=None, y=None, size=80, stage=3):
        """Initialize an asteroid with position, size, and split stage."""
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        self.size = size  # Size of the asteroid
        self.stage = stage  # 3 = large, 2 = medium, 1 = small, 0 = disappears
        self.sides = random.randint(7, 12)  # Number of points
        self.angle = random.uniform(0, 360)  # Movement direction
        self.speed = random.uniform(1, 3)  # Movement speed

        # Generate shape *once* and store relative offsets
        self.shape_offsets = self._generate_jagged_shape()
        self.update_shape()

    def _generate_jagged_shape(self):
        """Creates a jagged asteroid shape with fixed offsets."""
        jitter_amount = self.size // 3  # Edge variation
        offsets = []
        for i in range(self.sides):
            angle = (i / self.sides) * 2 * math.pi
            jitter = random.randint(-jitter_amount, jitter_amount)
            radius = self.size + jitter
            x_offset = math.cos(angle) * radius
            y_offset = math.sin(angle) * radius
            offsets.append((x_offset, y_offset))
        return offsets  # Store relative offsets so shape remains constant

    def update_shape(self):
        """Update shape based on current position while keeping offsets constant."""
        self.shape = [(self.x + ox, self.y + oy) for ox, oy in self.shape_offsets]

    def update(self):
        """Moves the asteroid across the screen and ensures wraparound."""
        angle_rad = math.radians(self.angle)
        dx = math.cos(angle_rad) * self.speed
        dy = math.sin(angle_rad) * self.speed

        # Update position
        self.x += dx
        self.y += dy

        # Screen wraparound logic
        if self.x < -self.size:
            self.x = WIDTH + self.size
        elif self.x > WIDTH + self.size:
            self.x = -self.size

        if self.y < -self.size:
            self.y = HEIGHT + self.size
        elif self.y > HEIGHT + self.size:
            self.y = -self.size

        # Update shape based on new position without changing offsets
        self.update_shape()

    def draw(self, screen):
        """Draw the asteroid with an outline (wireframe)."""
        pygame.draw.polygon(screen, WHITE, self.shape, 1)

    def split(self):
        """Splits the asteroid into two smaller ones if possible."""
        if self.stage > 1:  # Only split if not already at the smallest stage
            new_size = self.size // 2
            new_stage = self.stage - 1

            # Offset spawn positions slightly
            return [
                Asteroid(self.x + new_size // 2, self.y, new_size, new_stage),
                Asteroid(self.x - new_size // 2, self.y, new_size, new_stage)
            ]
        return []  # Instead of None, return an empty list

