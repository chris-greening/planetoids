import random

import pygame

# Constants
def get_screen_size():
    """Ensure Pygame is initialized before fetching display info."""
    if not pygame.get_init():  # Only init if necessary
        pygame.init()
    info = pygame.display.Info()
    return info.current_w, info.current_h

# Set WIDTH and HEIGHT dynamically when config is imported
WIDTH, HEIGHT = get_screen_size()
# WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
DARK_ORANGE = (255, 100, 0)
YELLOW = (255, 215, 0)
DIM_GRAY = (105, 105, 105)  # Dark gray, slightly faded
GREEN = (34, 139, 34)  # Darker, "hacker" style green

# Random Planet Position & Size
PLANET_X = random.randint(200, WIDTH - 200)
PLANET_Y = random.randint(200, HEIGHT - 200)
PLANET_RADIUS = random.randint(50, 150)  # Random planet size

VERSION="v0.1.0"
