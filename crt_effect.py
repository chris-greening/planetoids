import pygame
import random

def apply_scanlines(screen):
    """Draws horizontal scanlines to simulate an old CRT screen."""
    width, height = screen.get_size()
    scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for y in range(0, height, 4):  # Every 4 pixels (adjust for intensity)
        pygame.draw.line(scanline_surface, (0, 0, 0, 60), (0, y), (width, y))  # Semi-transparent black

    screen.blit(scanline_surface, (0, 0))

def apply_pixelation(screen, scale_factor=4):
    """Reduces resolution slightly to create a pixelated effect."""
    width, height = screen.get_size()
    small_surf = pygame.transform.scale(screen, (width // scale_factor, height // scale_factor))
    screen.blit(pygame.transform.scale(small_surf, (width, height)), (0, 0))

def apply_flicker(screen):
    """Adds a subtle flicker to simulate an old CRT glow effect."""
    if random.randint(0, 20) == 0:  # 10% chance per frame
        flicker_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        flicker_surface.fill((255, 255, 255, 5))  # Slight white overlay
        screen.blit(flicker_surface, (0, 0))