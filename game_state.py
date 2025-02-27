import math

from asteroid import Asteroid
from player import Player

class GameState:
    def __init__(self):
        """GameState manages all game objects"""
        self.player = Player()
        self.bullets = []
        self.asteroids = []

    def spawn_asteroids(self, count=5):
        """Spawn initial asteroids"""
        for _ in range(count):
            self.asteroids.append(Asteroid())

    def update_all(self, keys):
        """Update all game objects"""
        self.player.update(keys)
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.lifetime > 0]  # Cleanup expired bullets

        for asteroid in self.asteroids:
            asteroid.update()

    def draw_all(self, screen):
        self.player.draw(screen)
        """Draw all game objects"""
        for bullet in self.bullets:
            bullet.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)

    def check_for_collisions(self):
        """Check for bullet-asteroid collisions"""
        bullets_to_remove = []
        asteroids_to_remove = []

        for bullet in self.bullets[:]:  # Iterate over a copy
            for asteroid in self.asteroids[:]:  # Iterate over a copy
                dist = self.calculate_collision_distance(bullet, asteroid)
                if dist < asteroid.size:
                    bullets_to_remove.append(bullet)
                    asteroids_to_remove.append(asteroid)

                    # Asteroid splitting (Optional)
                    if asteroid.size > 30:
                        self.asteroids.append(Asteroid())  # Create a new one

        # Safely remove bullets & asteroids
        self.bullets = [b for b in self.bullets if b not in bullets_to_remove]
        self.asteroids = [a for a in self.asteroids if a not in asteroids_to_remove]

    def calculate_collision_distance(self, bullet, asteroid):
        dist = math.sqrt((bullet.x - asteroid.x)**2 + (bullet.y - asteroid.y)**2)
        return dist