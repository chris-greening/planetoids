import pygame
import config

class PauseMenu:
    def __init__(self, screen):
        """Initialize the pause menu."""
        self.screen = screen
        self.font = pygame.font.Font(None, 50)  # Default font
        self.running = False  # Pause state

    def show(self):
        """Displays the pause screen until the user resumes."""
        self.running = True
        while self.running:
            self._draw_pause_screen()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Resume game on 'P' press
                        self.running = False

    def _draw_pause_screen(self):
        """Draws a semi-transparent overlay with pause text."""
        overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # 150 alpha for slight transparency
        self.screen.blit(overlay, (0, 0))

        text = self.font.render("PAUSED - Press P to Resume", True, config.WHITE)
        self.screen.blit(text, (config.WIDTH // 2 - 200, config.HEIGHT // 2))
