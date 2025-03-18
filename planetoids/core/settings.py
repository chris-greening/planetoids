import json
import os
from appdirs import user_config_dir
import sys
import importlib.resources as pkg_resources
from pathlib import Path

def get_font_path():
    """Fetch font path inside the installed package safely."""
    if sys.version_info >= (3, 9):
        return str(pkg_resources.files("planetoids") / "assets" / "fonts" / "VT323.ttf")
    else:
        with pkg_resources.path("planetoids.assets.fonts", "VT323.ttf") as font_path:
            return str(font_path)

class Settings:
    """Handles loading, modifying, and saving game settings."""

    APP_NAME = "Planetoids"
    APP_AUTHOR = "GreeningStudio"
    CONFIG_DIR = user_config_dir(APP_NAME, APP_AUTHOR)
    CONFIG_PATH = os.path.join(CONFIG_DIR, "settings.json")

    DEFAULT_SETTINGS = {
        "fullscreen_enabled": True,
        "crt_enabled": False,
        "glitch_intensity": "medium",
        "pixelation": "minimum",
    }

    FONT_PATH = get_font_path()

    def __init__(self):
        """Initialize settings by loading from file or using defaults."""
        self._load_settings()

    def _load_settings(self):
        """Loads settings from a JSON file, or creates defaults if missing."""
        if not os.path.exists(self.CONFIG_DIR):
            os.makedirs(self.CONFIG_DIR, exist_ok=True)

        self.data = self.DEFAULT_SETTINGS.copy()  # Start with defaults

        if os.path.exists(self.CONFIG_PATH):
            try:
                with open(self.CONFIG_PATH, "r") as f:
                    loaded_data = json.load(f)

                # ✅ Merge loaded settings with defaults
                for key, default_value in self.DEFAULT_SETTINGS.items():
                    if key not in loaded_data:
                        loaded_data[key] = default_value  # Add missing default

                self.data = loaded_data  # Use merged settings

            except (json.JSONDecodeError, IOError):
                print("⚠️ Failed to load settings, using defaults.")
                self.save()  # Save defaults if load fails

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
            # self.save()

    def toggle(self, key):
        """Toggles a boolean setting, saves it, and returns the new state."""
        if key in self.DEFAULT_SETTINGS and isinstance(self.data[key], bool):
            self.data[key] = not self.data[key]
            # self.save()
            return self.data[key]  # ✅ Return new state


    def reset(self):
        """Resets settings to defaults."""
        self.data = self.DEFAULT_SETTINGS.copy()
        # self.save()
