import random

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
DARK_ORANGE = (255, 100, 0)

# Random Planet Position & Size
PLANET_X = random.randint(200, WIDTH - 200)
PLANET_Y = random.randint(200, HEIGHT - 200)
PLANET_RADIUS = random.randint(50, 150)  # Random planet size