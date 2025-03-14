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
        self.options_items = [
            f"CRT Effect: {'On' if self.settings.get('crt_enabled') else 'Off'}",
            f"Glitch Level: {self.settings.get('glitch_intensity').capitalize()}",
            "Save Settings",
            "Back"
        ]

        self._draw_text("OPTIONS", config.WIDTH // 2 - 120, config.HEIGHT // 4, config.YELLOW, self.font)

        for i, item in enumerate(self.options_items):
            color = config.WHITE if i != self.selected_index else config.ORANGE
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
                    self.selected_index = (self.selected_index + 1) % len(self.options_items)
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options_items)
                elif event.key == pygame.K_RETURN:
                    return self._handle_options_selection()
        return True

    def _handle_options_selection(self):
        """Handles selection logic in the options menu."""
        if self.selected_index == 0:  # Toggle CRT Effect
            self.settings.toggle("crt_enabled")
            self.unsaved_changes = True

        elif self.selected_index == 1:  # Cycle glitch level
            glitch_levels = ["minimum", "medium", "maximum"]
            current_index = glitch_levels.index(self.settings.get("glitch_intensity"))
            self.settings.set("glitch_intensity", glitch_levels[(current_index + 1) % len(glitch_levels)])
            self.unsaved_changes = True

        elif self.selected_index == 2:  # Save Settings
            self.settings.save()
            self.unsaved_changes = False
            self.save_time = time.time()

        elif self.selected_index == 3:  # Back
            # if self.unsaved_changes:
            #     return not self._confirm_unsaved_changes()
            return False  # Exit menu normally

        return True  # Stay in menu

    def _confirm_unsaved_changes(self):
        """Displays a confirmation popup if the user has unsaved changes."""
        confirmation = self._show_confirmation_popup(
            "Unsaved changes will be lost. Continue?", ["Yes", "No"]
        )
        return confirmation  # Returns True if "Yes" is selected, False otherwise

    def _show_confirmation_popup(self, message, options):
        """Displays a confirmation popup with selectable options."""
        overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent dark background
        self.screen.blit(overlay, (0, 0))

        # Render the message
        text_surface = self.small_font.render(message, True, config.WHITE)
        text_rect = text_surface.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 3))
        self.screen.blit(text_surface, text_rect)

        selected_index = 0  # Start with first option selected

        while True:
            self.screen.blit(overlay, (0, 0))  # Redraw overlay
            self.screen.blit(text_surface, text_rect)  # Redraw message

            for i, option in enumerate(options):
                color = config.ORANGE if i == selected_index else config.WHITE
                option_surface = self.small_font.render(option, True, color)
                option_rect = option_surface.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 + i * 40))
                self.screen.blit(option_surface, option_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        return selected_index == 0  # Returns True if "Yes" is selected, False if "No"

    def _draw_text(self, text, x, y, color=config.WHITE, font=None):
        """Helper function to render sharp, readable text."""
        if font is None:
            font = self.font  # Default to main font
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, (x, y))
