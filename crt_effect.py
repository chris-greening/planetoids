import pygame

def apply_scanlines(screen):
    """Draws horizontal scanlines to simulate an old CRT screen."""
    width, height = screen.get_size()
    scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for y in range(0, height, 4):  # Every 4 pixels (adjust for intensity)
        pygame.draw.line(scanline_surface, (0, 0, 0, 60), (0, y), (width, y))  # Semi-transparent black

    screen.blit(scanline_surface, (0, 0))
