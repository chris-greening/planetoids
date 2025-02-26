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

    # Game loop
    player = Player()
    bullets = []
    asteroids = [Asteroid() for _ in range(5)]
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
                # Fire bullet
                bullets.append(Bullet(player.x, player.y, player.angle))


        _update_objects(player, bullets, asteroids)

        # Remove expired bullets
        bullets = [bullet for bullet in bullets if bullet.lifetime > 0]

        # Check for bullet-asteroid collisions
        for bullet in bullets:
            for asteroid in asteroids:
                dist = helpers.calculate_collision_distance(bullet, asteroid)
                if dist < asteroid.size:  # Collision detected
                    asteroids.remove(asteroid)
                    bullets.remove(bullet)
                    asteroids.append(Asteroid())  # Spawn a new one

        planet.draw(screen)
        _draw_objects(player, screen, bullets, asteroids)

        pygame.display.flip()

    pygame.quit()

def _draw_objects(player, screen, bullets, asteroids) -> None:
    # Draw objects
    player.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)

def _update_objects(player, bullets, asteroids) -> None:
    # Update objects
        player.update()
        for bullet in bullets:
            bullet.update()
        for asteroid in asteroids:
            asteroid.update()

if __name__ == "__main__":
    main()