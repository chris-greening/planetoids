import pygame
import time

class ScorePopup:
    """Handles floating score text when asteroids are hit."""

    def __init__(self, x, y, score, color=(255, 0, 0)):
        """Initialize score popup."""
        self.x = x
        self.y = y
        self.score = score
        self.color = color
        self.start_time = time.time()
        self.duration = 0.4  # Score fades out after 0.6s
        self.alpha = 255  # Starts fully visible

    def update(self):
        """Update position and transparency."""
        elapsed = time.time() - self.start_time

        # Move up slightly over time
        self.y -= 10 * (elapsed / self.duration)  # Adjust speed

        # Fade out
        self.alpha = max(0, 255 - int(255 * (elapsed / self.duration)))

        # Check if expired
        return elapsed < self.duration

    def draw(self, screen, font):
        """Render the floating score popup."""
        if self.alpha > 0:
            text_surface = font.render(f"+{self.score}", True, self.color)
            text_surface.set_alpha(self.alpha)  # Apply fade effect
            screen.blit(text_surface, (int(self.x), int(self.y)))
