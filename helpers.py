import math
import config
import pygame
import helpers
from asteroid import Asteroid

def calculate_collision_distance(bullet, asteroid):
    dist = math.sqrt((bullet.x - asteroid.x)**2 + (bullet.y - asteroid.y)**2)
    return dist

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

def draw_objects(player, screen, bullets, asteroids) -> None:
    """Draws all game objects on the screen."""
    player.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)

def update_objects(player, bullets, asteroids) -> None:
    """Updates all game objects."""
    keys = pygame.key.get_pressed()  # Get key states
    player.update(keys)  # Pass keys to player movement
    for bullet in bullets:
        bullet.update()
    for asteroid in asteroids:
        asteroid.update()

def check_for_collisions(bullets, asteroids):
    # Check for bullet-asteroid collisions
    for bullet in bullets:
        for asteroid in asteroids:
            dist = helpers.calculate_collision_distance(bullet, asteroid)
            if dist < asteroid.size:  # Collision detected
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                asteroids.append(Asteroid())  # Spawn a new one