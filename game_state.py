import pygame
from player import Player
from asteroid import Asteroid
from bullet import Bullet

class GameState:
    def __init__(self):
        """GameState manages all game objects."""
        self.player = Player()
        self.bullets = []
        self.asteroids = []

    def spawn_asteroids(self, count=5):
        """Spawn initial asteroids."""
        for _ in range(count):
            self.asteroids.append(Asteroid())

    def update_all(self, keys):
        """Update all game objects."""
        self.player.update(keys)
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.lifetime > 0]  # Cleanup expired bullets

        for asteroid in self.asteroids:
            asteroid.update()

    def draw_all(self, screen):
        """Draw all game objects."""
        self.player.draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)

    def check_for_collisions(self):
        """Check for bullet-asteroid collisions."""
        bullets_to_remove = []
        asteroids_to_remove = []
        new_asteroids = []

        for asteroid in self.asteroids[:]:  # Iterate over a copy
            for bullet in self.bullets[:]:  # Iterate over a copy
                dist = self.calculate_collision_distance(bullet, asteroid)
                if dist < asteroid.size:
                    bullets_to_remove.append(bullet)
                    asteroids_to_remove.append(asteroid)
                    new_asteroids.extend(asteroid.split())  # Add split asteroids

        # Safely remove bullets & asteroids
        self.bullets = [b for b in self.bullets if b not in bullets_to_remove]
        self.asteroids = [a for a in self.asteroids if a not in asteroids_to_remove]

        # Add new split asteroids
        self.asteroids.extend(new_asteroids)

    def calculate_collision_distance(self, obj1, obj2):
        """Calculates distance between two game objects."""
        dx = obj1.x - obj2.x
        dy = obj1.y - obj2.y
        return (dx ** 2 + dy ** 2) ** 0.5  # Euclidean distance formula
