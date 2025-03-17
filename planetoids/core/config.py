import random
import pygame

class Config:
    """Handles dynamic game configuration, including screen scaling and colors."""

    BASE_WIDTH = 1360
    BASE_HEIGHT = 768
    FPS = 60

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255, 140, 0)
    RED = (255, 0, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 146, 255)
    DARK_ORANGE = (255, 100, 0)
    YELLOW = (255, 215, 0)
    DIM_GRAY = (105, 105, 105)  # Dark gray, slightly faded
    GREEN = (34, 139, 34)  # Darker, "hacker" style green

    VERSION = "v0.1.0"

    def __init__(self):
        """Initialize screen dimensions and scaled properties."""
        self._initialize_screen_size()
        self._scale_properties()

    def _initialize_screen_size(self):
        """Ensure Pygame is initialized before fetching display info."""
        if not pygame.get_init():
            pygame.init()
            pygame.display.set_mode((1, 1))  # Minimal window to enable display info

        info = pygame.display.Info()
        self.SCREEN_WIDTH = info.current_w
        self.SCREEN_HEIGHT = info.current_h

        self.WIDTH = int(self.SCREEN_WIDTH * (self.BASE_WIDTH / self.SCREEN_WIDTH))
        self.HEIGHT = int(self.SCREEN_HEIGHT * (self.BASE_HEIGHT / self.SCREEN_HEIGHT))

        # self.WIDTH, self.HEIGHT = 960, 540

    def _scale_properties(self):
        """Update any game elements that depend on screen size."""
        self.PLANET_X = random.randint(int(200 * (self.WIDTH / self.BASE_WIDTH)), int(self.WIDTH - 200 * (self.WIDTH / self.BASE_WIDTH)))
        self.PLANET_Y = random.randint(int(200 * (self.HEIGHT / self.BASE_HEIGHT)), int(self.HEIGHT - 200 * (self.HEIGHT / self.BASE_HEIGHT)))
        self.PLANET_RADIUS = random.randint(int(50 * (self.WIDTH / self.BASE_WIDTH)), int(150 * (self.WIDTH / self.BASE_WIDTH)))

    def update_screen_size(self):
        """Allows dynamic screen resizing and updates dependent properties."""
        self._initialize_screen_size()
        self._scale_properties()

# Global instance
config = Config()
