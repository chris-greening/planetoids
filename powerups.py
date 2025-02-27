import pygame
import random
from config import WIDTH, HEIGHT, WHITE

class PowerUp:
    """Represents a floating power-up that grants abilities."""
    
    TYPES = ["trishot"]  # Expandable list of powerups

    def __init__(self, x, y, power_type=None):
        """Initialize powerup with a random type if none is provided."""
        self.x = x
        self.y = y
        self.radius = 10  # Size of the power-up
        self.type = power_type if power_type else random.choice(PowerUp.TYPES)
        self.speed_x = random.uniform(-1.5, 1.5)  # Random float speed
        self.speed_y = random.uniform(-1.5, 1.5)

    def update(self):
        """Move the power-up around the screen."""
        self.x += self.speed_x
        self.y += self.speed_y

        # Screen wraparound (like asteroids)
        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self, screen):
        """Draw the power-up as a small circle with its type indicated."""
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 1)

        # Draw text label (abbreviated)
        font = pygame.font.Font(None, 20)
        text = font.render(self.type[0].upper(), True, WHITE)
        screen.blit(text, (self.x - 5, self.y - 5))
