import pygame
import config

class StartMenu:
    def __init__(self, screen, clock):
        """Initialize the start menu."""
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font(None, 50)  # Default font
        self.running = True

    def show(self):
        """Displays the start menu and waits for player input."""
        while self.running:
            self.screen.fill(config.BLACK)

            self._draw_text("Planetoids!", config.WIDTH // 2 - 150, config.HEIGHT // 3)
            self._draw_text("Press ENTER to Start", config.WIDTH // 2 - 140, config.HEIGHT // 2)
            self._draw_text("Press ESC to Quit", config.WIDTH // 2 - 120, config.HEIGHT // 2 + 50)

            pygame.display.flip()
            self.clock.tick(config.FPS)

            self._handle_events()

    def _draw_text(self, text, x, y):
        """Helper function to render text on the screen."""
        rendered_text = self.font.render(text, True, config.WHITE)
        self.screen.blit(rendered_text, (x, y))

    def _handle_events(self):
        """Handles user input for the menu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game on Enter
                    self.running = False
                if event.key == pygame.K_ESCAPE:  # Quit game on Escape
                    pygame.quit()
                    exit()
