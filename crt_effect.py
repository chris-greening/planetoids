import pygame
import random
import math

def apply_crt_effect(screen):
    """Apply CRT effect to the screen."""
    _apply_scanlines(screen)
    _apply_pixelation(screen, scale_factor=2)
    _apply_flicker(screen)
    _apply_glow(screen)
    _apply_vhs_glitch(screen)  # NEW: Add VHS glitch effect

def _apply_scanlines(screen):
    """Draws horizontal scanlines to simulate an old CRT screen."""
    width, height = screen.get_size()
    scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for y in range(0, height, 4):  # Every 4 pixels (adjust for intensity)
        pygame.draw.line(scanline_surface, (0, 0, 0, 60), (0, y), (width, y))  # Semi-transparent black

    screen.blit(scanline_surface, (0, 0))

def _apply_pixelation(screen, scale_factor=4):
    """Reduces resolution slightly to create a pixelated effect."""
    width, height = screen.get_size()
    small_surf = pygame.transform.scale(screen, (width // scale_factor, height // scale_factor))
    screen.blit(pygame.transform.scale(small_surf, (width, height)), (0, 0))

def _apply_flicker(screen):
    """Adds a subtle flicker to simulate an old CRT glow effect."""
    if random.randint(0, 20) == 0:  # 10% chance per frame
        flicker_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        flicker_surface.fill((255, 255, 255, 5))  # Slight white overlay
        screen.blit(flicker_surface, (0, 0))

def _apply_glow(screen):
    """Creates a soft glow effect by blurring bright pixels."""
    width, height = screen.get_size()

    # Create a blurred surface
    glow_surf = pygame.transform.smoothscale(screen, (width // 2, height // 2))
    glow_surf = pygame.transform.smoothscale(glow_surf, (width, height))

    # Overlay with transparency
    glow_surf.set_alpha(100)  # Adjust glow intensity (higher = stronger glow)
    screen.blit(glow_surf, (0, 0))

def _apply_vhs_glitch(screen):
    """Adds a VHS-style glitch effect with random tearing and color shifting."""
    width, height = screen.get_size()
    
    # Create a surface copy for distortions
    glitch_surface = screen.copy()

    # Glitch effect: randomly shift horizontal slices
    for _ in range(4):  # Number of glitch distortions
        if random.random() < 0.1:  # 10% chance of a glitch appearing
            y_start = random.randint(0, height - 20)
            slice_height = random.randint(5, 20)
            offset = random.randint(-20, 20)

            # Copy the slice, shift it, then paste it back
            slice_area = pygame.Rect(0, y_start, width, slice_height)
            slice_copy = glitch_surface.subsurface(slice_area).copy()
            glitch_surface.blit(slice_copy, (offset, y_start))

    # Color separation glitch (Red, Green, Blue channels slightly misaligned)
    if random.random() < 0.05:  # 5% chance of color glitch
        for i in range(3):  # RGB channels
            x_offset = random.randint(-2, 2)
            y_offset = random.randint(-2, 2)
            color_shift_surface = glitch_surface.copy()
            color_shift_surface.fill((0, 0, 0))
            color_shift_surface.blit(glitch_surface, (x_offset, y_offset))
            screen.blit(color_shift_surface, (0, 0), special_flags=pygame.BLEND_ADD)

    # Apply rolling static effect
    static_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(0, height, 8):  # Adjust for stronger static lines
        if random.random() < 0.2:  # 20% chance of static per line
            pygame.draw.line(static_surface, (255, 255, 255, random.randint(30, 80)), (0, y), (width, y))

    # Blend the static overlay
    screen.blit(static_surface, (0, 0), special_flags=pygame.BLEND_ADD)

    # Finally, blit the glitch effect back onto the screen
    screen.blit(glitch_surface, (0, 0))
