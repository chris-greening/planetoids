import logging
import os

import dotenv

dotenv.load_dotenv()

DEBUG_MODE = os.getenv("DEBUG", "False").lower() in ("true", "1")

# Define log directory
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
LOG_FILE = os.path.join(LOG_DIR, "game.log")

logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,  # Set to INFO or WARNING in production
    format="[%(asctime)s - %(levelname)s - %(module)s]: - %(message)s",
    handlers=[
        # logging.FileHandler(LOG_FILE, mode="w"),  # Logs to a file
        logging.StreamHandler()  # Logs to console
    ]
)

logger = logging.getLogger("Planetoids")
