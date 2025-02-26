import pygame
import math
from player import Player
from asteroid import Asteroid
from bullet import Bullet
import constants

# Initialize Pygame
pygame.init()

# Initialize window
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Asteroids Clone")
clock = pygame.time.Clock()

# Helper function for rotation
def rotate_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=(x, y))
    return rotated_image, new_rect.topleft

# Game loop
player = Player()
bullets = []
asteroids = [Asteroid() for _ in range(5)]

running = True
while running:
    screen.fill(constants.BLACK)
    clock.tick(constants.FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Fire bullet
            bullets.append(Bullet(player.x, player.y, player.angle))

    # Update objects
    player.update()
    for bullet in bullets:
        bullet.update()
    for asteroid in asteroids:
        asteroid.update()

    # Remove expired bullets
    bullets = [bullet for bullet in bullets if bullet.lifetime > 0]

    # Check for bullet-asteroid collisions
    for bullet in bullets:
        for asteroid in asteroids:
            dist = math.sqrt((bullet.x - asteroid.x)**2 + (bullet.y - asteroid.y)**2)
            if dist < asteroid.size:  # Collision detected
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                asteroids.append(Asteroid())  # Spawn a new one

    # Draw objects
    player.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)

    pygame.display.flip()

pygame.quit()
