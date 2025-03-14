import json
import os
from appdirs import user_config_dir

class Settings:
    """Handles loading, modifying, and saving game settings."""

    APP_NAME = "Planetoids"
    APP_AUTHOR = "GreeningStudio"
    CONFIG_DIR = user_config_dir(APP_NAME, APP_AUTHOR)
    CONFIG_PATH = os.path.join(CONFIG_DIR, "settings.json")

    DEFAULT_SETTINGS = {
        "crt_enabled": True
    }

    def __init__(self):
        """Initialize settings by loading from file or using defaults."""
        self.data = self._load_settings()

    def _load_settings(self):
        """Loads settings from a JSON file, or creates defaults if missing."""
        if not os.path.exists(self.CONFIG_DIR):
            os.makedirs(self.CONFIG_DIR, exist_ok=True)

        if os.path.exists(self.CONFIG_PATH):
            try:
                with open(self.CONFIG_PATH, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                print("Failed to load settings, using defaults.")

        # If no file exists or load fails, return defaults
        self.save()  # Save the defaults immediately
        return self.DEFAULT_SETTINGS.copy()  # Avoid modifying class-level dict

    def save(self):
        """Saves settings to a JSON file."""
        with open(self.CONFIG_PATH, "w") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key):
        """Retrieves a setting value safely."""
        return self.data.get(key, self.DEFAULT_SETTINGS.get(key))

    def set(self, key, value):
        """Updates a setting value and marks settings as needing saving."""
        if key in self.DEFAULT_SETTINGS:
            self.data[key] = value

    def toggle(self, key):
        """Toggles a boolean setting (e.g., CRT effect)."""
        if key in self.DEFAULT_SETTINGS and isinstance(self.data[key], bool):
            self.data[key] = not self.data[key]

    def reset(self):
        """Resets settings to defaults."""
        self.data = self.DEFAULT_SETTINGS.copy()
        self.save()

