import pygame
import random
from config import WIDTH, HEIGHT, WHITE, CYAN

class PowerUp:
    """Base class for all power-ups."""

    def __init__(self, x, y, radius=10):
        """Initialize power-up properties."""
        self.x = x
        self.y = y
        self.radius = radius
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
        """Draw the power-up as a glowing neon blue circle."""
        # Outer glow effect
        pygame.draw.circle(screen, (0, 100, 255), (int(self.x), int(self.y)), self.radius + 4, 1)  # Soft glow
        pygame.draw.circle(screen, (0, 150, 255), (int(self.x), int(self.y)), self.radius + 2, 1)  # Inner glow

        # Main powerup shape
        pygame.draw.circle(screen, CYAN, (int(self.x), int(self.y)), self.radius)

        # Draw powerup type (letter)
        font = pygame.font.Font(None, 20)
        text = font.render(self.get_symbol(), True, (0, 0, 0))  # Black text for contrast
        screen.blit(text, (self.x - 5, self.y - 5))

    def apply(self, player):
        """Apply the effect of the power-up (to be overridden by subclasses)."""
        raise NotImplementedError("PowerUp subclasses must implement `apply()`.")

    def get_symbol(self):
        """Return the symbol to display inside the power-up."""
        return "?"

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
