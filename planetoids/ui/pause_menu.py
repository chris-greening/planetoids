import os
import pygame

from planetoids.core.config import config
from planetoids.effects.crt_effect import apply_crt_effect
from planetoids.core.logger import logger
from planetoids.ui import OptionsMenu
from planetoids.core.settings import get_font_path

class PauseMenu:
    def __init__(self, screen, game_state):
        """Initialize the pause menu with retro font and settings support."""
        self.screen = screen
        self.running = False  # Pause state
        self.selected_index = 0  # Menu selection index
        self.menu_items = ["Resume", "Options", "Quit"]
        self.game_state = game_state  # Access GameState to modify settings

        # Load the same retro pixel font as the Start Menu
        font_path = get_font_path()
        self.font = pygame.font.Font(font_path, 64)  # Main menu font
        self.menu_font = pygame.font.Font(font_path, 64)  # Menu items
        self.small_font = pygame.font.Font(font_path, 36)  # Smaller for instructions

        # Instantiate OptionsMenu with font settings
        self.options_menu = OptionsMenu(
            screen,
            self.game_state.settings,
            self.font,
            self.menu_font,
            self.small_font
        )

        logger.info("PauseMenu instantiated")

    def show(self):
        """Displays the pause menu and waits for player input."""
        logger.info("Pause menu triggered")
        self.running = True
        while self.running:
            self.screen.fill(config.BLACK)
            # Draw the pause menu
            self._draw_pause_menu()

            # Apply CRT effect if enabled
            if self.game_state.settings.get("crt_enabled"):
                apply_crt_effect(self.screen, self.game_state.settings)

            pygame.display.flip()
            self._handle_events()
        self.game_state.paused = False
        self.game_state.clock.tick()

    def _draw_pause_menu(self):
        """Draws the pause menu."""
        self._draw_text("PAUSED", config.WIDTH // 2 - 100, config.HEIGHT // 4, config.YELLOW, self.font)

        for i, item in enumerate(self.menu_items):
            color = config.WHITE if i != self.selected_index else config.ORANGE  # Highlight selected option
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
                    self.selected_index = (self.selected_index + 1) % len(self.menu_items)
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN:
                    self._handle_pause_selection()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False  # Unpause when ESC is pressed

    def _handle_pause_selection(self):
        """Handles selection in the pause menu."""
        if self.selected_index == 0:  # Resume
            self.running = False
        elif self.selected_index == 1:  # Open Options
            self.options_menu.show()
        elif self.selected_index == 2:  # Quit
            pygame.quit()
            exit()
