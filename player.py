import pygame
import math
import random
from config import WIDTH, HEIGHT, WHITE, ORANGE
from particle import Particle  # Import the new particle class

class Player:
    def __init__(self):
        """Initialize player with movement settings."""
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.1
        self.max_speed = 5
        self.size = 20  # Ship size
        self.thrusting = False
        self.particles = []  # Stores exhaust particles

    def update(self, keys):
        """Handles movement, rotation, and particle effects."""
        self.thrusting = False  # Reset thrust effect

        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5
        if keys[pygame.K_UP]:  # Apply thrust
            self.thrusting = True
            angle_rad = math.radians(self.angle)
            self.velocity_x += math.cos(angle_rad) * self.acceleration
            self.velocity_y -= math.sin(angle_rad) * self.acceleration

            # Limit speed
            speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            if speed > self.max_speed:
                factor = self.max_speed / speed
                self.velocity_x *= factor
                self.velocity_y *= factor

            # Generate exhaust particles
            self._generate_exhaust()

        # Apply movement
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Screen wraparound
        self.x %= WIDTH
        self.y %= HEIGHT

        # Update and remove expired particles
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()

    def draw(self, screen):
        """Draws the player ship and particles."""
        angle_rad = math.radians(self.angle)

        # Triangle points relative to the center
        front = (self.x + math.cos(angle_rad) * self.size, self.y - math.sin(angle_rad) * self.size)
        left = (self.x + math.cos(angle_rad + 2.5) * self.size * 0.6, self.y - math.sin(angle_rad + 2.5) * self.size * 0.6)
        right = (self.x + math.cos(angle_rad - 2.5) * self.size * 0.6, self.y - math.sin(angle_rad - 2.5) * self.size * 0.6)

        # Draw particles first (so they appear behind the ship)
        for particle in self.particles:
            particle.draw(screen)

        # Draw ship
        pygame.draw.polygon(screen, WHITE, [front, left, right], 1)

        # Draw thruster effect if accelerating
        if self.thrusting:
            self._draw_thruster(screen, angle_rad, left, right)

    def _generate_exhaust(self):
        """Adds new particles behind the ship."""
        angle_rad = math.radians(self.angle)
        exhaust_x = self.x - math.cos(angle_rad) * self.size * 1.2
        exhaust_y = self.y + math.sin(angle_rad) * self.size * 1.2
        self.particles.append(Particle(exhaust_x, exhaust_y, self.angle, random.uniform(1, 3)))

    def _draw_thruster(self, screen, angle_rad, left, right):
        """Draws a flickering thrust effect behind the ship."""
        flicker_size = random.uniform(self.size * 0.4, self.size * 0.6)
        thruster_tip = (
            self.x - math.cos(angle_rad) * flicker_size * 2,
            self.y + math.sin(angle_rad) * flicker_size * 2
        )
        pygame.draw.polygon(screen, ORANGE, [thruster_tip, left, right])
