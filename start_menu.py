import config
import pygame

def show_start_menu(screen, clock) -> None:
    """Displays the start menu and waits for player input."""
    font = pygame.font.Font(None, 50)  # Default font

    menu_running = True
    while menu_running:
        screen.fill(config.BLACK)

        _draw_text(screen, "Planetoids!", config.WIDTH // 2 - 150, config.HEIGHT // 3, font)
        _draw_text(screen, "Press ENTER to Start", config.WIDTH // 2 - 140, config.HEIGHT // 2, font)
        _draw_text(screen, "Press ESC to Quit", config.WIDTH // 2 - 120, config.HEIGHT // 2 + 50, font)

        pygame.display.flip()
        clock.tick(config.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game on Enter
                    menu_running = False
                if event.key == pygame.K_ESCAPE:  # Quit game on Escape
                    pygame.quit()
                    exit()

def _draw_text(screen, text, x, y, font) -> None:
    """Helper function to render text on the screen."""
    rendered_text = font.render(text, True, config.WHITE)
    screen.blit(rendered_text, (x, y))