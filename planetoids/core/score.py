import json
import os
import time
import pygame

from planetoids.core.config import config
from planetoids.core.settings import Settings  # For access to CONFIG_DIR

class Score:
    HIGHSCORE_PATH = os.path.join(Settings.CONFIG_DIR, "high_score.json")

    def __init__(self, settings):
        self.score = 0
        self.settings = settings
        self.high_score = self._load_high_score()
        self.new_high_score = False

        self.multiplier = 1
        self.multiplier_progress = 0.0
        self.last_hit_time = time.time()

        self.multiplier_thresholds = {1: 1.0, 2: 1.5, 3: 2.0, 4: 3.5}
        self.multiplier_decay_rates = {1: 0.1, 2: 0.25, 3: 0.4, 4: 0.55}
        self.last_multiplier_increase = 0

    @property
    def font(self):
        return pygame.font.Font(
            self.settings.FONT_PATH,
            {"minimum": 36, "medium": 48, "maximum": 64}.get(self.settings.get("pixelation"), 36)
        )

    def update_score(self, asteroid):
        """Increase score based on asteroid size and bump multiplier progress."""
        # Bump multiplier bar
        progress_increase = {1: 0.4, 2: 0.25, 3: 0.15}.get(self.multiplier, 0.1)
        self.multiplier_progress += progress_increase

        if self.multiplier < 4:
            if self.multiplier_progress >= self.multiplier_thresholds[self.multiplier]:
                self.multiplier += 1
                self.multiplier_progress = 0.1  # Start the new level with a bit of progress
        else:
            self.multiplier_progress = min(
                self.multiplier_progress,
                self.multiplier_thresholds[self.multiplier]
    )

        self.last_hit_time = time.time()

        # Calculate score
        base_score = 100 if asteroid.size >= 40 else 200 if asteroid.size >= 20 else 300
        earned = int(base_score * self.multiplier)
        self.score += earned

        if self.score > self.high_score:
            self.high_score = self.score
            self.new_high_score = True

    def update_multiplier(self, dt):
        """Continuously decays multiplier progress."""
        if self.multiplier > 1:
            self.multiplier_progress -= self.multiplier_decay_rates[self.multiplier] * dt
            if self.multiplier_progress <= 0:
                self.multiplier = 1
                self.multiplier_progress = 0.0
        elif self.multiplier == 1:
            self.multiplier_progress = max(0, self.multiplier_progress - self.multiplier_decay_rates[1] * dt)

    def draw_multiplier(self, screen):
        """Draws multiplier bar and label beneath the score in the top-right."""
        max_bar_width = 250
        bar_height = 20

        # Align with top-right corner under score
        padding = 20
        spacing = 10
        x = config.WIDTH - max_bar_width - padding
        y = {"minimum": 80, "medium": 98, "maximum": 116}.get(self.settings.get("pixelation"), 80)

        fill_ratio = self.multiplier_progress / self.multiplier_thresholds[self.multiplier]
        fill_ratio = max(0, min(fill_ratio, 1.0))
        fill_width = int(max_bar_width * fill_ratio)

        color = {1: config.CYAN, 2: config.YELLOW, 3: config.ORANGE, 4: config.RED}.get(self.multiplier, config.CYAN)

        # Background and filled bar
        pygame.draw.rect(screen, (50, 50, 50), (x, y, max_bar_width, bar_height))
        pygame.draw.rect(screen, color, (x, y, fill_width, bar_height))

        # Label aligned to top-right above the bar
        label = self.font.render(f"{self.multiplier}x", True, color)
        screen.blit(label, (x + max_bar_width - label.get_width(), y - label.get_height() - 2))

    def draw(self, screen):
        offset = {"minimum": 200, "medium": 300, "maximum": 400}.get(
            self.settings.get("pixelation"), 200
        )

        score_text = self.font.render(f"Score: {self.score}", True, config.WHITE)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, config.YELLOW)

        high_score_rect = high_score_text.get_rect(center=(config.WIDTH // 2, 30))
        score_rect = score_text.get_rect(topright=(config.WIDTH - 20, high_score_rect.top))

        screen.blit(score_text, score_rect)
        screen.blit(high_score_text, high_score_rect)
        self.draw_multiplier(screen)

    def maybe_save_high_score(self):
        if self.new_high_score:
            try:
                with open(self.HIGHSCORE_PATH, "w") as f:
                    json.dump({"high_score": self.high_score}, f)
                print("✅ High score saved")
            except Exception as e:
                print(f"⚠️ Failed to save high score: {e}")

    def _load_high_score(self):
        try:
            if os.path.exists(self.HIGHSCORE_PATH):
                with open(self.HIGHSCORE_PATH, "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except Exception as e:
            print(f"⚠️ Failed to load high score: {e}")
        return 0
