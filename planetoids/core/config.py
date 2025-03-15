import random
import pygame

def get_screen_size():
    """Ensure Pygame is initialized before fetching display info."""
    if not pygame.get_init():
        pygame.init()
    info = pygame.display.Info()
    return info.current_w, info.current_h

BASE_WIDTH = 1360
BASE_HEIGHT = 768

SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_size()

WIDTH = int(SCREEN_WIDTH * (BASE_WIDTH / SCREEN_WIDTH))
HEIGHT = int(SCREEN_HEIGHT * (BASE_HEIGHT / SCREEN_HEIGHT))

# Constants
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
DARK_ORANGE = (255, 100, 0)
YELLOW = (255, 215, 0)
DIM_GRAY = (105, 105, 105)  # Dark gray, slightly faded
GREEN = (34, 139, 34)  # Darker, "hacker" style green

PLANET_X = random.randint(int(200 * (WIDTH / BASE_WIDTH)), int(WIDTH - 200 * (WIDTH / BASE_WIDTH)))
PLANET_Y = random.randint(int(200 * (HEIGHT / BASE_HEIGHT)), int(HEIGHT - 200 * (HEIGHT / BASE_HEIGHT)))
PLANET_RADIUS = random.randint(int(50 * (WIDTH / BASE_WIDTH)), int(150 * (WIDTH / BASE_WIDTH)))  # Scaled planet size

VERSION = "v0.1.0"
