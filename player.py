import pygame
import math
from config import WIDTH, HEIGHT, WHITE
import random

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
        self.thrusting = False
        self.size = 20  # Ship size

    def update(self, keys):
        """Handles movement and rotation."""
        self.thrusting = False
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5
        if keys[pygame.K_UP]:
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

        # Apply movement
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Screen wraparound
        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self, screen):
        """Draws the player ship as an outlined triangle."""
        angle_rad = math.radians(self.angle)

        # Triangle points relative to the center
        front = (self.x + math.cos(angle_rad) * self.size, self.y - math.sin(angle_rad) * self.size)
        left = (self.x + math.cos(angle_rad + 2.5) * self.size * 0.6, self.y - math.sin(angle_rad + 2.5) * self.size * 0.6)
        right = (self.x + math.cos(angle_rad - 2.5) * self.size * 0.6, self.y - math.sin(angle_rad - 2.5) * self.size * 0.6)

        pygame.draw.polygon(screen, WHITE, [front, left, right], 1)  # Outline only, no fill

        if self.thrusting:
            self._draw_thruster(screen, angle_rad, left, right)

    def _draw_thruster(self, screen, angle_rad, left, right):
        """Draws a flickering thrust effect behind the ship."""
        # Calculate thrust flicker effect
        flicker_size = random.uniform(self.size * 0.4, self.size * 0.6)

        # Thruster position (slightly behind ship)
        thruster_tip = (
            self.x - math.cos(angle_rad) * flicker_size * 2,
            self.y + math.sin(angle_rad) * flicker_size * 2
        )

        # Draw thruster triangle (glowing orange effect)
        pygame.draw.polygon(screen, WHITE, [thruster_tip, left, right])