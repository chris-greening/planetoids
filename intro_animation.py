import pygame
import random
import time
import math
import config
from crt_effect import apply_crt_effect

class IntroAnimation:
    """Handles the Greening Games intro animation with glitch, vignette, and pixelation effects."""
    
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font("assets/fonts/VT323.ttf", 124)  # Retro pixel-style font
        self.text_surface = self.font.render("GREENING GAMES", True, config.GREEN)
        self.text_x = (config.WIDTH - self.text_surface.get_width()) // 2
        self.text_y = (config.HEIGHT - self.text_surface.get_height()) // 2

    def play(self):
        """Runs the intro animation with glitch, pixelation, and CRT effects."""
        start_time = time.time()
        while time.time() - start_time < 3:  # Show for ~3 seconds
            self.screen.fill((10, 15, 30))  # Deep blue background

            # Apply glitch effect
            self._glitch_effect(self.screen, self.text_surface, self.text_x, self.text_y)

            # Apply CRT effect (if enabled)
            apply_crt_effect(self.screen)

            pygame.display.flip()
            self.clock.tick(30)  # Control frame rate

        self._fade_out()  # Smooth transition

    def _glitch_effect(self, surface, text_surface, x, y):
        """Applies a glitch effect by shifting color channels and adding distortion."""
        width, height = text_surface.get_size()
        glitch_surf = text_surface.copy()

        for _ in range(10):  # Number of glitch passes
            shift_x = random.randint(-5, 5)
            shift_y = random.randint(-3, 3)

            # Ensure slice selection is within valid bounds
            slice_y = random.randint(0, max(0, height - 1))  # Clamp to valid range
            max_slice_height = max(2, min(8, height - slice_y))  # Ensure slice height is never less than 2
            if max_slice_height > 2:
                slice_height = random.randint(2, max_slice_height)
            else:
                slice_height = 2  # Default to 2 if no valid range

            # Only proceed if slice_height is valid
            if slice_height > 0 and slice_y + slice_height <= height:
                slice_rect = pygame.Rect(0, slice_y, width, slice_height)
                slice_surf = glitch_surf.subsurface(slice_rect).copy()
                surface.blit(slice_surf, (x + shift_x, y + shift_y))

        # Color separation effect
        for i, offset in enumerate([-2, 2, -1, 1]):
            color_shift_surf = text_surface.copy()
            color_shift_surf.fill((0, 0, 0))
            color_shift_surf.blit(text_surface, (offset, offset))
            surface.blit(color_shift_surf, (x, y), special_flags=pygame.BLEND_ADD)

            # 🔥 More frequent color separation for VHS-style distortion
            if random.random() < 0.8:  # 80% chance per frame
                for offset in [-3, 3, -2, 2]:
                    color_shift_surf = self.text_surface.copy()
                    color_shift_surf.fill((0, 0, 0))
                    color_shift_surf.blit(self.text_surface, (offset, offset))
                    self.screen.blit(color_shift_surf, (self.text_x, self.text_y), special_flags=pygame.BLEND_ADD)

    def _fade_out(self):
        """Fades out the intro animation before transitioning to the game."""
        fade_surface = pygame.Surface((config.WIDTH, config.HEIGHT))
        fade_surface.fill(config.BLACK)
        for alpha in range(0, 255, 10):
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(30)
