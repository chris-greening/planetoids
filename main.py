import pygame
from player import Player
from asteroid import Asteroid
from bullet import Bullet
from planet import Planet
import config
import helpers

def main() -> None:
    # Initialize Pygame
    pygame.init()

    # Initialize window
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Asteroids Clone")
    clock = pygame.time.Clock()

    # Show start menu before the game starts
    helpers.show_start_menu(screen, clock)

    # Game objects
    player = Player()
    for _ in range(5):  # Create initial asteroids
        Asteroid.create()
    planet = Planet()

    running = True
    while running:
        screen.fill(config.BLACK)
        clock.tick(config.FPS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Fire a bullet
                Bullet.create(player.x, player.y, player.angle)

        # Update all objects
        keys = pygame.key.get_pressed()
        player.update(keys)
        Bullet.update_all()
        Asteroid.update_all()

        # Check for collisions
        helpers.check_for_collisions(Bullet.bullets, Asteroid.asteroids)

        # Draw everything
        # planet.draw(screen)
        player.draw(screen)
        Bullet.draw_all(screen)
        Asteroid.draw_all(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
