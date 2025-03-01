import pygame
from player import Player
from asteroid import Asteroid, ExplodingAsteroid
from bullet import Bullet
from powerups import PowerUp, TemporalSlowdownPowerUp
from pause_menu import PauseMenu
import config
import random

class GameState:
    def __init__(self, screen, crt_enabled):
        """GameState manages all game objects, including the player and asteroids."""
        self.screen = screen
        self.crt_enabled = crt_enabled
        self.player = Player()
        self.bullets = []
        self.asteroids = []
        self.powerups = []
        self.lives = 3
        self.respawn_timer = 0
        self.level = 1
        self.paused = False
        self.pause_menu = PauseMenu(screen, self)
        self.score = 0
        self.asteroid_slowdown_active = False
        self.slowdown_timer = 0

    def update_score(self, asteroid):
        """Increase score based on asteroid size."""
        if asteroid.size >= 40:
            self.score += 100
        elif asteroid.size >= 20:
            self.score += 200
        else:
            self.score += 300
        print(f"Score: {self.score}")

    def toggle_pause(self):
        """Toggles pause and shows the pause screen."""
        if not self.paused:
            self.paused = True
            self.pause_menu.show()
            self.paused = False

    def spawn_powerup(self, x, y):
        """Spawns a power-up with a probability, allowing multiple to exist at once."""
        if len(self.powerups) < 3 and random.random() < .1:
            powerup_classes = PowerUp.get_powerups()
            if not self.player.shield_active:
                powerup_classes = [
                    p for p in powerup_classes if p.__name__ != "ShieldPowerUp"
                ]
            chosen_powerup = random.choice(powerup_classes)
            self.powerups.append(chosen_powerup(x, y))

    def check_for_clear_map(self):
        """Checks if all asteroids are destroyed and resets the map if so."""
        if not self.asteroids:
            self.level += 1
            self.spawn_asteroids(5 + self.level * 2)
            self.player.set_invincibility()

    def spawn_asteroids(self, count=5):
        """Spawn initial asteroids."""
        for _ in range(count):
            if random.random() < .5:
                self.asteroids.append(ExplodingAsteroid())
            else:
                self.asteroids.append(Asteroid())

    def update_all(self, keys):
        """Update all game objects, including power-ups and explosions."""

        # Handle player respawn
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            print(f"Respawning in {self.respawn_timer} frames")
            if self.respawn_timer == 0:
                print("Respawning player now!")
                self.respawn_player()
        else:
            self.player.update(keys)

        # Update bullets
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.lifetime > 0]

        # Update asteroids and handle explosion removals
        asteroids_to_remove = []
        for asteroid in self.asteroids:
            if isinstance(asteroid, ExplodingAsteroid) and asteroid.exploding:
                asteroid.update_explosion()
                if asteroid.explosion_timer <= 0:  # Remove after explosion ends
                    asteroids_to_remove.append(asteroid)
            else:
                asteroid.update(self)

        # Remove exploding asteroids after animation finishes
        self.asteroids = [a for a in self.asteroids if a not in asteroids_to_remove]

        # Update power-ups
        for powerup in self.powerups:
            powerup.update()
        self.powerups = [p for p in self.powerups if not p.is_expired()]

        # Check if player collects a power-up
        self.check_powerup_collisions()


    def handle_powerup_expiration(self, event):
        """Handles expiration events for power-ups."""
        if event.type == pygame.USEREVENT + 5:
            self.asteroid_slowdown_active = False

    def draw_all(self, screen):
        """Draw all game objects, including power-ups."""
        if self.respawn_timer == 0:
            self.player.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)
            if isinstance(asteroid, ExplodingAsteroid) and asteroid.exploding:
                asteroid.draw_explosion(screen)
        for powerup in self.powerups:
            powerup.draw(screen)

        self._draw_lives(screen)
        self._draw_level(screen)
        self._draw_powerup_timer(screen)
        self._draw_score(screen)  # Draw score

        self._asteroid_slowdown_active(screen)

    def _asteroid_slowdown_active(self, screen):
        # Draw slowdown visual effect
        if self.asteroid_slowdown_active:
            # Calculate elapsed time since slowdown started
            total_duration = 5000  # 5 seconds in milliseconds
            time_elapsed = total_duration - max(0, self.slowdown_timer - pygame.time.get_ticks())

            # Calculate opacity: Starts at 70 and smoothly decreases to 0
            fade_intensity = max(0, int(70 * (1 - (time_elapsed / total_duration))))

            # Create semi-transparent blue overlay
            overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 150, 255, fade_intensity))  # Softer cyan overlay
            screen.blit(overlay, (0, 0))

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
        if isinstance(powerup, TemporalSlowdownPowerUp):
            self.slowdown_timer = pygame.time.get_ticks() + 5000  # 5 seconds
            self.asteroid_slowdown_active = True
            pygame.time.set_timer(pygame.USEREVENT + 5, 5000)
        else:
            powerup.apply(self.player)  # Call the power-up's apply() method

    def _draw_level(self, screen):
        """Display current level number."""
        font = pygame.font.Font(None, 36)
        text = font.render(f"Level: {self.level}", True, config.WHITE)
        screen.blit(text, (config.WIDTH - 120, config.HEIGHT - 30))  # Display bottom-right

    def _handle_bullet_asteroid_collision(self):
        bullets_to_remove = []
        asteroids_to_remove = []
        new_asteroids = []

        for bullet in self.bullets[:]:  # Iterate over a copy
            for asteroid in self.asteroids[:]:  # Iterate over a copy
                dist = self.calculate_collision_distance(bullet, asteroid)
                if dist < asteroid.size:
                    bullet.on_hit_asteroid(asteroid)
                    self.update_score(asteroid)

                    if isinstance(asteroid, ExplodingAsteroid):
                        if not asteroid.exploding:  # Start explosion if not already started
                            asteroid.explode(self.asteroids)

                        # The explosion should not remove the asteroid immediately
                        exploded_asteroids = asteroid.explode(self.asteroids)
                        for exploded_asteroid in exploded_asteroids:
                            self.update_score(exploded_asteroid)  # Score for each destroyed asteroid
                            asteroids_to_remove.append(exploded_asteroid)  # Remove after explosion
                            new_asteroids.extend(exploded_asteroid.split())

                    else:
                        asteroids_to_remove.append(asteroid)  # Non-exploding asteroids get removed normally
                        new_asteroids.extend(asteroid.split())  # Add split asteroids

                    if not bullet.piercing:
                        bullets_to_remove.append(bullet)

                    self.spawn_powerup(asteroid.x, asteroid.y)

                    if self.player.ricochet_active and not bullet.ricochet:
                        new_angle = random.randint(0, 360)  # Random ricochet angle
                        ricochet_bullet = Bullet(asteroid.x, asteroid.y, new_angle, ricochet=True)
                        self.bullets.append(ricochet_bullet)

        # Remove only **non-exploding** asteroids immediately
        self.asteroids = [a for a in self.asteroids if a not in asteroids_to_remove or (isinstance(a, ExplodingAsteroid) and a.exploding)]

        # Add new split asteroids
        self.asteroids.extend(new_asteroids)

        # Remove bullets
        self.bullets = [b for b in self.bullets if b not in bullets_to_remove]


    def _handle_player_asteroid_collision(self, screen):
        if self.respawn_timer == 0:  # Only check if player is alive
            for asteroid in self.asteroids:
                dist = self.calculate_collision_distance(self.player, asteroid)
                if dist < asteroid.size:  # Collision detected
                    self.handle_player_collision(screen)  # Pass screen to function

    def check_for_collisions(self, screen):
        """Check for bullet-asteroid and player-asteroid collisions."""
        self._handle_bullet_asteroid_collision()
        self._handle_player_asteroid_collision(screen)

    def handle_player_collision(self, screen):
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
