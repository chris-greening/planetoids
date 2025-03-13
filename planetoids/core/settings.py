import json
import os
from appdirs import user_config_dir

# Define the directory and file path
APP_NAME = "Planetoids"
APP_AUTHOR = "GreeningStudio"
CONFIG_DIR = user_config_dir(APP_NAME, APP_AUTHOR)
CONFIG_PATH = os.path.join(CONFIG_DIR, "settings.json")

# Default settings (used if no file exists)
DEFAULT_SETTINGS = {
    "crt_enabled": True
}

def load_settings():
    """Loads settings from a JSON file, or creates defaults if missing."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)  # Ensure directory exists

    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Failed to load settings, using defaults.")

    # If no file exists or load fails, return defaults
    save_settings(DEFAULT_SETTINGS)
    return DEFAULT_SETTINGS

def save_settings(settings):
    """Saves settings to a JSON file."""
    with open(CONFIG_PATH, "w") as f:
        json.dump(settings, f, indent=4)
