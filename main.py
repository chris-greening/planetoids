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

        helpers.update_objects(player, bullets, asteroids)

        # Remove expired bullets
        bullets = [bullet for bullet in bullets if bullet.lifetime > 0]

        helpers.check_for_collisions(bullets, asteroids)

        # planet.draw(screen)
        helpers.draw_objects(player, screen, bullets, asteroids)

        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()
