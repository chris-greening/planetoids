import random
import time

import pygame

from planetoids.core.config import config
from planetoids.effects.crt_effect import apply_crt_effect
from planetoids.core.logger import logger
from planetoids.core.settings import get_font_path

class IntroAnimation:
    """Handles the Greening Games intro animation with glitch, terminal typing, and CRT effects."""

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font(get_font_path(), 120)  # Retro pixel-style font
        self.text = "GREENING STUDIO"  # Full text
        self.typed_text = ""  # What has been typed so far
        self.cursor_visible = True  # Blinking cursor state
        self.cursor_timer = time.time()  # Timer for cursor blinking
        self.text_x = (config.WIDTH - self.font.size(self.text)[0]) // 2
        self.text_y = (config.HEIGHT - self.font.size(self.text)[1]) // 2
        self.typing_speed = 0.06  # Faster typing (reduced delay per character)
        logger.info("IntroAnimation instantiated")

    def play(self):
        """Runs the intro animation with terminal typing effect, glitch, and CRT effects."""
        logger.info("Intro animation playing")
        start_time = time.time()
        char_index = 0  

        while char_index < len(self.text) or time.time() - start_time < 1.8:  # Reduced total time
            self.screen.fill((10, 15, 30))  

            # Faster typing effect
            if char_index < len(self.text) and time.time() - start_time > char_index * self.typing_speed:
                self.typed_text += self.text[char_index]
                char_index += 1

            # Blinking cursor
            if time.time() - self.cursor_timer > 0.3:  # Faster blinking
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = time.time()

            # Render text with cursor
            display_text = f"> {self.typed_text}{'_' if self.cursor_visible else ' '}"
            text_surface = self.font.render(display_text, True, config.GREEN)

            # Glitch effect
            self._glitch_effect(self.screen, text_surface, self.text_x, self.text_y)

            # CRT effect
            apply_crt_effect(self.screen)

            pygame.display.flip()
            self.clock.tick(40)  # Faster frame rate for smoother effect

        self._sequential_glitch_out()  

    def _glitch_effect(self, surface, text_surface, x, y):
        """Applies a glitch effect by shifting color channels and adding distortion."""
        width, height = text_surface.get_size()
        glitch_surf = text_surface.copy()

        for _ in range(6):  # Fewer glitch passes for speed
            shift_x = random.randint(-4, 4)
            shift_y = random.randint(-2, 2)

            slice_y = random.randint(0, max(0, height - 1))  
            slice_height = random.randint(2, max(6, height - slice_y))  

            if slice_y + slice_height <= height:
                slice_rect = pygame.Rect(0, slice_y, width, slice_height)
                slice_surf = glitch_surf.subsurface(slice_rect).copy()
                surface.blit(slice_surf, (x + shift_x, y + shift_y))

        # Color separation effect
        for offset in [-2, 2]:
            color_shift_surf = text_surface.copy()
            color_shift_surf.fill((0, 0, 0))
            color_shift_surf.blit(text_surface, (offset, offset))
            surface.blit(color_shift_surf, (x, y), special_flags=pygame.BLEND_ADD)

    def _sequential_glitch_out(self):
        """Sequentially glitches out each letter into garbage characters, then keeps glitching for a bit longer."""
        logger.info("Sequential glitch out triggered")
        glitched_text = list(self.text)
        char_pool = "!@#$%^&*()_+=<>?/\\|{}[]"

        for i in range(len(glitched_text)):
            for _ in range(4):  # Control glitch speed
                self.screen.fill((10, 15, 30))

                # Randomly corrupt letters up to `i`
                for j in range(i + 1):
                    if random.random() < 0.8:
                        glitched_text[j] = random.choice(char_pool)

                display_text = f"> {''.join(glitched_text)}_"
                text_surface = self.font.render(display_text, True, config.RED)

                # Heavy glitch effect
                self._glitch_effect(self.screen, text_surface, self.text_x, self.text_y)

                # CRT effect
                apply_crt_effect(self.screen)

                pygame.display.flip()
                self.clock.tick(25)

        # **Extra 0.5s of continuous glitching before fade-out**
        end_time = time.time() + .75
        while time.time() < end_time:
            self.screen.fill((10, 15, 30))

            # More aggressive glitching
            corrupted_text = ''.join(random.choice(char_pool) for _ in glitched_text)
            text_surface = self.font.render(f"> {corrupted_text}_", True, config.RED)

            # Heavy glitch effect
            self._glitch_effect(self.screen, text_surface, self.text_x, self.text_y)

            # CRT effect
            apply_crt_effect(self.screen)

            pygame.display.flip()
            self.clock.tick(25)  # Keep the chaotic effect running

        self._fade_out()


    def _fade_out(self):
        """Fades out the intro animation faster than before."""
        logger.info("Intro animation fadeout")
        fade_surface = pygame.Surface((config.WIDTH, config.HEIGHT))
        fade_surface.fill(config.BLACK)
        for alpha in range(0, 255, 20):  # Increased fade step size
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(30)  
