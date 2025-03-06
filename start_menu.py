import pygame
import config
import random
from asteroid import Asteroid  # Ensure Asteroid class is imported

class StartMenu:
    def __init__(self, screen, clock):
        """Initialize the start menu with a moving asteroid background."""
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font(None, 50)  # Default font
        self.running = True
        self.options_mode = False  # Toggle between main menu & options menu
        self.selected_index = 0  # Menu selection index
        self.menu_items = ["Start Game", "Options", "Quit"]  # Main menu options
        self.options_items = ["CRT Effect: On", "Back"]  # Options menu
        self.crt_enabled = False  # CRT effect starts enabled
        
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
                asteroid.update(game_state=None)  # No game state needed for now
                asteroid.draw(self.screen)

            if self.options_mode:
                self._draw_options_menu()
            else:
                self._draw_main_menu()

            pygame.display.flip()
            self.clock.tick(config.FPS)

            self._handle_events()

        self._fade_out()  # Smooth transition effect before starting the game
        return self.crt_enabled  # Return CRT setting for use in the game

    def _draw_main_menu(self):
        """Draws the main start menu."""
        self._draw_text("Planetoids!", config.WIDTH // 2 - 150, config.HEIGHT // 3)

        for i, item in enumerate(self.menu_items):
            color = config.WHITE if i != self.selected_index else config.ORANGE  # Highlight selected option
            self._draw_text(item, config.WIDTH // 2 - 100, config.HEIGHT // 2 + i * 40, color)

    def _draw_options_menu(self):
        """Draws the options menu."""
        self._draw_text("Options", config.WIDTH // 2 - 100, config.HEIGHT // 3)

        # Update CRT effect label dynamically
        self.options_items[0] = f"CRT Effect: {'On' if self.crt_enabled else 'Off'}"

        for i, item in enumerate(self.options_items):
            color = config.WHITE if i != self.selected_index else config.ORANGE
            self._draw_text(item, config.WIDTH // 2 - 100, config.HEIGHT // 2 + i * 40, color)

    def _draw_text(self, text, x, y, color=config.WHITE):
        """Helper function to render text on the screen."""
        rendered_text = self.font.render(text, True, color)
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
            self.running = False  # This exits the menu loop
        elif self.selected_index == 1:  # Options
            self.options_mode = True
            self.selected_index = 0  # Reset selection in options
        elif self.selected_index == 2:  # Quit
            pygame.quit()
            exit()

    def _handle_options_selection(self):
        """Handles selection in the options menu."""
        if self.selected_index == 0:  # Toggle CRT Effect
            self.crt_enabled = not self.crt_enabled
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

            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(30)  # Smooth transition speed
