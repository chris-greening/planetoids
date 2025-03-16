import time
import pygame
from planetoids.core import config
from planetoids.effects.crt_effect import apply_crt_effect

class OptionsMenu:
    """Handles the options menu logic for modifying and saving game settings."""

    def __init__(self, screen, settings, font, menu_font, small_font):
        self.screen = screen
        self.settings = settings
        self.font = font
        self.menu_font = menu_font
        self.small_font = small_font

        self.selected_index = 0
        self.options_items = [
            f"CRT Effect: {'On' if self.settings.get('crt_enabled') else 'Off'}",
            f"Glitch Level: {self.settings.get('glitch_intensity').capitalize()}",
            f"Pixelation: {self.settings.get('pixelation').capitalize()}",
            "Save Settings",
            "Back"
        ]

        self.unsaved_changes = False
        self.save_time = 0

    def show(self):
        """Displays the options menu and waits for user input."""
        running = True
        while running:
            self.screen.fill(config.BLACK)
            self._draw_options_menu()

            if self.settings.get("crt_enabled"):
                apply_crt_effect(self.screen, self.settings)

            pygame.display.flip()
            running = self._handle_events()

    def _draw_options_menu(self):
        """Draws the options menu, ensuring updated values are displayed."""
        crt_enabled = self.settings.get("crt_enabled")

        self.options_items = [
            f"CRT Effect: {'On' if crt_enabled else 'Off'}",
            f"Glitch Level: {self.settings.get('glitch_intensity').capitalize()}",
            f"Pixelation: {self.settings.get('pixelation').capitalize()}",
            "Save Settings",
            "Back"
        ]

        self._draw_text("OPTIONS", config.WIDTH // 2 - 120, config.HEIGHT // 4, config.YELLOW, self.font)

        for i, item in enumerate(self.options_items):
            # 🔹 If CRT is OFF, make Glitch Level & Pixelation greyed out
            if i in [1, 2] and not crt_enabled:
                color = config.DIM_GRAY  # Greyed out
            else:
                color = config.WHITE if i != self.selected_index else config.ORANGE  # Highlighted selection

            self._draw_text(item, config.WIDTH // 2 - 120, config.HEIGHT // 2 + i * 50, color, self.menu_font)

        # Display "Saved!" if settings were saved recently
        if self.save_time and time.time() - self.save_time < 3:
            self._draw_text("Saved!", config.WIDTH // 2, config.HEIGHT - 80, config.GREEN, self.small_font)

    def _handle_events(self):
        """Handles user input for menu navigation."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self._navigate(1)
                elif event.key == pygame.K_UP:
                    self._navigate(-1)
                elif event.key == pygame.K_RETURN:
                    return self._handle_options_selection()
        return True

    def _navigate(self, direction):
        """Moves selection up or down, skipping disabled items."""
        crt_enabled = self.settings.get("crt_enabled")
        
        while True:
            self.selected_index = (self.selected_index + direction) % len(self.options_items)

            # 🔹 Skip glitch level & pixelation when CRT is off
            if not crt_enabled and self.selected_index in [1, 2]:
                continue

            break

    def _handle_options_selection(self):
        """Handles selection logic in the options menu."""
        crt_enabled = self.settings.get("crt_enabled")

        if self.selected_index == 0:  # Toggle CRT Effect
            self.settings.toggle("crt_enabled")
            self.unsaved_changes = True

        elif self.selected_index == 1 and crt_enabled:  # Cycle glitch level
            glitch_levels = ["minimum", "medium", "maximum"]
            current_index = glitch_levels.index(self.settings.get("glitch_intensity"))
            self.settings.set("glitch_intensity", glitch_levels[(current_index + 1) % len(glitch_levels)])
            self.unsaved_changes = True

        elif self.selected_index == 2 and crt_enabled:  # Pixelation level
            glitch_levels = ["minimum", "medium", "maximum"]
            current_index = glitch_levels.index(self.settings.get("pixelation"))
            self.settings.set("pixelation", glitch_levels[(current_index + 1) % len(glitch_levels)])
            self.unsaved_changes = True

        elif self.selected_index == 3:  # Save Settings
            self.settings.save()
            self.unsaved_changes = False
            self.save_time = time.time()

        elif self.selected_index == 4:  # Back
            return False  # Exit menu

        return True  # Stay in menu

    def _draw_text(self, text, x, y, color=config.WHITE, font=None):
        """Helper function to render sharp, readable text."""
        if font is None:
            font = self.font  # Default to main font
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, (x, y))
