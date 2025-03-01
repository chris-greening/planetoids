import pygame
import random
import math
from config import WIDTH, HEIGHT, WHITE, ORANGE, DARK_ORANGE
from particle import Particle

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
            if random.random() < 0.02:
                asteroid1 = ExplodingAsteroid(
                    x=self.x + random.randint(-5, 5),
                    y=self.y + random.randint(-5, 5),
                    size=new_size,
                    stage=new_stage
                )
            else:
                asteroid1 = Asteroid(
                    x=self.x + random.randint(-5, 5),
                    y=self.y + random.randint(-5, 5),
                    size=new_size,
                    stage=new_stage
                )
            if random.random() < 0.02:
                asteroid2 = ExplodingAsteroid(
                    x=self.x + random.randint(-5, 5),
                    y=self.y + random.randint(-5, 5),
                    size=new_size,
                    stage=new_stage
                )
            else:
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
    """Asteroid that explodes, destroying nearby asteroids and playing an explosion animation."""

    def __init__(self, x=None, y=None, size=80, stage=3, explosion_radius=200):  # Bigger explosion
        super().__init__(x, y, size, stage)
        self.explosion_radius = explosion_radius
        self.exploding = False
        self.explosion_particles = []
        self.fragments = []
        self.explosion_timer = 40  # Longer explosion duration

    def explode(self, asteroids):
        """Triggers explosion effect and destroys nearby asteroids."""
        if not self.exploding:
            self.exploding = True
            self._generate_explosion()

        destroyed_asteroids = [a for a in asteroids if self._is_within_explosion_radius(a)]
        return destroyed_asteroids

    def _generate_explosion(self):
        """Generates explosion fragments and particles."""
        angle_rad = math.radians(self.angle)

        # Generate asteroid fragments (now bigger and faster)
        front = (self.x + math.cos(angle_rad) * self.size, self.y - math.sin(angle_rad) * self.size)
        left = (self.x + math.cos(angle_rad + 2.5) * self.size * 0.6, self.y - math.sin(angle_rad + 2.5) * self.size * 0.6)
        right = (self.x + math.cos(angle_rad - 2.5) * self.size * 0.6, self.y - math.sin(angle_rad - 2.5) * self.size * 0.6)

        self.fragments = [
            {"pos": front, "vel": (random.uniform(-4, 4), random.uniform(-4, 4))},  # Faster movement
            {"pos": left, "vel": (random.uniform(-4, 4), random.uniform(-4, 4))},
            {"pos": right, "vel": (random.uniform(-4, 4), random.uniform(-4, 4))}
        ]

        # Generate explosion particles (increased amount)
        self.explosion_particles = [
            Particle(self.x, self.y, random.uniform(0, 360), random.uniform(2, 5))  # Bigger explosion
            for _ in range(40)
        ]

    def _is_within_explosion_radius(self, asteroid):
        """Checks if another asteroid is within explosion range."""
        distance = math.sqrt((asteroid.x - self.x) ** 2 + (asteroid.y - self.y) ** 2)
        return distance <= self.explosion_radius

    def update_explosion(self):
        """Updates explosion animation each frame."""
        if self.exploding:
            for fragment in self.fragments:
                fragment["pos"] = (fragment["pos"][0] + fragment["vel"][0], fragment["pos"][1] + fragment["vel"][1])

            for particle in self.explosion_particles:
                particle.update()

            self.explosion_timer -= 1  # Countdown

            if self.explosion_timer <= 0:
                self.exploding = False  # Mark explosion as done

    def draw(self, screen):
        """Draw the asteroid as an orange polygon, or explosion if exploding."""
        ORANGE = (255, 165, 0)
        DARK_ORANGE = (255, 100, 0)

        if not self.exploding:
            pygame.draw.polygon(screen, ORANGE, self.shape)  # Filled polygon
            pygame.draw.polygon(screen, DARK_ORANGE, self.shape, 2)  # Outline
        else:
            self.draw_explosion(screen)  # Draw explosion animation

    def draw_explosion(self, screen):
        """Draws explosion fragments, particles, and a properly sized shockwave."""

        # Colors for the explosion
        ORANGE = (255, 165, 0)
        RED_ORANGE = (255, 69, 0)

        # **Draw Fragments Only Within Explosion Radius**
        for fragment in self.fragments:
            fx, fy = fragment["pos"]
            if math.sqrt((fx - self.x) ** 2 + (fy - self.y) ** 2) <= self.explosion_radius:
                pygame.draw.circle(screen, ORANGE, (int(fx), int(fy)), 4)

        # **Only Draw Particles Inside Explosion Radius**
        for particle in self.explosion_particles:
            px, py = particle.x, particle.y
            if math.sqrt((px - self.x) ** 2 + (py - self.y) ** 2) <= self.explosion_radius:
                particle.draw(screen)

        # **Controlled Shockwave Expansion**
        max_radius = self.explosion_radius * 0.6  # Max shockwave size = 60% of explosion radius
        growth_per_frame = max_radius / 40  # Grows evenly over explosion duration
        shockwave_radius = min((40 - self.explosion_timer) * growth_per_frame, max_radius)

        if shockwave_radius > 0:
            pygame.draw.circle(screen, RED_ORANGE, (int(self.x), int(self.y)), int(shockwave_radius), 2)
