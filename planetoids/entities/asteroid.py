import random
import math

import pygame

from planetoids.core.config import WIDTH, HEIGHT, WHITE, ORANGE, DARK_ORANGE
from planetoids.entities.particle import Particle

class Asteroid:
    asteroid_types = []
    spawn_chance = 1.0

    def __init__(self, x=None, y=None, size=120, stage=3):
        """Initialize an asteroid with position, size, and split stage."""
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        self.size = size  # Size of the asteroid
        self.stage = stage  # 3 = large, 2 = medium, 1 = small, 0 = disappears
        self.sides = random.randint(7, 12)  # Number of points
        self.angle = random.uniform(0, 360)  # Movement direction
        self.base_speed = random.uniform(2, 4)  # Normal speed
        self.speed = self.base_speed  # Current speed (adjusted by slowdown)

        # Generate shape *once* and store relative offsets
        self.shape_offsets = self._generate_jagged_shape()
        self.update_shape()

    def __new__(cls, *args, **kwargs):
        """Ensures the base class registers itself on first reference"""
        if cls is Asteroid and Asteroid not in Asteroid.asteroid_types:
            Asteroid.asteroid_types.append(Asteroid)
        return super().__new__(cls)

    def __init_subclass__(cls, **kwargs):
        """Automatically registers subclasses"""
        super().__init_subclass__(**kwargs)
        if cls not in Asteroid.asteroid_types:
            Asteroid.asteroid_types.append(cls)

    def split(self):
        """Splits into two smaller asteroids with weighted chance"""
        if self.stage > 1:
            new_size = self.size // 2
            new_stage = self.stage - 1

            asteroid_class_1 = self._get_asteroid_type()
            asteroid_class_2 = self._get_asteroid_type()

            asteroid1 = asteroid_class_1(self.x + random.randint(-5, 5), self.y + random.randint(-5, 5), size=new_size, stage=new_stage)
            asteroid2 = asteroid_class_2(self.x + random.randint(-5, 5), self.y + random.randint(-5, 5), size=new_size, stage=new_stage)

            return [asteroid1, asteroid2]

        return []

    @classmethod
    def _get_asteroid_type(cls):
        """Selects an asteroid type based on weighted probabilities"""
        asteroid_classes = cls.asteroid_types
        weights = [subclass.spawn_chance for subclass in asteroid_classes]
        return random.choices(asteroid_classes, weights=weights, k=1)[0]

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
        asteroid_slowdown_active = False if game_state is None else game_state.asteroid_slowdown_active
        slowdown_factor = 0.3 if asteroid_slowdown_active else 1  # Slowdown multiplier

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

class ExplodingAsteroid(Asteroid):
    """Asteroid that explodes, destroying nearby asteroids and playing an explosion animation."""
    spawn_chance = 0.05

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

# class IceAsteroid(Asteroid):
#     """Asteroid that leaves a visible ice trail and slows the player when touched."""

#     def __init__(self, x=None, y=None, size=80, stage=3):
#         super().__init__(x, y, size, stage)
#         self.ice_trail = []  # Stores ice trail positions
#         self.trail_max_length = 50  # **Increase trail length**
#         self.ice_slowdown_factor = 0.6  # Reduces player speed by 40%
#         self.trail_spacing = 5  # **Distance between trail drops**

#     def update(self, game_state):
#         """Move the asteroid and leave an ice trail behind it."""
#         super().update(game_state)

#         # **Only add a new ice patch every few frames (reduces clutter)**
#         if not self.ice_trail or math.hypot(self.x - self.ice_trail[-1][0], self.y - self.ice_trail[-1][1]) > self.trail_spacing:
#             self.ice_trail.append((self.x, self.y))

#         # **Limit Trail Length**
#         if len(self.ice_trail) > self.trail_max_length:
#             self.ice_trail.pop(0)  # Remove oldest ice patch

#         # **Check if Player is Touching Ice**
#         player_on_ice = False
#         for ice_x, ice_y in self.ice_trail:
#             if math.sqrt((game_state.player.x - ice_x) ** 2 + (game_state.player.y - ice_y) ** 2) < self.size / 2:
#                 player_on_ice = True

#                 # **Gradual slowdown instead of instant velocity drop**
#                 if not game_state.player.slowed_by_ice:
#                     game_state.player.velocity_x *= 0.85  # Reduce speed smoothly
#                     game_state.player.velocity_y *= 0.85
#                     game_state.player.slowed_by_ice = True  # Mark slowdown applied

#                 # **Ensure player still has some movement**
#                 min_speed = 1.5  # Minimum movement speed
#                 if abs(game_state.player.velocity_x) < min_speed:
#                     game_state.player.velocity_x = min_speed if game_state.player.velocity_x > 0 else -min_speed
#                 if abs(game_state.player.velocity_y) < min_speed:
#                     game_state.player.velocity_y = min_speed if game_state.player.velocity_y > 0 else -min_speed

#         # **If Player Leaves Ice, Remove Slowdown**
#         if not player_on_ice:
#             game_state.player.slowed_by_ice = False



#     def draw(self, screen):
#         """Draw the asteroid and its ice trail with better visuals."""

#         ICE_BLUE = (173, 216, 230, 100)  # Light blue with transparency
#         DARK_ICE = (100, 149, 237)  # Darker blue for asteroid outline

#         ice_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Enable transparency

#         # **Draw Ice Trail (Wider and Transparent)**
#         for i, (ice_x, ice_y) in enumerate(self.ice_trail):
#             size = 18 - (i // 3)  # Larger initial size, gradually smaller
#             size = max(size, 10)  # Minimum size for visibility
#             alpha = max(200 - (i * 5), 50)  # Fades out over time

#             # **Transparent Ice Trail**
#             pygame.draw.circle(ice_surface, (173, 216, 230, alpha), (int(ice_x), int(ice_y)), size)

#         # **Blit the transparent surface onto the screen**
#         screen.blit(ice_surface, (0, 0))

#         # **Draw the Ice Asteroid**
#         pygame.draw.polygon(screen, ICE_BLUE[:3], self.shape)  # Remove alpha for asteroid
#         pygame.draw.polygon(screen, DARK_ICE, self.shape, 2)  # Outline
