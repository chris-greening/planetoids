import random

import pygame

def apply_crt_effect(screen, settings=None):
    """Apply CRT effect to the screen."""
    if settings is None:
        settings = {"pixelation": "minimum", "glitch_intensity": "medium"}
    _apply_scanlines(screen)
    _apply_pixelation(screen, settings.get("pixelation"))
    _apply_flicker(screen)
    _apply_glow(screen)
    _apply_vhs_glitch(screen, settings.get("glitch_intensity"))  # NEW: Add VHS glitch effect

def _apply_scanlines(screen):
    """Draws horizontal scanlines to simulate an old CRT screen."""
    width, height = screen.get_size()
    scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for y in range(0, height, 4):  # Every 4 pixels (adjust for intensity)
        pygame.draw.line(scanline_surface, (0, 0, 0, 60), (0, y), (width, y))  # Semi-transparent black

    screen.blit(scanline_surface, (0, 0))

def _apply_pixelation(screen, pixelation):
    """Reduces resolution slightly to create a pixelated effect."""
    pixelation = {"minimum": 2, "medium": 4, "maximum": 6}.get(pixelation, 2)
    width, height = screen.get_size()
    small_surf = pygame.transform.scale(screen, (width // pixelation, height // pixelation))
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

def _apply_vhs_glitch(screen, intensity):
    """Adds a VHS-style glitch effect based on intensity level."""
    width, height = screen.get_size()
    glitch_surface = screen.copy()

    glitch_count = {"minimum": 2, "medium": 4, "maximum": 8}.get(intensity, 4)

    for _ in range(glitch_count):
        _add_glitch_effect(height, width, glitch_surface, intensity)

    _add_color_separation(screen, glitch_surface, intensity)
    _add_rolling_static(screen, height, width, intensity)

    screen.blit(glitch_surface, (0, 0))

def _add_glitch_effect(height, width, glitch_surface, intensity):
    shift_amount = {"minimum": 10, "medium": 20, "maximum": 40}.get(intensity, 20)

    if random.random() < 0.1:
        y_start = random.randint(0, height - 20)
        slice_height = random.randint(5, 20)
        offset = random.randint(-shift_amount, shift_amount)

        slice_area = pygame.Rect(0, y_start, width, slice_height)
        slice_copy = glitch_surface.subsurface(slice_area).copy()
        glitch_surface.blit(slice_copy, (offset, y_start))

def _add_color_separation(screen, glitch_surface, intensity):
    color_shift = {"minimum": 2, "medium": 4, "maximum": 8}.get(intensity, 4)

    if random.random() < 0.05:
        for i in range(3):
            x_offset = random.randint(-color_shift, color_shift)
            y_offset = random.randint(-color_shift, color_shift)
            color_shift_surface = glitch_surface.copy()
            color_shift_surface.fill((0, 0, 0))
            color_shift_surface.blit(glitch_surface, (x_offset, y_offset))
            screen.blit(color_shift_surface, (0, 0), special_flags=pygame.BLEND_ADD)

def _add_rolling_static(screen, height, width, intensity):
    static_chance = {"minimum": 0.1, "medium": 0.2, "maximum": 0.5}.get(intensity, 0.2)

    static_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(0, height, 8):
        if random.random() < static_chance:
            pygame.draw.line(static_surface, (255, 255, 255, random.randint(30, 80)), (0, y), (width, y))

    screen.blit(static_surface, (0, 0), special_flags=pygame.BLEND_ADD)

