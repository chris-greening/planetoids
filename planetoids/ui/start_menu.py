import random
import os

import pygame

from planetoids.core import config
from planetoids.entities.asteroid import Asteroid
from planetoids.effects.crt_effect import apply_crt_effect  # Import CRT effect function
from planetoids.core.logger import logger
from planetoids.ui.options_menu import OptionsMenu  # Import OptionsMenu

class StartMenu:
    def __init__(self, screen, clock, settings):
        """Initialize the start menu with a moving asteroid background and refined retro font."""
        self.screen = screen
        self.clock = clock
        self.running = True
        self.selected_index = 0
        self.menu_items = ["Start Game", "Options", "Quit"]
        self.settings = settings

        # Load a refined vintage arcade font (Sleek but retro)
        font_path = os.path.join("assets", "fonts", "VT323.ttf")
        self.font = pygame.font.Font(font_path, 120)
        self.menu_font = pygame.font.Font(font_path, 64)
        self.small_font = pygame.font.Font(font_path, 36)

        # Initialize Options Menu
        self.options_menu = OptionsMenu(
            self.screen, self.settings, self.font, self.menu_font, self.small_font
        )

        # Generate background asteroids
        self.background_asteroids = [
            Asteroid(
                random.randint(0, config.WIDTH),
                random.randint(0, config.HEIGHT),
                size=random.randint(30, 60),
                stage=3)
            for _ in range(6)
        ]
        logger.info("StartMenu instantiated")

    def show(self):
        """Displays the start menu with moving asteroid background."""
        logger.info("Show start menu")
        while self.running:
            self.screen.fill(config.BLACK)

            # Update and draw background asteroids
            for asteroid in self.background_asteroids:
                asteroid.update(game_state=None)
                asteroid.draw(self.screen)

            self._draw_main_menu()

            # Apply CRT effect if enabled
            if self.settings.get("crt_enabled"):
                apply_crt_effect(self.screen)

            pygame.display.flip()
            self.clock.tick(config.FPS)

            self._handle_events()

        self._fade_out()  # Smooth transition effect before starting the game

    def _draw_main_menu(self):
        """Draws the main start menu with a refined arcade look."""
        self._draw_text("PLANETOIDS", config.WIDTH // 2 - 160, config.HEIGHT // 4, color=config.YELLOW, font=self.font)

        for i, item in enumerate(self.menu_items):
            color = config.WHITE if i != self.selected_index else config.ORANGE  # Highlight selected option
            self._draw_text(item, config.WIDTH // 2 - 120, config.HEIGHT // 2 + i * 50, color, self.menu_font)

        self._draw_text("Press ENTER to select", config.WIDTH // 2 - 140, config.HEIGHT - 40, config.DIM_GRAY, self.small_font)
        self._draw_studio_branding()
        self._draw_version()

    def _draw_version(self):
        """Displays the game version in the bottom right corner."""
        version_text = self.small_font.render(config.VERSION, True, config.DIM_GRAY)
        version_rect = version_text.get_rect(bottomright=(config.WIDTH - 10, config.HEIGHT - 10))
        self.screen.blit(version_text, version_rect)

    def _draw_studio_branding(self):
        """Displays 'Greening Studio' in the bottom left corner."""
        studio_text = self.small_font.render("GREENING STUDIO", True, config.GREEN)
        studio_rect = studio_text.get_rect(bottomleft=(10, config.HEIGHT - 10))
        self.screen.blit(studio_text, studio_rect)

    def _draw_text(self, text, x, y, color=config.WHITE, font=None):
        """Helper function to render sharp, readable text."""
        if font is None:
            font = self.font  # Default to main font
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
                    self._handle_main_selection()

    def _handle_main_selection(self):
        """Handles selection in the main menu."""
        if self.selected_index == 0:  # Start Game
            self.running = False  # Exit menu loop
        elif self.selected_index == 1:  # Open Options
            self.options_menu.show()
        elif self.selected_index == 2:  # Quit
            pygame.quit()
            exit()

    def _fade_out(self):
        """Applies a fade-out transition before starting the game."""
        fade_surface = pygame.Surface((config.WIDTH, config.HEIGHT))
        fade_surface.fill(config.BLACK)

        for alpha in range(0, 255, 10):  # Increase alpha gradually
            fade_surface.set_alpha(alpha)
            self.screen.fill(config.BLACK)

            # Keep drawing background asteroids while fading
            for asteroid in self.background_asteroids:
                asteroid.update(game_state=None)
                asteroid.draw(self.screen)

            # Apply CRT effect if enabled during fade-out
            if self.settings.get("crt_enabled"):
                apply_crt_effect(self.screen)

            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(30)  # Smooth transition speed
        logger.info("Start menu fadeout")
