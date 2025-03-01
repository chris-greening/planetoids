import pygame
import random
import math
from config import WIDTH, HEIGHT, WHITE, ORANGE

class Asteroid:
    def __init__(self, x=None, y=None, size=80, stage=3):
        """Initialize an asteroid with position, size, and split stage."""
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        self.size = size  # Size of the asteroid
        self.stage = stage  # 3 = large, 2 = medium, 1 = small, 0 = disappears
        self.sides = random.randint(7, 12)  # Number of points
        self.angle = random.uniform(0, 360)  # Movement direction
        self.base_speed = random.uniform(1, 3)  # Normal speed
        self.speed = self.base_speed  # Current speed (adjusted by slowdown)

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

    def update(self, game_state):
        """Moves the asteroid across the screen, applying slowdown if active."""
        slowdown_factor = 0.3 if game_state.asteroid_slowdown_active else 1  # Slowdown multiplier

        angle_rad = math.radians(self.angle)
        dx = math.cos(angle_rad) * self.base_speed * slowdown_factor
        dy = math.sin(angle_rad) * self.base_speed * slowdown_factor

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

            # Give new asteroids a small random speed boost
            new_speed = min(self.base_speed * 1.2, 5)  # Slightly faster but capped

            # Offset their angles so they don’t overlap
            angle_variation = random.uniform(-20, 20)

            # Create two new asteroids moving in different directions
            asteroid1 = Asteroid(
                x=self.x + random.randint(-5, 5),
                y=self.y + random.randint(-5, 5),
                size=new_size,
                stage=new_stage
            )
            asteroid2 = Asteroid(
                x=self.x + random.randint(-5, 5),
                y=self.y + random.randint(-5, 5),
                size=new_size,
                stage=new_stage
            )

            # Adjust their movement speeds and directions
            asteroid1.base_speed = new_speed
            asteroid2.base_speed = new_speed
            asteroid1.angle = (self.angle + angle_variation) % 360
            asteroid2.angle = (self.angle - angle_variation) % 360

            return [asteroid1, asteroid2]

        return []  # If the asteroid is at the smallest stage, it disappears

class ExplodingAsteroid(Asteroid):
    """Asteroid that explodes and destroys nearby asteroids upon impact."""
    def __init__(self, x=None, y=None, size=80, stage=3, explosion_radius=300):
        super().__init__(x, y, size, stage)
        self.explosion_radius = explosion_radius

    def draw(self, screen):
        """Draw the asteroid with an orange color fill and outline."""
        pygame.draw.polygon(screen, ORANGE, self.shape)  # Filled polygon
        pygame.draw.polygon(screen, (255, 100, 0), self.shape, 2)  # Slightly darker outline

    def explode(self, asteroids):
        """Destroys all asteroids within a certain radius."""
        destroyed_asteroids = []

        for asteroid in asteroids:
            if asteroid is not self:
                distance = math.sqrt((asteroid.x - self.x) ** 2 + (asteroid.y - self.y) ** 2)
                if distance <= self.explosion_radius:
                    destroyed_asteroids.append(asteroid)

        return destroyed_asteroids  # Return list of asteroids to remove