import math
import pygame
import config

# Player class
class Player:
    def __init__(self):
        self.x = config.WIDTH / 2
        self.y = config.HEIGHT / 2
        self.angle = 0  # Facing right (0 degrees)
        self.speed = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.1
        self.max_speed = 5
        self.size = 20  # Triangle size

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += 5  # Rotate counterclockwise
        if keys[pygame.K_RIGHT]:
            self.angle -= 5  # Rotate clockwise
        if keys[pygame.K_UP]:
            # Apply acceleration in the direction the ship is facing
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
        self.x %= config.WIDTH
        self.y %= config.HEIGHT

    def draw(self, screen):
        # Calculate triangle points
        angle_rad = math.radians(self.angle)
        front = (self.x + math.cos(angle_rad) * self.size, self.y - math.sin(angle_rad) * self.size)
        left = (self.x + math.cos(angle_rad + 2.5) * self.size * 0.6, self.y - math.sin(angle_rad + 2.5) * self.size * 0.6)
        right = (self.x + math.cos(angle_rad - 2.5) * self.size * 0.6, self.y - math.sin(angle_rad - 2.5) * self.size * 0.6)

        # Draw the ship as a triangle
        pygame.draw.polygon(screen, config.WHITE, [front, left, right])
