import pygame
from planetoids.core import config
import random
import os
from planetoids.entities.asteroid import Asteroid
from planetoids.effects.crt_effect import apply_crt_effect  # Import CRT effect function

class StartMenu:
    def __init__(self, screen, clock):
        """Initialize the start menu with a moving asteroid background and refined retro font."""
        self.screen = screen
        self.clock = clock
        self.running = True
        self.options_mode = False
        self.selected_index = 0
        self.menu_items = ["Start Game", "Options", "Quit"]
        self.options_items = ["CRT Effect: On", "Back"]
        self.crt_enabled = True  # CRT effect starts ENABLED by default

        # Load a refined vintage arcade font (Sleek but retro)
        font_path = os.path.join("assets", "fonts", "VT323.ttf")  # ✅ More sci-fi, less cartoony
        self.font = pygame.font.Font(font_path, 120)  # ✅ Larger for title
        self.menu_font = pygame.font.Font(font_path, 64)  # ✅ Medium for menu
        self.small_font = pygame.font.Font(font_path, 36)  # ✅ Small for instructions

        # Generate background asteroids
        self.background_asteroids = [Asteroid(random.randint(0, config.WIDTH),
                                              random.randint(0, config.HEIGHT),
                                              size=random.randint(30, 60),
                                              stage=3)
                                     for _ in range(6)]  # Adjust number of asteroids as needed

    def show(self):
        """Displays the start menu with moving asteroid background."""
        while self.running:
            self.screen.fill(config.BLACK)

            # Update and draw background asteroids
            for asteroid in self.background_asteroids:
                asteroid.update(game_state=None)
                asteroid.draw(self.screen)

            if self.options_mode:
                self._draw_options_menu()
            else:
                self._draw_main_menu()

            # Apply CRT effect if enabled
            if self.crt_enabled:
                apply_crt_effect(self.screen)

            pygame.display.flip()
            self.clock.tick(config.FPS)

            self._handle_events()

        self._fade_out()  # Smooth transition effect before starting the game
        return self.crt_enabled  # Return CRT setting for use in the game

    def _draw_main_menu(self):
        """Draws the main start menu with a refined arcade look."""
        self._draw_text("PLANETOIDS", config.WIDTH // 2 - 160, config.HEIGHT // 4, color=config.YELLOW, font=self.font)

        for i, item in enumerate(self.menu_items):
            color = config.WHITE if i != self.selected_index else config.ORANGE  # Highlight selected option
            self._draw_text(item, config.WIDTH // 2 - 120, config.HEIGHT // 2 + i * 50, color, self.menu_font)

        self._draw_text("Press ENTER to select", config.WIDTH // 2 - 140, config.HEIGHT - 40, config.DIM_GRAY, self.small_font)
        self._draw_studio_branding()
        self._draw_version

    def _draw_options_menu(self):
        """Draws the options menu."""
        self._draw_text("OPTIONS", config.WIDTH // 2 - 120, config.HEIGHT // 4, config.YELLOW, self.font)

        # Update CRT effect label dynamically
        self.options_items[0] = f"CRT Effect: {'On' if self.crt_enabled else 'Off'}"

        for i, item in enumerate(self.options_items):
            color = config.WHITE if i != self.selected_index else config.ORANGE
            self._draw_text(item, config.WIDTH // 2 - 120, config.HEIGHT // 2 + i * 50, color, self.menu_font)

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

        # Create text surface (No more double blitting for glow)
        rendered_text = font.render(text, True, color)

        # Blit actual text
        self.screen.blit(rendered_text, (x, y))

    def _handle_events(self):
        """Handles user input for menu navigation."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % (len(self.options_items) if self.options_mode else len(self.menu_items))
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % (len(self.options_items) if self.options_mode else len(self.menu_items))
                if event.key == pygame.K_RETURN:
                    if self.options_mode:
                        self._handle_options_selection()
                    else:
                        self._handle_main_selection()
                if event.key == pygame.K_ESCAPE and self.options_mode:
                    self.options_mode = False  # Return to main menu

    def _handle_main_selection(self):
        """Handles selection in the main menu."""
        if self.selected_index == 0:  # Start Game
            self.running = False  # Exit menu loop
        elif self.selected_index == 1:  # Options
            self.options_mode = True
            self.selected_index = 0  # Reset selection in options
        elif self.selected_index == 2:  # Quit
            pygame.quit()
            exit()

    def _handle_options_selection(self):
        """Handles selection in the options menu."""
        if self.selected_index == 0:  # Toggle CRT Effect
            self.crt_enabled = not self.crt_enabled  # Toggle CRT effect on/off
        elif self.selected_index == 1:  # Back
            self.options_mode = False
            self.selected_index = 0  # Reset main menu selection

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
            if self.crt_enabled:
                apply_crt_effect(self.screen)

            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(30)  # Smooth transition speed
