import os

import pygame

from planetoids.core import config
from planetoids.effects.crt_effect import apply_crt_effect  # Import CRT effect function

class PauseMenu:
    def __init__(self, screen, game_state):
        """Initialize the pause menu with retro font."""
        self.screen = screen
        self.running = False  # Pause state
        self.selected_index = 0  # Menu selection index
        self.menu_items = ["Resume", "Options", "Quit"]
        self.options_items = ["CRT Effect: On", "Back"]
        self.options_mode = False  # Toggle between pause menu & options menu
        self.game_state = game_state  # Access GameState to modify settings

        # Load the same retro pixel font as the Start Menu
        font_path = os.path.join("assets", "fonts", "VT323.ttf")  # Change if needed
        self.font = pygame.font.Font(font_path, 64)  # Main menu font
        self.small_font = pygame.font.Font(font_path, 36)  # Smaller for instructions

    def show(self):
        """Displays the pause menu and waits for player input."""
        self.running = True
        while self.running:
            self.screen.fill(config.BLACK)

            # Update menu based on mode
            if self.options_mode:
                self._draw_options_menu()
            else:
                self._draw_pause_menu()

            # Apply CRT effect if enabled
            if self.game_state.crt_enabled:
                apply_crt_effect(self.screen)

            pygame.display.flip()
            self._handle_events()

    def _draw_pause_menu(self):
        """Draws the pause menu."""
        self._draw_text("PAUSED", config.WIDTH // 2 - 100, config.HEIGHT // 4, config.YELLOW, self.font)

        for i, item in enumerate(self.menu_items):
            color = config.WHITE if i != self.selected_index else config.ORANGE  # Highlight selected option
            self._draw_text(item, config.WIDTH // 2 - 100, config.HEIGHT // 2 + i * 50, color)

    def _draw_options_menu(self):
        """Draws the options menu."""
        self._draw_text("OPTIONS", config.WIDTH // 2 - 100, config.HEIGHT // 4, config.YELLOW, self.font)

        # Update CRT effect label dynamically
        self.options_items[0] = f"CRT Effect: {'On' if self.game_state.crt_enabled else 'Off'}"

        for i, item in enumerate(self.options_items):
            color = config.WHITE if i != self.selected_index else config.ORANGE
            self._draw_text(item, config.WIDTH // 2 - 100, config.HEIGHT // 2 + i * 50, color)

    def _draw_text(self, text, x, y, color=config.WHITE, font=None):
        """Helper function to render text on the screen."""
        if font is None:
            font = self.font  # Default to the main font

        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, (x, y))

    def _handle_events(self):
        """Handles user input for menu navigation."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % (len(self.options_items) if self.options_mode else len(self.menu_items))
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % (len(self.options_items) if self.options_mode else len(self.menu_items))
                if event.key == pygame.K_RETURN:
                    if self.options_mode:
                        self._handle_options_selection()
                    else:
                        self._handle_pause_selection()
                if event.key == pygame.K_ESCAPE and self.options_mode:
                    self.options_mode = False  # Return to pause menu

    def _handle_pause_selection(self):
        """Handles selection in the pause menu."""
        if self.selected_index == 0:  # Resume
            self.running = False
        elif self.selected_index == 1:  # Options
            self.options_mode = True
            self.selected_index = 0  # Reset selection in options menu
        elif self.selected_index == 2:  # Quit
            pygame.quit()
            exit()

    def _handle_options_selection(self):
        """Handles selection in the options menu."""
        if self.selected_index == 0:  # Toggle CRT Effect
            self.game_state.crt_enabled = not self.game_state.crt_enabled
        elif self.selected_index == 1:  # Back
            self.options_mode = False
            self.selected_index = 0  # Reset pause menu selection
