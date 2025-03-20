import math
import random
import time

import pygame

from planetoids.core.config import config
from planetoids.entities.particle import Particle  # Import the new particle class
from planetoids.entities.bullet import Bullet
from planetoids.core.logger import logger
from planetoids.entities.powerups import RicochetShotPowerUp, TrishotPowerUp, QuadShotPowerUp

class Player:
    def __init__(self, settings, game_state):
        """Initialize player with movement settings."""
        self.settings = settings
        self.game_state = game_state
        self.reset_position()
        self.acceleration = 0.1
        self.max_speed = 5
        self.size = 30  # Ship size
        self.thrusting = False
        self.particles = []  # Stores exhaust particles
        self.set_invincibility()
        self.trishot_active = False
        self.quadshot_active = False
        self.ricochet_active = False
        self.ricochet_piercing = False
        self.powerup_timer = 0
        self.active_powerup_color = None  # Store the color of the active power-up
        self.explosion_particles = []  # Temporary explosion effect
        self.fragments = []  # Pieces of the ship
        self.explosion_timer = 30

        # Shield system
        self.activate_shield()

        logger.info(f"Spawned player")

    def activate_shield(self):
        """Activates the shield for a limited time."""
        self.shield_active = True
        self.shield_cooldown = 0
        self.last_shield_recharge = time.time()  # Track recharge time
        logger.info(f"Shield activated")

    def shoot(self):
        """Shoots bullets. If QuadShot is active, fires in 4 directions."""
        bullets = []

        if self.quadshot_active:
            angles = [self.angle, self.angle + 90, self.angle + 180, self.angle + 270]  # QuadShot based on player angle
            color = QuadShotPowerUp.color
            radius = 7
        elif self.trishot_active:
            angles = [self.angle - 15, self.angle, self.angle + 15]  # Trishot spread
            color = TrishotPowerUp.color
            radius = 7
        elif self.ricochet_active:
            color = RicochetShotPowerUp.color
            angles = [self.angle]
            radius = 14
        else:
            color = config.RED
            angles = [self.angle]  # Normal shot
            radius = 7
        for angle in angles:
            bullets.append(Bullet(self.game_state, self.x, self.y, angle, color=color, radius=radius))

        return bullets

    def _disable_previous_shots(self):
        self.trishot_active = False
        self.quadshot_active = False
        self.ricochet_active = False
        self.ricochet_piercing = False
        logger.info("Previous shots disabled")

    def enable_invincibility(self):
        """Activates quadshot mode for a limited time."""
        self._disable_previous_shots()
        self.set_invincibility(timer=300)
        self.powerup_timer = 300
        logger.info(f"Invincibility enabled")

    def enable_ricochet(self):
        """Activates ricochet shot mode for a limited time."""
        self._disable_previous_shots()
        self.ricochet_active = True
        self.ricochet_piercing = True
        self.powerup_timer = 300
        self.active_powerup_color = RicochetShotPowerUp.color  # Ricochet Shot Aura
        self.powerup_aura_timer = 300
        logger.info("Ricochet enabled")

    def enable_quadshot(self):
        """Activates quadshot mode for a limited time."""
        self._disable_previous_shots()
        self.quadshot_active = True
        self.powerup_timer = 300
        self.active_powerup_color = QuadShotPowerUp.color  # Quadshot Aura
        self.powerup_aura_timer = 300
        logger.info("Quadshot enabled")

    def enable_trishot(self):
        """Activates trishot mode for a limited time."""
        self._disable_previous_shots()
        self.trishot_active = True
        self.powerup_timer = 300
        self.active_powerup_color = TrishotPowerUp.color  # Trishot Aura
        self.powerup_aura_timer = 300
        logger.info("Trishot enabled")

    def reset_position(self):
        """Resets player position, stops movement, and enables brief invincibility."""
        print("Resetting player position")  # Debugging
        self.x = config.WIDTH // 2
        self.y = config.HEIGHT // 2
        self.angle = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.base_velocity_x = 0
        self.base_velocity_y = 0
        self.thrusting = False  # Reset thrust effect
        self.trishot_active = False
        self.activate_shield()
        self.set_invincibility()
        logger.info(f"Position reset to ({self.x}, {self.y})")

    def set_invincibility(self, timer=120):
        """Set the player as invincible"""
        self.invincible = True
        self.invincibility_timer = timer  # 2 seconds of invincibility
        logger.info(f"Set invincibility")

    def _draw_shield_bar(self, screen):
        """Draws a shield recharge bar in the top-left corner."""
        bar_width = 120
        bar_height = 12
        bar_x = 10
        bar_y = {"minimum": 40, "medium": 60, "maximum": 80}.get(self.settings.get("pixelation"), 40)  # Position on screen

        # Calculate recharge progress (0 to 1)
        if self.shield_active:
            progress = 1.0  # Full shield
        else:
            time_since_break = time.time() - self.last_shield_recharge
            progress = min(time_since_break / 30, 1.0)  # Fill over 30 seconds

        # Bar colors
        border_color = (200, 200, 200)  # Light grey border
        empty_color = (80, 80, 80)  # Dark grey when empty
        fill_color = (0, 255, 255) if self.shield_active else (100, 100, 255)  # Cyan when full, blue when recharging

        # Draw border
        pygame.draw.rect(screen, border_color, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4), 2)

        # Draw empty bar
        pygame.draw.rect(screen, empty_color, (bar_x, bar_y, bar_width, bar_height))

        # Draw progress fill
        pygame.draw.rect(screen, fill_color, (bar_x, bar_y, bar_width * progress, bar_height))

    def update(self, keys):
        """Handles movement, rotation, and particle effects in a momentum-based system using delta time."""

        self._handle_shield_regeneration()

        if self.powerup_timer > 0:
            self.powerup_timer -= self.game_state.dt * 60
            if self.powerup_timer <= 0:
                self._disable_previous_shots()

        if self.invincibility_timer > 0:
            self.invincibility_timer -= self.game_state.dt * 60
            if self.invincibility_timer <= 0:
                self.invincible = False

        self.thrusting = False  # Reset thrust effect

        rotation_speed = 250  # Degrees per second
        if keys[pygame.K_LEFT]:
            self.angle += rotation_speed * self.game_state.dt
        if keys[pygame.K_RIGHT]:
            self.angle -= rotation_speed * self.game_state.dt

        if keys[pygame.K_UP]:
            self.thrusting = True
            angle_rad = math.radians(self.angle)

            self.velocity_x += math.cos(angle_rad) * self.acceleration * self.game_state.dt * 60
            self.velocity_y -= math.sin(angle_rad) * self.acceleration * self.game_state.dt * 60

            self._generate_exhaust()

        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.velocity_x *= scale
            self.velocity_y *= scale

        if not getattr(self, "slowed_by_ice", False):  # Ensure slowdown doesn't overwrite true base speed
            self.base_velocity_x = self.velocity_x
            self.base_velocity_y = self.velocity_y

        self.x += self.velocity_x * self.game_state.dt * 60
        self.y += self.velocity_y * self.game_state.dt * 60

        self.x %= config.WIDTH
        self.y %= config.HEIGHT

        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()

    def draw_aura(self, screen):
        """Draws a soft, pulsating aura around the player when a power-up is active."""
        if self.powerup_aura_timer > 0:
            pulse_factor = 1 + 0.1 * math.sin(pygame.time.get_ticks() * 0.01)  # Smooth pulsation
            aura_radius = int(50 * pulse_factor)  # Adjust size dynamically
            alpha = int(100 + 40 * pulse_factor)  # Opacity range: 100 - 140

            aura_surface = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
            aura_surface.fill((0, 0, 0, 0))  # Transparent background

            if self.active_powerup_color:
                aura_color = (*self.active_powerup_color[:3], alpha)  # Apply pulsating transparency
                pygame.draw.circle(aura_surface, aura_color, (aura_radius, aura_radius), aura_radius)

            screen.blit(aura_surface, (self.x - aura_radius, self.y - aura_radius))

    def _handle_shield_regeneration(self):
        """Regenerates shield every 30 seconds if broken."""
        if not self.shield_active:
            time_since_break = time.time() - self.last_shield_recharge
            if time_since_break >= 30:  # 30 seconds cooldown
                self.shield_active = True  # Shield is restored
                logger.info(f"Shield recharged")

    def take_damage(self):
        """Handles damage logic: shield breaks first, then invincibility, then death."""
        if self.shield_active and not self.invincible:
            self.shield_active = False  # Break the shield
            self.last_shield_recharge = time.time()  # Start recharge timer
            self.set_invincibility()  # Trigger 2 seconds of invincibility
            logger.info(f"Shield broken")

    def draw(self, screen):
        """Draws the player ship and particles."""
        angle_rad = math.radians(self.angle)

        if self.powerup_timer > 0 and self.active_powerup_color:
            if (self.trishot_active or self.quadshot_active or self.ricochet_active):
            # Aura effect: Expanding and fading glow
                self.draw_aura(screen)

        # Triangle points relative to the center
        front = (self.x + math.cos(angle_rad) * self.size, self.y - math.sin(angle_rad) * self.size)
        left = (self.x + math.cos(angle_rad + 2.5) * self.size * 0.6, self.y - math.sin(angle_rad + 2.5) * self.size * 0.6)
        right = (self.x + math.cos(angle_rad - 2.5) * self.size * 0.6, self.y - math.sin(angle_rad - 2.5) * self.size * 0.6)

        # Draw particles first (so they appear behind the ship)
        for particle in self.particles:
            particle.draw(screen)

        # Draw player (blink effect when invincible)
        if not self.invincible or (self.invincibility_timer % 10 < 5):  # Blink effect
            pygame.draw.polygon(screen, config.WHITE, [front, left, right], 4)

        # Draw thruster effect if accelerating
        if self.thrusting:
            self._draw_thruster(screen, angle_rad, left, right)
        if self.shield_active:
            self._draw_shield(screen)
        self._draw_shield_bar(screen)

    def _draw_shield(self, screen):
        """Draws a glowing shield around the player with a pulsing effect."""
        pulse_intensity = int(50 + 30 * abs(math.sin(time.time() * 2)))  # Pulses over time
        shield_color = (0, 255, 255, pulse_intensity)  # Cyan with alpha

        pygame.draw.circle(screen, shield_color, (int(self.x), int(self.y)), self.size + 5, 2)

        # When shield is broken, show a "shatter" effect
        if not self.shield_active:
            for _ in range(5):  # 5 pieces flying out
                offset_x = random.randint(-10, 10)
                offset_y = random.randint(-10, 10)
                pygame.draw.circle(screen, (100, 100, 255), (int(self.x + offset_x), int(self.y + offset_y)), 4)

    def _generate_exhaust(self):
        """Adds new particles behind the ship."""
        angle_rad = math.radians(self.angle)
        exhaust_x = self.x - math.cos(angle_rad) * self.size * 1.2
        exhaust_y = self.y + math.sin(angle_rad) * self.size * 1.2
        self.particles.append(Particle(exhaust_x, exhaust_y, self.angle, random.uniform(1, 3), self.game_state))

    def _draw_thruster(self, screen, angle_rad, left, right):
        """Draws a flickering thrust effect behind the ship."""
        flicker_size = random.uniform(self.size * 0.4, self.size * 0.6)
        thruster_tip = (
            self.x - math.cos(angle_rad) * flicker_size * 2,
            self.y + math.sin(angle_rad) * flicker_size * 2
        )
        pygame.draw.polygon(screen, config.ORANGE, [thruster_tip, left, right])

    def _generate_explosion(self):
        """Initializes the explosion effect when the player dies."""
        self.explosion_particles = []  # Temporary explosion effect
        self.fragments = []  # Pieces of the ship
        self.explosion_timer = 30  # Lasts for 30 frames (half a second)

        angle_rad = math.radians(self.angle)

        # Define original ship triangle points
        front = (self.x + math.cos(angle_rad) * self.size, self.y - math.sin(angle_rad) * self.size)
        left = (self.x + math.cos(angle_rad + 2.5) * self.size * 0.6, self.y - math.sin(angle_rad + 2.5) * self.size * 0.6)
        right = (self.x + math.cos(angle_rad - 2.5) * self.size * 0.6, self.y - math.sin(angle_rad - 2.5) * self.size * 0.6)

        # Create moving fragments
        self.fragments.append({"pos": front, "vel": (random.uniform(-2, 2), random.uniform(-2, 2))})
        self.fragments.append({"pos": left, "vel": (random.uniform(-2, 2), random.uniform(-2, 2))})
        self.fragments.append({"pos": right, "vel": (random.uniform(-2, 2), random.uniform(-2, 2))})

        # Generate explosion particles
        for _ in range(15):
            self.explosion_particles.append(
                Particle(
                    self.x,
                    self.y,
                    random.uniform(0, 360),
                    random.uniform(1, 3),
                    self.game_state
                )
            )

        logger.info("Player explosion generated")

    def _update_explosion(self):
        """Updates explosion animation frame by frame using delta time."""
        if self.explosion_timer > 0:
            self.explosion_timer -= self.game_state.dt * 60

            self._update_fragments(self.fragments)
            self._update_particles(self.explosion_particles)

            if self.explosion_timer <= 0:
                self._clear_explosion()
        else:
            self._clear_explosion()

    def _clear_explosion(self):
        """Clear explosion effects"""
        # Animation is done, clear effects
        self.explosion_particles = []
        self.fragments = []
        logger.info(f"Clear player explosion animation")

    def _update_particles(self, explosion_particles):
        """Update the explosion particles using delta time scaling."""
        for particle in explosion_particles:
            particle.update()

    def _update_fragments(self, fragments):
        """Update the fragment particles using delta time scaling."""
        for fragment in fragments:
            fragment["pos"] = (
                fragment["pos"][0] + fragment["vel"][0] * self.game_state.dt * 60,
                fragment["pos"][1] + fragment["vel"][1] * self.game_state.dt * 60
            )

    def _draw_explosion(self, screen):
        """Draws the explosion effect and ship fragments."""
        if self.explosion_timer > 0:
            for fragment in self.fragments:
                pygame.draw.polygon(screen, config.WHITE, [fragment["pos"], fragment["pos"], fragment["pos"]], 4)
            for particle in self.explosion_particles:
                particle.draw(screen)
