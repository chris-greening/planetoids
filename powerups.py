import pygame
import random
import time
from config import WIDTH, HEIGHT, CYAN

class PowerUp:
    """Base class for all power-ups."""

    def __init__(self, x, y, radius=10):
        """Initialize power-up properties."""
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = random.uniform(-1.5, 1.5)
        self.speed_y = random.uniform(-1.5, 1.5)
        self.spawn_time = time.time()  # Store the spawn time

    def update(self):
        """Move the power-up and handle expiration."""
        self.x += self.speed_x
        self.y += self.speed_y

        # Screen wraparound
        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self, screen):
        """Draw the power-up, with a blinking effect before expiration."""
        if self.is_expired():
            return  # Do not draw expired power-ups

        # Blinking effect (start blinking after 6 seconds, every 0.2s)
        elapsed_time = time.time() - self.spawn_time
        if elapsed_time > 10 and int(elapsed_time * 5) % 2 == 0:
            return  # Skip drawing to create blinking effect

        # Outer glow effect
        pygame.draw.circle(screen, (0, 100, 255), (int(self.x), int(self.y)), self.radius + 4, 1)
        pygame.draw.circle(screen, (0, 150, 255), (int(self.x), int(self.y)), self.radius + 2, 1)

        # Main powerup shape
        pygame.draw.circle(screen, CYAN, (int(self.x), int(self.y)), self.radius)

        # Draw powerup type (letter)
        font = pygame.font.Font(None, 20)
        text = font.render(self.get_symbol(), True, (0, 0, 0))
        screen.blit(text, (self.x - 5, self.y - 5))

    def is_expired(self):
        """Check if the power-up should disappear."""
        return time.time() - self.spawn_time > 15  # Disappear after 10 seconds

class TrishotPowerUp(PowerUp):
    """Trishot power-up that enables triple bullets for a limited time."""

    def __init__(self, x, y):
        """Initialize the trishot power-up."""
        super().__init__(x, y)  # Use parent class constructor

    def apply(self, player):
        """Grants the player trishot mode."""
        player.enable_trishot()

    def get_symbol(self):
        """Display 'T' inside the power-up."""
        return "T"

class ShieldPowerUp(PowerUp):
    """Shield power-up that reenables player's shield"""

    def __init__(self, x, y):
        """Initialize the shield power-up."""
        super().__init__(x, y)  # Use parent class constructor

    def apply(self, player):
        """Grants the player shield."""
        player.activate_shield()

    def get_symbol(self):
        """Display 'S' inside the power-up."""
        return "S"

class QuadShotPowerUp(PowerUp):
    """QuadShot power-up that enables four-directional bullets for a limited time."""

    def apply(self, player):
        """Grants the player QuadShot mode."""
        player.enable_quadshot()

    def get_symbol(self):
        return "Q"  # Displays "Q" inside the power-up
