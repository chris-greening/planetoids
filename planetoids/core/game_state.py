import random
import os

import pygame

from planetoids.entities.player import Player
from planetoids.entities.asteroid import Asteroid, ExplodingAsteroid
from planetoids.entities.bullet import Bullet
from planetoids.entities.powerups import PowerUp, TemporalSlowdownPowerUp
from planetoids.ui.pause_menu import PauseMenu
from planetoids.core import config
from planetoids.effects import crt_effect

class GameState:
    def __init__(self, screen, crt_enabled, clock):
        """GameState manages all game objects, including the player and asteroids."""
        self.screen = screen
        self.crt_enabled = crt_enabled
        self.clock = clock
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
        self.font_path = os.path.join("assets", "fonts", "VT323.ttf")  # ✅ More sci-fi, less cartoony
        self.font = pygame.font.Font(self.font_path, 36)  # ✅ Larger for title

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
            if random.random() < .02:
                self.asteroids.append(ExplodingAsteroid())
            # elif random.random() < .5:
            #     self.asteroids.append(IceAsteroid())
            else:
                self.asteroids.append(Asteroid())

    def update_all(self, keys):
        """Update all game objects, including power-ups, bullets, asteroids, and explosions."""

        self.player.slowed_by_ice = False  # Reset ice slowdown before checking

        self._update_respawn(keys)
        self._update_bullets()
        self._update_asteroids()
        self._update_powerups()
        self.check_powerup_collisions()

        if self.player.explosion_timer > 0:
            self.player._update_explosion()

        # Restore player speed if not affected by ice
        if not self.player.slowed_by_ice:
            self.player.velocity_x = max(self.player.velocity_x, self.player.base_velocity_x)
            self.player.velocity_y = max(self.player.velocity_y, self.player.base_velocity_y)

    def _update_respawn(self, keys):
        """Handles player respawn countdown and resets the player when ready."""
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            print(f"Respawning in {self.respawn_timer} frames")
            if self.respawn_timer == 0:
                print("Respawning player now!")
                self.respawn_player()
        else:
            self.player.update(keys)

    def _update_bullets(self):
        """Updates bullets and removes expired ones."""
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.lifetime > 0]

    def _update_asteroids(self):
        """Updates asteroids, handles explosion animations, and removes destroyed asteroids."""
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

    def _update_powerups(self):
        """Updates power-ups and removes expired ones."""
        for powerup in self.powerups:
            powerup.update()
        self.powerups = [p for p in self.powerups if not p.is_expired()]

    def handle_powerup_expiration(self, event):
        """Handles expiration events for power-ups."""
        if event.type == pygame.USEREVENT + 5:
            self.asteroid_slowdown_active = False

    def _draw_bullets(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

    def _draw_asteroids(self, screen):
        for asteroid in self.asteroids:
            asteroid.draw(screen)
            if isinstance(asteroid, ExplodingAsteroid) and asteroid.exploding:
                asteroid.draw_explosion(screen)

    def _draw_powerups(self, screen):
        for powerup in self.powerups:
            powerup.draw(screen)

    def _draw_player(self, screen):
        if self.player.explosion_timer > 0:
            self.player._draw_explosion(screen)
        else:
            self.player.draw(screen)

    def draw_all(self, screen):
        """Draw all game objects, including power-ups."""
        self._draw_player(screen)
        self._draw_asteroids(screen)
        self._draw_powerups(screen)
        self._draw_bullets(screen)
        self._draw_lives(screen)
        self._draw_level(screen)
        self._draw_powerup_timer(screen)
        self._draw_score(screen)

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
        score_text = self.font.render(f"Score: {self.score}", True, config.WHITE)
        screen.blit(score_text, (config.WIDTH - 200, 20))  # Position in top-right

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
        text = self.font.render(f"Level: {self.level}", True, config.WHITE)
        screen.blit(text, (config.WIDTH - 120, config.HEIGHT - 30))  # Display bottom-right

    def _handle_bullet_asteroid_collision(self):
        """Handles collisions between bullets and asteroids."""

        bullets_to_remove = []
        asteroids_to_remove = []
        new_asteroids = []

        for bullet in self.bullets[:]:  # Iterate over a copy
            for asteroid in self.asteroids[:]:  # Iterate over a copy
                if self._is_bullet_asteroid_collision(bullet, asteroid):
                    self._process_bullet_hit(bullet, asteroid, bullets_to_remove, asteroids_to_remove, new_asteroids)

        self._remove_destroyed_asteroids(asteroids_to_remove)
        self.asteroids.extend(new_asteroids)  # Add newly split asteroids
        self.bullets = self._remove_used_bullets(self.bullets, bullets_to_remove)

    def _remove_used_bullets(self, bullets, bullets_to_remove):
        return [b for b in bullets if b not in bullets_to_remove]

    def _is_bullet_asteroid_collision(self, bullet, asteroid):
        """Returns True if a bullet collides with an asteroid."""
        return self.calculate_collision_distance(bullet, asteroid) < asteroid.size

    def _process_bullet_hit(self, bullet, asteroid, bullets_to_remove, asteroids_to_remove, new_asteroids):
        """Handles the effects of a bullet hitting an asteroid."""

        self._apply_bullet_effects(bullet, asteroid)
        self._handle_asteroid_destruction(asteroid, asteroids_to_remove, new_asteroids)

        if not bullet.piercing:
            bullets_to_remove.append(bullet)

        self._handle_powerup_spawn(asteroid)
        self._handle_ricochet_bullet(bullet, asteroid)

    def _apply_bullet_effects(self, bullet, asteroid):
        """Applies effects when a bullet hits an asteroid."""
        bullet.on_hit_asteroid(asteroid)
        self.update_score(asteroid)

    def _handle_asteroid_destruction(self, asteroid, asteroids_to_remove, new_asteroids):
        """Determines how an asteroid is destroyed or split."""
        if isinstance(asteroid, ExplodingAsteroid):
            self._handle_exploding_asteroid(asteroid, asteroids_to_remove, new_asteroids)
        else:
            asteroids_to_remove.append(asteroid)  # Remove normal asteroids
            new_asteroids.extend(asteroid.split())  # Add split asteroids

    def _handle_powerup_spawn(self, asteroid):
        """Spawns a power-up at the asteroid’s location if conditions are met."""
        self.spawn_powerup(asteroid.x, asteroid.y)

    def _handle_ricochet_bullet(self, bullet, asteroid):
        """Creates a ricochet bullet if the player has ricochet active."""
        if self.player.ricochet_active and not bullet.ricochet:
            self._spawn_ricochet_bullet(asteroid.x, asteroid.y)

    def _handle_exploding_asteroid(self, asteroid, asteroids_to_remove, new_asteroids):
        """Triggers an asteroid explosion and manages affected asteroids."""

        if not asteroid.exploding:  # Start explosion if not already started
            asteroid.explode(self.asteroids)

        exploded_asteroids = asteroid.explode(self.asteroids)
        for exploded_asteroid in exploded_asteroids:
            self.update_score(exploded_asteroid)
            asteroids_to_remove.append(exploded_asteroid)
            new_asteroids.extend(exploded_asteroid.split())

    def _spawn_ricochet_bullet(self, x, y):
        """Creates and adds a ricochet bullet."""
        new_angle = random.randint(0, 360)  # Random ricochet angle
        ricochet_bullet = Bullet(x, y, new_angle, ricochet=True)
        self.bullets.append(ricochet_bullet)

    def _remove_destroyed_asteroids(self, asteroids_to_remove):
        """Removes non-exploding asteroids that were destroyed."""
        self.asteroids = [
            a for a in self.asteroids
            if a not in asteroids_to_remove or (isinstance(a, ExplodingAsteroid) and a.exploding)
        ]

    def _handle_player_asteroid_collision(self, screen):
        """Handles collisions between the player and asteroids, triggering the explosion before respawn."""

        if self.respawn_timer > 0:
            return  # Player is currently respawning, ignore collisions

        for asteroid in self.asteroids:
            if self._is_collision(self.player, asteroid):
                self._trigger_player_explosion(screen)
                break  # Stop checking after first collision

    def _is_collision(self, entity1, entity2):
        """Returns True if two entities are colliding based on their distance."""
        return self.calculate_collision_distance(entity1, entity2) < entity2.size

    def _trigger_player_explosion(self, screen):
        """Handles the player explosion animation and sets up respawn or game over."""

        if self.player.invincible:
            return  # Skip if player is currently invincible

        if self.player.shield_active:
            self.player.take_damage()
            return  # Shield absorbs the hit

        self.player._generate_explosion()  # Trigger explosion animation
        self.respawn_timer = 30  # Delay respawn for explosion duration

        self.lives -= 1
        if self.lives <= 0:
            self.game_over(screen)  # No lives left, game over

    def check_for_collisions(self, screen):
        """Check for bullet-asteroid and player-asteroid collisions."""
        self._handle_bullet_asteroid_collision()
        self._handle_player_asteroid_collision(screen)

    def handle_player_collision(self, screen):
        """Handles player collision logic, including shield effects, death animation, and respawn/game over."""

        if self._player_is_invincible():
            return

        if self._player_has_shield():
            return

        self._process_player_death(screen)

    def _player_is_invincible(self):
        """Checks if the player is invincible after respawn."""
        return self.player.invincible

    def _player_has_shield(self):
        """Checks if the player has an active shield and applies damage if so."""
        if self.player.shield_active:
            self.player.take_damage()
            return True
        return False

    def _process_player_death(self, screen):
        """Handles player death animation, life count, and respawn or game over."""
        self.player.death_animation(screen)  # Play death effect
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

    def game_over(self, screen):
        """Ends the game and shows Game Over screen."""
        self._display_game_over(screen)  # For now, just print (will be replaced with a menu)
        pygame.quit()
        exit()

    def _display_game_over(self, screen):
        """Displays 'GAME OVER' while the game keeps running, showing moving asteroids in the background."""
        font_path = os.path.join("assets", "fonts", "VT323.ttf")
        game_over_font = pygame.font.Font(font_path, 64)

        text = game_over_font.render("GAME OVER", True, config.YELLOW)
        text_rect = text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2))

        game_over = True
        while game_over:
            screen.fill(config.BLACK)

            # Keep updating & drawing asteroids so they continue moving
            for asteroid in self.asteroids:
                asteroid.update(self)
                asteroid.draw(screen)

            # Draw the "GAME OVER" text
            screen.blit(text, text_rect)

            if self.crt_enabled:
                crt_effect.apply_crt_effect(screen)

            pygame.display.flip()
            self.clock.tick(config.FPS)

            # Wait for a key press to return to the main menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:  # Any key press exits the game over screen
                    game_over = False

    def _draw_lives(self, screen):
        """Displays remaining player lives as small triangles in the top-right corner, Galaga-style."""
        ship_size = 15  # Adjust size of the life icons
        spacing = 10     # Spacing between ships
        start_x = 10
        start_y = 18     # Position at the top-right corner

        for i in range(self.lives - 1):
            x_offset = start_x + i * (ship_size + spacing)

            # Triangle points for the small ship
            front = (x_offset, start_y - ship_size)
            left = (x_offset - ship_size * 0.6, start_y + ship_size * 0.6)
            right = (x_offset + ship_size * 0.6, start_y + ship_size * 0.6)

            # Draw the mini ship
            pygame.draw.polygon(screen, config.WHITE, [front, left, right], 1)

    def calculate_collision_distance(self, obj1, obj2):
        """Calculates distance between two game objects."""
        dx = obj1.x - obj2.x
        dy = obj1.y - obj2.y
        return (dx ** 2 + dy ** 2) ** 0.5  # Euclidean distance formula
