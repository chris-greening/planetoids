import pygame
from start_menu import StartMenu
from game_state import GameState
import crt_effect
import config
import random
import time
import math

def main():
    pygame.init()

    # Initialize window
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Planetoids!")
    clock = pygame.time.Clock()

    _show_intro(screen, clock)

    # Show the start menu
    start_menu = StartMenu(screen, clock)
    crt_enabled = start_menu.show()  # Returns True or False

    # Create GameState instance
    game_state = GameState(screen, crt_enabled, clock)
    print(crt_enabled)
    game_state.spawn_asteroids(5)

    running = True
    while running:
        screen.fill(config.BLACK)
        clock.tick(config.FPS)

        _event_handler(game_state)

        if game_state.paused:
            continue

        # Update game state
        keys = pygame.key.get_pressed()
        game_state.update_all(keys)
        game_state.check_for_clear_map()
        game_state.check_for_collisions(screen)

        # Draw everything
        game_state.draw_all(screen)

        if game_state.crt_enabled:
            crt_effect.apply_crt_effect(screen)
        pygame.display.flip()

    pygame.quit()

def _glitch_effect(surface, text_surface, x, y):
    """Applies a glitch effect by shifting color channels and adding distortion."""
    width, height = text_surface.get_size()
    glitch_surf = text_surface.copy()

    for _ in range(5):  # Number of glitch passes
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


def _show_intro(screen, clock):
    """Displays the Greening Games intro with a hardcore glitch effect."""
    pygame.font.init()
    font = pygame.font.Font("assets/fonts/VT323.ttf", 80)  # Use a retro-style font

    # Generate the text surface
    text_surface = font.render("GREENING GAMES", True, config.GREEN)

    # Center the text
    text_x = (config.WIDTH - text_surface.get_width()) // 2
    text_y = (config.HEIGHT - text_surface.get_height()) // 2

    start_time = time.time()
    while time.time() - start_time < 3:  # Display for ~3 seconds
        # **Apply a dark blue background instead of black**
        screen.fill((10, 15, 30))  # Deep dark blue background

        # Apply glitch effect
        _glitch_effect(screen, text_surface, text_x, text_y)

        # Apply CRT effect (if enabled)
        crt_effect.apply_crt_effect(screen)

        pygame.display.flip()
        clock.tick(30)  # Control frame rate

    # Fade out effect
    fade_surface = pygame.Surface((config.WIDTH, config.HEIGHT))
    fade_surface.fill(config.BLACK)
    for alpha in range(0, 255, 10):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(30)

def _event_handler(game_state):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_state.toggle_pause()
            elif event.key == pygame.K_SPACE and not game_state.paused:
                game_state.bullets.extend(game_state.player.shoot())
        game_state.handle_powerup_expiration(event)

if __name__ == "__main__":
    main()

