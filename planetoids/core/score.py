import json
import os
import pygame

from planetoids.core.config import config
from planetoids.core.settings import Settings  # For access to CONFIG_DIR

class Score:
    HIGHSCORE_PATH = os.path.join(Settings.CONFIG_DIR, "high_score.json")

    def __init__(self, settings):
        self.score = 0
        self.settings = settings
        self.high_score = self._load_high_score()
        self.new_high_score = False  # ✅ Track if a new high score was achieved

    @property
    def font(self):
        return pygame.font.Font(
            self.settings.FONT_PATH,
            {"minimum": 36, "medium": 48, "maximum": 64}.get(self.settings.get("pixelation"), 36)
        )

    def update_score(self, asteroid):
        """Increase score based on asteroid size and track new high score."""
        if asteroid.size >= 40:
            self.score += 100
        elif asteroid.size >= 20:
            self.score += 200
        else:
            self.score += 300

        if self.score > self.high_score:
            self.high_score = self.score
            self.new_high_score = True  # ✅ Mark that we’ve beaten the previous high score

    def draw(self, screen):
        offset = {"minimum": 200, "medium": 300, "maximum": 400}.get(
            self.settings.get("pixelation"), 200
        )

        score_text = self.font.render(f"Score: {self.score}", True, config.WHITE)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, config.YELLOW)

        # Use centery for better vertical alignment
        high_score_rect = high_score_text.get_rect(center=(config.WIDTH // 2, 30))
        score_rect = score_text.get_rect(topright=(config.WIDTH - 20, high_score_rect.top))

        screen.blit(score_text, score_rect)
        screen.blit(high_score_text, high_score_rect)

    def maybe_save_high_score(self):
        """Only write high score if a new one was reached."""
        if self.new_high_score:
            try:
                with open(self.HIGHSCORE_PATH, "w") as f:
                    json.dump({"high_score": self.high_score}, f)
                print("✅ High score saved")
            except Exception as e:
                print(f"⚠️ Failed to save high score: {e}")

    def _load_high_score(self):
        """Loads high score from a separate file."""
        try:
            if os.path.exists(self.HIGHSCORE_PATH):
                with open(self.HIGHSCORE_PATH, "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except Exception as e:
            print(f"⚠️ Failed to load high score: {e}")
        return 0
