import pygame
from player import Player
from asteroid import Asteroid
from bullet import Bullet
import config

class GameState:
    def __init__(self):
        """GameState manages all game objects, including the player and asteroids."""
        self.player = Player()
        self.bullets = []
        self.asteroids = []
        self.lives = 3  # Number of player lives
        self.respawn_timer = 0  # Prevent instant respawn collisions
        self.level = 1  # Start at level 1
        self.paused = False

    def toggle_pause(self):
        self.paused = not self.paused

    def check_for_clear_map(self):
        """Checks if all asteroids are destroyed and resets the map if so."""
        if not self.asteroids:  # If asteroid list is empty
            self.level += 1
            self.spawn_asteroids(5)  # Reset the map with new asteroids
            self.player.set_invincibility()

    def spawn_asteroids(self, count=5):
        """Spawn initial asteroids."""
        for _ in range(count):
            self.asteroids.append(Asteroid())

    def update_all(self, keys):
        """Update all game objects and check for player respawn cooldown."""
        if self.respawn_timer > 0:
            self.respawn_timer -= 1  # Countdown to prevent instant death loop
        else:
            self.player.update(keys)

        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.lifetime > 0]  # Cleanup expired bullets

        for asteroid in self.asteroids:
            asteroid.update()

    def draw_all(self, screen):
        """Draw all game objects."""
        if self.respawn_timer == 0:  # Only draw player if alive
            self.player.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)

        # Draw lives counter
        self._draw_lives(screen)
        self._draw_level(screen)

    def _draw_level(self, screen):
        """Display current level number."""
        font = pygame.font.Font(None, 36)
        text = font.render(f"Level: {self.level}", True, config.WHITE)
        screen.blit(text, (config.WIDTH - 120, 10))  # Display top-right

    def check_for_collisions(self, screen):
        """Check for bullet-asteroid and player-asteroid collisions."""
        bullets_to_remove = []
        asteroids_to_remove = []
        new_asteroids = []

        # Bullet vs Asteroid Collision
        for bullet in self.bullets[:]:  # Iterate over a copy
            for asteroid in self.asteroids[:]:  # Iterate over a copy
                dist = self.calculate_collision_distance(bullet, asteroid)
                if dist < asteroid.size:
                    bullets_to_remove.append(bullet)
                    asteroids_to_remove.append(asteroid)
                    new_asteroids.extend(asteroid.split())  # Add split asteroids

        # Player vs Asteroid Collision
        if self.respawn_timer == 0:  # Only check if player is alive
            for asteroid in self.asteroids:
                dist = self.calculate_collision_distance(self.player, asteroid)
                if dist < asteroid.size:  # Collision detected
                    self.handle_player_death(screen)  # Pass screen to function

        # Safely remove bullets & asteroids
        self.bullets = [b for b in self.bullets if b not in bullets_to_remove]
        self.asteroids = [a for a in self.asteroids if a not in asteroids_to_remove]

        # Add new split asteroids
        self.asteroids.extend(new_asteroids)

    def handle_player_death(self, screen):
        """Handles player death with an animation before respawn or game over."""
        if self.player.invincible:
            return  # Don't kill if invincible after respawn

        self.player.death_animation(screen)  # Pass screen to death effect

        self.lives -= 1
        if self.lives > 0:
            self.respawn_player()
        else:
            self.game_over()

    def respawn_player(self):
        """Respawns the player at the center after a short delay."""
        self.respawn_timer = 60  # 1 second delay
        self.player.reset_position()  # Now resets velocity and prevents instant death

    def game_over(self):
        """Ends the game and shows Game Over screen."""
        print("Game Over!")  # For now, just print (will be replaced with a menu)
        pygame.quit()
        exit()

    def _draw_lives(self, screen):
        """Display player lives on the screen."""
        font = pygame.font.Font(None, 36)
        text = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

    def calculate_collision_distance(self, obj1, obj2):
        """Calculates distance between two game objects."""
        dx = obj1.x - obj2.x
        dy = obj1.y - obj2.y
        return (dx ** 2 + dy ** 2) ** 0.5  # Euclidean distance formula
