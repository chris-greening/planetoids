"""Store central configurations"""

import importlib.resources

import pygame

def get_local_version() -> str:
    """Return version number from version.txt"""
    with importlib.resources.open_text("planetoids.core", "version.txt") as f:
        return f.read().strip()

class Config:
    """Handles dynamic game configuration, including screen scaling and colors."""

    BASE_WIDTH = 1360
    BASE_HEIGHT = 768
    FPS = 60

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255, 100, 0)
    RED = (255, 40, 60)
    CYAN = (0, 255, 220)
    BLUE = (0, 180, 255)
    DARK_ORANGE = (255, 80, 20)
    YELLOW = (255, 255, 80)
    DIM_GRAY = (105, 105, 105)  # Dark gray, slightly faded
    GREEN = (34, 139, 34)  # Darker, "hacker" style green

    VERSION = get_local_version()

    def __init__(self) -> None:
        """Initialize screen dimensions and scaled properties."""
        self._initialize_screen_size()

    def _initialize_screen_size(self) -> None:
        """Ensure Pygame is initialized before fetching display info."""
        if not pygame.get_init():
            pygame.init()
            pygame.display.set_mode((1, 1))  # Minimal window to enable display info

        info = pygame.display.Info()
        self.SCREEN_WIDTH = info.current_w
        self.SCREEN_HEIGHT = info.current_h

        self.WIDTH = int(self.SCREEN_WIDTH * (self.BASE_WIDTH / self.SCREEN_WIDTH))
        self.HEIGHT = int(self.SCREEN_HEIGHT * (self.BASE_HEIGHT / self.SCREEN_HEIGHT))

    def update_screen_size(self) -> None:
        """Allows dynamic screen resizing and updates dependent properties."""
        self._initialize_screen_size()

# Global instance
config = Config()
