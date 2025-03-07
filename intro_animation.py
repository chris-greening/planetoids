import pygame
import random
import time
import config
from crt_effect import apply_crt_effect

class IntroAnimation:
    """Handles the Greening Games intro animation with glitch, terminal typing, and CRT effects."""

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font("assets/fonts/VT323.ttf", 80)  # Retro pixel-style font
        self.text = "GREENING GAMES"  # Full text
        self.typed_text = ""  # What has been typed so far
        self.cursor_visible = True  # Blinking cursor state
        self.cursor_timer = time.time()  # Timer for cursor blinking
        self.text_x = (config.WIDTH - self.font.size(self.text)[0]) // 2
        self.text_y = (config.HEIGHT - self.font.size(self.text)[1]) // 2
        self.typing_speed = 0.07  # Speed of typing effect (seconds per character)

    def play(self):
        """Runs the intro animation with terminal typing effect, glitch, and CRT effects."""
        start_time = time.time()
        char_index = 0  # Tracks how much of the text has been typed

        while char_index < len(self.text) or time.time() - start_time < 3:
            self.screen.fill((10, 15, 30))  # Deep blue background

            # Type one character at a time
            if char_index < len(self.text) and time.time() - start_time > char_index * self.typing_speed:
                self.typed_text += self.text[char_index]
                char_index += 1

            # Blinking cursor effect
            if time.time() - self.cursor_timer > 0.4:  # Blinks every 0.4s
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = time.time()

            # Render the text with a blinking cursor
            display_text = f"> {self.typed_text}{'_' if self.cursor_visible else ' '}"
            text_surface = self.font.render(display_text, True, config.GREEN)

            # Apply glitch effect
            self._glitch_effect(self.screen, text_surface, self.text_x, self.text_y)

            # Apply CRT effect (if enabled)
            apply_crt_effect(self.screen)

            pygame.display.flip()
            self.clock.tick(30)  # Control frame rate

        self._sequential_glitch_out()  # Letter-by-letter corruption before fade

    def _glitch_effect(self, surface, text_surface, x, y):
        """Applies a glitch effect by shifting color channels and adding distortion."""
        width, height = text_surface.get_size()
        glitch_surf = text_surface.copy()

        for _ in range(8):  # Number of glitch passes
            shift_x = random.randint(-5, 5)
            shift_y = random.randint(-3, 3)

            # Ensure slice selection is within valid bounds
            slice_y = random.randint(0, max(0, height - 1))  # Clamp to valid range
            max_slice_height = max(2, min(8, height - slice_y))  # Ensure slice height is never less than 2
            slice_height = random.randint(2, max_slice_height)

            # Only proceed if slice_height is valid
            if slice_y + slice_height <= height:
                slice_rect = pygame.Rect(0, slice_y, width, slice_height)
                slice_surf = glitch_surf.subsurface(slice_rect).copy()
                surface.blit(slice_surf, (x + shift_x, y + shift_y))

        # Color separation effect
        for offset in [-3, 3, -2, 2]:
            color_shift_surf = text_surface.copy()
            color_shift_surf.fill((0, 0, 0))
            color_shift_surf.blit(text_surface, (offset, offset))
            surface.blit(color_shift_surf, (x, y), special_flags=pygame.BLEND_ADD)

    def _sequential_glitch_out(self):
        """Sequentially glitches out each letter into garbage characters."""
        glitched_text = list(self.text)
        char_pool = "!@#$%^&*()_+=<>?/\\|{}[]"

        for i in range(len(glitched_text)):
            for _ in range(5):  # Rapid glitch effect per letter
                self.screen.fill((10, 15, 30))  # Keep background consistent

                # Randomly replace letters up to `i` with glitch chars
                for j in range(i + 1):
                    if random.random() < 0.6:  # 60% chance of corruption
                        glitched_text[j] = random.choice(char_pool)

                display_text = f"> {''.join(glitched_text)}_"
                text_surface = self.font.render(display_text, True, config.RED)

                # Heavy glitch effects during corruption
                self._glitch_effect(self.screen, text_surface, self.text_x, self.text_y)

                # Apply CRT effect
                apply_crt_effect(self.screen)

                pygame.display.flip()
                self.clock.tick(15)  # Slower updates for impact

        self._fade_out()  # Smooth transition

    def _fade_out(self):
        """Fades out the intro animation after glitching out."""
        fade_surface = pygame.Surface((config.WIDTH, config.HEIGHT))
        fade_surface.fill(config.BLACK)
        for alpha in range(0, 255, 10):
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(30)
