import pygame
from player import Player
from asteroid import Asteroid
from bullet import Bullet
from powerups import PowerUp
from powerups import TrishotPowerUp, ShieldPowerUp, QuadShotPowerUp
from pause_menu import PauseMenu
import config
import random

class GameState:
    def __init__(self, screen):
        """GameState manages all game objects, including the player and asteroids."""
        self.screen = screen
        self.player = Player()
        self.bullets = []
        self.asteroids = []
        self.powerups = []
        self.lives = 3
        self.respawn_timer = 0
        self.level = 1
        self.paused = False
        self.pause_menu = PauseMenu(screen, self)  # Pass self to PauseMenu
        self.crt_enabled = True  # Default CRT effect setting
        self.score = 0  # Initialize score

    def update_score(self, asteroid):
        """Increase score based on asteroid size."""
        if asteroid.size >= 40:  # Large asteroid
            self.score += 100
        elif asteroid.size >= 20:  # Medium asteroid
            self.score += 200
        else:  # Small asteroid
            self.score += 300
        print(f"Score: {self.score}")  # Debugging

    def toggle_pause(self):
        """Toggles pause and shows the pause screen."""
        if not self.paused:
            self.paused = True
            self.pause_menu.show()  # Show pause menu
            self.paused = False  # Resume after exiting menu

    def spawn_powerup(self, x, y):
        """Spawns a power-up with a probability, allowing multiple to exist at once."""
        if len(self.powerups) < 3 and random.random() < .1:
            powerup_classes = [TrishotPowerUp, QuadShotPowerUp]
            print(powerup_classes)
            if not self.player.shield_active:
                powerup_classes.append(ShieldPowerUp)
            chosen_powerup = random.choice(powerup_classes)
            self.powerups.append(chosen_powerup(x, y))

    def check_for_clear_map(self):
        """Checks if all asteroids are destroyed and resets the map if so."""
        if not self.asteroids:  # If asteroid list is empty
            self.level += 1
            self.spawn_asteroids(5 + self.level * 2)  # Reset the map with new asteroids
            self.player.set_invincibility()

    def spawn_asteroids(self, count=5):
        """Spawn initial asteroids."""
        for _ in range(count):
            self.asteroids.append(Asteroid())

    def update_all(self, keys):
        """Update all game objects, including powerups."""
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            print(f"Respawning in {self.respawn_timer} frames")  # Debug
            if self.respawn_timer == 0:
                print("Respawning player now!")  # Debug
                self.respawn_player()
        else:
            self.player.update(keys)

        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.lifetime > 0] 

        for asteroid in self.asteroids:
            asteroid.update()

        # Update powerups
        for powerup in self.powerups:
            powerup.update()
        self.powerups = [p for p in self.powerups if not p.is_expired()]

        # Check if player collects a power-up
        self.check_powerup_collisions()

    def draw_all(self, screen):
        """Draw all game objects, including power-ups."""
        if self.respawn_timer == 0:
            self.player.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)

        for powerup in self.powerups:
            powerup.draw(screen)

        self._draw_lives(screen)
        self._draw_level(screen)
        self._draw_powerup_timer(screen)
        self._draw_score(screen)  # Draw score

    def _draw_score(self, screen):
        """Displays the score in the top-right corner."""
        font = pygame.font.Font(None, 36)  # Score font
        score_text = font.render(f"Score: {self.score}", True, config.WHITE)
        screen.blit(score_text, (config.WIDTH - 150, 20))  # Position in top-right

    def check_powerup_collisions(self):
        """Checks if the player collects a power-up."""
        for powerup in self.powerups[:]:
            if self.calculate_collision_distance(self.player, powerup) < powerup.radius + self.player.size:
                print(f"Player collected {powerup.__class__.__name__}!")  # Debug
                self.apply_powerup(powerup)  # Pass powerup instance
                self.powerups.remove(powerup)  # Remove after collection

    def apply_powerup(self, powerup):
        """Applies the collected power-up effect."""
        powerup.apply(self.player)  # Call the power-up's apply() method

    def _draw_level(self, screen):
        """Display current level number."""
        font = pygame.font.Font(None, 36)
        text = font.render(f"Level: {self.level}", True, config.WHITE)
        screen.blit(text, (config.WIDTH - 120, config.HEIGHT - 30))  # Display bottom-right

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
                    self.update_score(asteroid)
                    bullets_to_remove.append(bullet)
                    asteroids_to_remove.append(asteroid)
                    new_asteroids.extend(asteroid.split())  # Add split asteroids
                    self.spawn_powerup(asteroid.x, asteroid.y)

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
        if self.player.shield_active:
            self.player.take_damage()
            return

        self.player.death_animation(screen)  # Pass screen to death effect

        self.lives -= 1
        if self.lives > 0:
            self.respawn_player()
        else:
            self.game_over()

    def respawn_player(self):
        """Respawns the player at the center after the timer expires."""
        if self.respawn_timer > 0:
            return  # Prevent accidental multiple calls

        print("Respawning player!")  # Debugging
        self.player.reset_position()
        self.player.invincible = True
        pygame.time.set_timer(pygame.USEREVENT + 2, 2000)  # 2 sec invincibility

    def _draw_powerup_timer(self, screen):
        """Draws a shrinking timer bar for active powerups."""
        if self.player.powerup_timer > 0:
            bar_width = int((self.player.powerup_timer / 300) * 200)  # Scale to 200px max
            pygame.draw.rect(screen, (0, 255, 255), (config.WIDTH // 2 - 100, config.HEIGHT - 30, bar_width, 10))

    def game_over(self):
        """Ends the game and shows Game Over screen."""
        print("Game Over!")  # For now, just print (will be replaced with a menu)
        pygame.quit()
        exit()

    def _draw_lives(self, screen):
        """Display player lives on the screen."""
        font = pygame.font.Font(None, 36)
        text = font.render(f"Lives: {self.lives}", True, config.WHITE)
        screen.blit(text, (10, 10))

    def calculate_collision_distance(self, obj1, obj2):
        """Calculates distance between two game objects."""
        dx = obj1.x - obj2.x
        dy = obj1.y - obj2.y
        return (dx ** 2 + dy ** 2) ** 0.5  # Euclidean distance formula
