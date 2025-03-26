"""Contains the central game state manager"""

import random
from typing import List

import pygame

from planetoids.entities.asteroid import (
    Asteroid, ExplodingAsteroid, ShieldAsteroid
)
from planetoids.entities.powerups import (
    PowerUp, TemporalSlowdownPowerUp, RicochetShotPowerUp,
    InvincibilityPowerUp, TrishotPowerUp, QuadShotPowerUp
)
from planetoids.entities.bullet import Bullet
from planetoids.entities.player import Player
from planetoids.ui.pause_menu import PauseMenu
from planetoids.core.score import Score
from planetoids.core.level import Level
from planetoids.core.life import Life
from planetoids.core.config import config
from planetoids.core.logger import logger
from planetoids.core.settings import Settings
from planetoids.entities.score_popup import ScorePopup

class GameState:
    """GameState manages all game objects, including the player and asteroids."""
    def __init__(
            self, screen: pygame.Surface, settings: Settings,
            clock: pygame.time.Clock
        ):
        self.screen = screen
        self.settings = settings
        self.clock = clock
        self.player = Player(self.settings, self)
        self.bullets = []
        self.asteroids = []
        self.powerups = []
        self.life = Life(self.settings)
        self.respawn_timer = 0
        self.level = Level(self.settings)
        self.paused = False
        self.pause_menu = PauseMenu(screen, self)
        self.score = Score(self.settings)
        self.asteroid_slowdown_active = False
        self.slowdown_timer = 0
        self.dt = 1.0
        logger.info("GameState instantiated")
        self.score_popups = []
        self.debris = []
        self.shots_fired = 0
        self.asteroids_destroyed = 0
        self.shots_hit = 0
        self.start_time = pygame.time.get_ticks()

    @property
    def font(self) -> pygame.font.Font:
        """Returns font adjusted due to pixelation intensity"""
        return pygame.font.Font(
            self.settings.FONT_PATH,
            {"minimum":36, "medium": 48, "maximum": 64}.get(self.settings.get("pixelation"), 36)
        )

    def update_dt(self, dt: float) -> None:
        """Updates dt each frame to maintain FPS independence."""
        self.dt = dt

    def toggle_pause(self) -> None:
        """Toggles pause and shows the pause screen."""
        if not self.paused:
            self.paused = True
            self.pause_menu.show()
            self.paused = False
            self.dt = 0

    def spawn_powerup(self, x: int, y: int) -> None:
        """Spawns a power-up with a probability, allowing multiple to exist at once."""
        if len(self.powerups) < 3 and random.random() < .1:
            powerup_class = PowerUp.get_powerup_type()
            self.powerups.append(powerup_class(self, x, y))

    def check_for_clear_map(self) -> None:
        """Checks if all asteroids are destroyed and resets the map if so."""
        if not self.asteroids:
            self.level.increment_level()
            self.spawn_asteroids(5 + self.level.get_level() * 2)
            self.player.set_invincibility()

    def spawn_asteroids(self, count: int=5) -> None:
        """Spawn initial asteroids using weighted selection from asteroid types."""
        for _ in range(count):
            asteroid_type = Asteroid.get_asteroid_type()
            print(asteroid_type)
            self.asteroids.append(asteroid_type(self))
        logger.info("{count} asteroids spawned")

    def update_all(self, keys, dt: float) -> None:
        """Update all game objects, including power-ups, bullets, asteroids,
        and explosions, using delta time (dt)."""

        self.player.slowed_by_ice = False  # Reset ice slowdown before checking

        self._update_respawn(keys)
        self._update_bullets()
        self._update_asteroids()
        self._update_powerups()
        self.check_powerup_collisions()

        if self.player.explosion_timer > 0:
            self.player.update_explosion()

        for debris in self.debris:
            debris.update(dt)

        self.score_popups = [popup for popup in self.score_popups if popup.update()]
        self.debris = [d for d in self.debris if d.lifetime > 0]
        self.score.update_multiplier(dt)

    def _update_respawn(self, keys) -> None:
        """Handles player respawn countdown and resets the player when ready, using delta time."""

        if self.respawn_timer > 0:
            self.respawn_timer -= self.dt * 60
            print(f"Respawning in {max(0, int(self.respawn_timer))} frames")

            if self.respawn_timer <= 0:
                print("Respawning player now!")
                self.respawn_player()
        else:
            self.player.update(keys)

    def _update_bullets(self) -> None:
        """Updates bullets and removes expired ones using delta time."""
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.lifetime > self.dt * 60]

    def _update_asteroids(self) -> None:
        """Updates asteroids, handles explosion animations, and removes
        destroyed asteroids using delta time."""
        asteroids_to_remove = []

        for asteroid in self.asteroids:
            if isinstance(asteroid, ExplodingAsteroid) and asteroid.exploding:
                asteroid.update_explosion()
                if asteroid.explosion_timer <= 0:
                    asteroids_to_remove.append(asteroid)
            else:
                asteroid.update()

        # Remove exploding asteroids after animation finishes
        self.asteroids = [a for a in self.asteroids if a not in asteroids_to_remove]

    def _update_powerups(self) -> None:
        """Updates power-ups and removes expired ones using delta time."""
        for powerup in self.powerups:
            powerup.update()
        self.powerups = [p for p in self.powerups if not p.is_expired()]

    def handle_powerup_expiration(self, event: pygame.event.Event) -> None:
        """Handles expiration events for power-ups."""
        if event.type == pygame.USEREVENT + 5:
            self.asteroid_slowdown_active = False

    def _draw_bullets(self, screen: pygame.Surface) -> None:
        for bullet in self.bullets:
            bullet.draw(screen)

    def _draw_asteroids(self, screen: pygame.Surface) -> None:
        for asteroid in self.asteroids:
            asteroid.draw(screen)
            if isinstance(asteroid, ExplodingAsteroid) and asteroid.exploding:
                asteroid.draw_explosion(screen)

    def _draw_powerups(self, screen: pygame.Surface) -> None:
        for powerup in self.powerups:
            powerup.draw(screen)

    def _draw_player(self, screen: pygame.Surface) -> None:
        if self.player.explosion_timer > 0:
            self.player.draw_explosion(screen)
        else:
            self.player.draw(screen)

    def draw_all(self, screen: pygame.Surface) -> None:
        """Draw all game objects, including power-ups."""
        self._draw_player(screen)
        self._draw_asteroids(screen)
        self._draw_powerups(screen)
        self._draw_bullets(screen)
        self.life.draw(screen)
        self._draw_powerup_timer(screen)
        self.level.draw(screen)
        self.score.draw(screen)
        self._draw_debris(screen)
        self._draw_score_popups(screen)

        self._asteroid_slowdown_active(screen)

    def _draw_debris(self, screen: pygame.Surface) -> None:
        for debris in self.debris:
            debris.draw(screen)

    def _draw_score_popups(self, screen: pygame.Surface) -> None:
        for popup in self.score_popups:
            popup.draw(screen, self.font)

    def _asteroid_slowdown_active(self, screen: pygame.Surface) -> None:
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

    def check_powerup_collisions(self) -> None:
        """Checks if the player collects a power-up."""
        for powerup in self.powerups[:]:
            combined_size = powerup.radius + self.player.size
            if self.calculate_collision_distance(self.player, powerup) < combined_size:
                print(f"Player collected {powerup.__class__.__name__}!")  # Debug
                self.apply_powerup(powerup)  # Pass powerup instance
                self.powerups.remove(powerup)  # Remove after collection

    def apply_powerup(self, powerup: PowerUp) -> None:
        """Applies the collected power-up effect."""
        if isinstance(powerup, TemporalSlowdownPowerUp):
            self.slowdown_timer = pygame.time.get_ticks() + 5000  # 5 seconds
            self.asteroid_slowdown_active = True
            pygame.time.set_timer(pygame.USEREVENT + 5, 5000)
        else:
            powerup.apply(self.player)  # Call the power-up's apply() method

    def _handle_bullet_asteroid_collision(self) -> None:
        """Handles collisions between bullets and asteroids."""

        bullets_to_remove = []
        asteroids_to_remove = []
        new_asteroids = []

        for bullet in self.bullets[:]:  # Iterate over a copy
            for asteroid in self.asteroids[:]:  # Iterate over a copy
                if self._is_bullet_asteroid_collision(bullet, asteroid):
                    self._process_bullet_hit(
                        bullet, asteroid, bullets_to_remove,
                        asteroids_to_remove, new_asteroids
                    )

        self._remove_destroyed_asteroids(asteroids_to_remove)
        self.asteroids.extend(new_asteroids)  # Add newly split asteroids
        self.bullets = [b for b in self.bullets if b not in bullets_to_remove]

    def _is_bullet_asteroid_collision(
            self, bullet: Bullet, asteroid: Asteroid
        ) -> bool:
        """Returns True if a bullet collides with an asteroid."""
        return self.calculate_collision_distance(bullet, asteroid) < asteroid.size

    #pylint: disable=too-many-arguments
    def _process_bullet_hit(
            self, bullet: Bullet, asteroid: Asteroid,
            bullets_to_remove: List[Bullet],
            asteroids_to_remove: List[Asteroid], new_asteroids: List[Asteroid]
        ) -> None:
        """Handles the effects of a bullet hitting an asteroid."""

        self._apply_bullet_effects(bullet, asteroid)
        if isinstance(asteroid, ShieldAsteroid) and asteroid.current_shield > 0:
            asteroid.on_hit(bullet)  # Reduce shield health
            bullets_to_remove.append(bullet)  # Destroy bullet
            return  # Skip further processing (don't damage the asteroid)
        self._handle_asteroid_destruction(asteroid, asteroids_to_remove, new_asteroids)

        if not bullet.piercing:
            bullets_to_remove.append(bullet)

        self._handle_powerup_spawn(asteroid)
        self._handle_ricochet_bullet(bullet, asteroid)

    def _apply_bullet_effects(self, bullet: Bullet, asteroid: Asteroid):
        """Applies effects when a bullet hits an asteroid."""
        bullet.on_hit_asteroid(asteroid)
        self.score.update_score(asteroid)
        if asteroid.size >= 40:
            score_value = 100 * self.score.multiplier
        elif asteroid.size >= 20:
            score_value = 200 * self.score.multiplier
        else:
            score_value = 300 * self.score.multiplier
        self.score_popups.append(ScorePopup(asteroid.x, asteroid.y, score_value))  # Example score

    def _handle_asteroid_destruction(
            self, asteroid: Asteroid,
            asteroids_to_remove: List[Asteroid], new_asteroids: List[Asteroid]
        ):
        """Determines how an asteroid is destroyed or split."""
        if isinstance(asteroid, ExplodingAsteroid):
            self._handle_exploding_asteroid(asteroid, asteroids_to_remove, new_asteroids)
        else:
            asteroids_to_remove.append(asteroid)  # Remove normal asteroids
            new_asteroids.extend(asteroid.split())  # Add split asteroids

    def _handle_powerup_spawn(self, asteroid: Asteroid) -> None:
        """Spawns a power-up at the asteroid’s location if conditions are met."""
        self.spawn_powerup(asteroid.x, asteroid.y)

    def _handle_ricochet_bullet(
            self, bullet: Bullet, asteroid: Asteroid
        ) -> None:
        """Creates a ricochet bullet if the player has ricochet active."""
        if self.player.ricochet_active and not bullet.ricochet:
            self._spawn_ricochet_bullet(asteroid.x, asteroid.y)

    def _handle_exploding_asteroid(
            self, asteroid: Asteroid,
            asteroids_to_remove: List[Asteroid], new_asteroids: List[Asteroid]
        ) -> None:
        """Triggers an asteroid explosion and manages affected asteroids."""

        if not asteroid.exploding:  # Start explosion if not already started
            asteroid.explode(self.asteroids)

        exploded_asteroids = asteroid.explode(self.asteroids)
        for exploded_asteroid in exploded_asteroids:
            self.score.update_score(exploded_asteroid)
            asteroids_to_remove.append(exploded_asteroid)
            new_asteroids.extend(exploded_asteroid.split())

    def _spawn_ricochet_bullet(self, x: int, y: int) -> None:
        """Creates and adds a ricochet bullet."""
        new_angle = random.randint(0, 360)  # Random ricochet angle
        ricochet_bullet = Bullet(
            self, x, y, new_angle, ricochet=True,
            color=RicochetShotPowerUp.color, radius=14
        )
        self.bullets.append(ricochet_bullet)

    def _remove_destroyed_asteroids(self, asteroids_to_remove: List[Asteroid]) -> None:
        """Removes non-exploding asteroids that were destroyed."""
        self.asteroids = [
            a for a in self.asteroids
            if a not in asteroids_to_remove or (isinstance(a, ExplodingAsteroid) and a.exploding)
        ]

    def _handle_player_asteroid_collision(self) -> None:
        """Handles collisions between the player and asteroids, triggering the
        explosion before respawn."""
        if self.respawn_timer > 0:
            return  # Player is currently respawning, ignore collisions
        for asteroid in self.asteroids:
            if self._is_collision(self.player, asteroid):
                self._trigger_player_explosion()
                break  # Stop checking after first collision

    def _is_collision(self, entity1, entity2):
        """Returns True if two entities are colliding based on their distance."""
        return self.calculate_collision_distance(entity1, entity2) < entity2.size

    def _trigger_player_explosion(self) -> None:
        """Handles the player explosion animation and sets up respawn or game over."""
        if self.player.invincible:
            return  # Skip if player is currently invincible
        if self.player.shield_active:
            self.player.take_damage()
            return  # Shield absorbs the hit
        self.player.generate_explosion()  # Trigger explosion animation
        self.respawn_timer = 30  # Delay respawn for explosion duration
        self.life.decrement()

    def check_for_collisions(self) -> None:
        """Check for bullet-asteroid and player-asteroid collisions."""
        self._handle_bullet_asteroid_collision()
        self._handle_player_asteroid_collision()

    def handle_player_collision(self, screen: pygame.Surface) -> None:
        """Handles player collision logic, including shield effects,
        death animation, and respawn/game over."""
        if self._player_is_invincible():
            return
        if self._player_has_shield():
            return
        self._process_player_death(screen)

    def _player_is_invincible(self) -> bool:
        """Checks if the player is invincible after respawn."""
        return self.player.invincible

    def _player_has_shield(self) -> bool:
        """Checks if the player has an active shield and applies damage if so."""
        if self.player.shield_active:
            self.player.take_damage()
            return True
        return False

    def _process_player_death(self, screen: pygame.Surface) -> None:
        """Handles player death animation, life count, and respawn or game over."""
        self.player.death_animation(screen)  # Play death effect
        self.life.decrement()
        if self.life.get_lives() > 0:
            self.respawn_player()

    def respawn_player(self) -> None:
        """Respawns the player at the center after the timer expires."""
        if self.respawn_timer > 0:
            return
        logger.info("Respawning player!")
        self.player.reset_position()
        self.player.invincible = True
        pygame.time.set_timer(pygame.USEREVENT + 2, 2000)  # 2 sec invincibility

    def _draw_powerup_timer(self, screen: pygame.Surface) -> None:
        """Draws a shrinking timer bar for active powerups with their
        corresponding colors and labels."""
        y_offset = {"minimum": 75, "medium": 85, "maximum": 100}.get(
            self.settings.get("pixelation"), 85
        )

        if self.player.powerup_timer <= 0:
            return

        # Map each flag to its corresponding class and label
        powerup_mappings = [
            (self.player.trishot_active, TrishotPowerUp, "Trishot"),
            (self.player.quadshot_active, QuadShotPowerUp, "Quadshot"),
            (self.player.ricochet_active, RicochetShotPowerUp, "Ricochet"),
            (self.player.invincible, InvincibilityPowerUp, "Invincibility")
        ]

        for is_active, powerup_class, label in powerup_mappings:
            if is_active:
                color = getattr(powerup_class, "color", (0, 255, 255))  # Fallback: cyan
                bar_width = int((self.player.powerup_timer / 300) * 200)

                # Draw timer bar
                pygame.draw.rect(
                    screen, color, (config.WIDTH // 2 - 100, config.HEIGHT - 30, bar_width, 10)
                )

                # Draw power-up name
                text_surface = self.font.render(label, True, (255, 255, 255))
                text_rect = text_surface.get_rect(
                    center=(config.WIDTH // 2, config.HEIGHT - y_offset)
                )
                screen.blit(text_surface, text_rect)
                break


    def calculate_collision_distance(self, obj1, obj2) -> None:
        """Calculates Euclidean distance between two game objects."""
        dx = obj1.x - obj2.x
        dy = obj1.y - obj2.y
        return (dx ** 2 + dy ** 2) ** 0.5
