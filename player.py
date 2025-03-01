import pygame
import math
import random
from config import WIDTH, HEIGHT, WHITE, ORANGE, CYAN
from particle import Particle  # Import the new particle class
from bullet import Bullet
import time

class Player:
    def __init__(self):
        """Initialize player with movement settings."""
        self.reset_position()
        self.acceleration = 0.1
        self.max_speed = 5
        self.size = 20  # Ship size
        self.thrusting = False
        self.particles = []  # Stores exhaust particles
        self.set_invincibility()
        self.trishot_active = False
        self.quadshot_active = False
        self.ricochet_active = False
        self.ricochet_piercing = False
        self.powerup_timer = 0

        # Shield system
        self.activate_shield()

    def activate_shield(self):
        """Activates the shield for a limited time."""
        self.shield_active = True
        self.shield_cooldown = 0
        self.last_shield_recharge = time.time()  # Track recharge time

    def shoot(self):
        """Shoots bullets. If QuadShot is active, fires in 4 directions."""
        bullets = []

        if self.quadshot_active:
            angles = [self.angle, self.angle + 90, self.angle + 180, self.angle + 270]  # QuadShot based on player angle
        elif self.trishot_active:
            angles = [self.angle - 15, self.angle, self.angle + 15]  # Trishot spread
        else:
            angles = [self.angle]  # Normal shot

        for angle in angles:
            bullets.append(Bullet(self.x, self.y, angle))

        return bullets

    def _disable_previous_shots(self):
        self.trishot_active = False
        self.quadshot_active = False
        self.ricochet_active = False
        self.ricochet_piercing = False

    def enable_invincibility(self):
        """Activates quadshot mode for a limited time."""
        self._disable_previous_shots()
        self.set_invincibility(timer=300)
        self.powerup_timer = 300

    def enable_ricochet(self):
        """Activates quadshot mode for a limited time."""
        self._disable_previous_shots()
        self.ricochet_active = True
        self.ricochet_piercing = True
        self.powerup_timer = 300

    def enable_quadshot(self):
        """Activates quadshot mode for a limited time."""
        self._disable_previous_shots()
        self.quadshot_active = True
        self.powerup_timer = 300

    def enable_trishot(self):
        """Activates trishot mode for a limited time."""
        self._disable_previous_shots()
        self.trishot_active = True
        self.powerup_timer = 300

    def reset_position(self):
        """Resets player position, stops movement, and enables brief invincibility."""
        print("Resetting player position")  # Debugging
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.thrusting = False  # Reset thrust effect
        self.trishot_active = False
        self.activate_shield()
        self.set_invincibility()

    def set_invincibility(self, timer=120):
        """Set the player as invincible"""
        self.invincible = True
        self.invincibility_timer = timer  # 2 seconds of invincibility

    def _draw_shield_bar(self, screen):
        """Draws a shield recharge bar in the top-left corner."""
        bar_width = 120
        bar_height = 12
        bar_x, bar_y = 10, 40  # Position on screen

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
        """Handles movement, rotation, and particle effects."""
        self._handle_shield_regeneration()

        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer == 0:
                self._disable_previous_shots()

        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1
            if self.invincibility_timer == 0:
                self.invincible = False  # Invincibility expires

        self.thrusting = False  # Reset thrust effect

        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5
        if keys[pygame.K_UP]:  # Apply thrust
            self.thrusting = True
            angle_rad = math.radians(self.angle)
            self.velocity_x += math.cos(angle_rad) * self.acceleration
            self.velocity_y -= math.sin(angle_rad) * self.acceleration

            # Limit speed
            speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            if speed > self.max_speed:
                factor = self.max_speed / speed
                self.velocity_x *= factor
                self.velocity_y *= factor

            # Generate exhaust particles
            self._generate_exhaust()

        # Apply movement
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Screen wraparound
        self.x %= WIDTH
        self.y %= HEIGHT

        # Update and remove expired particles
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()

    def _handle_shield_regeneration(self):
        """Regenerates shield every 30 seconds if broken."""
        if not self.shield_active:
            time_since_break = time.time() - self.last_shield_recharge
            if time_since_break >= 30:  # 30 seconds cooldown
                self.shield_active = True  # Shield is restored
                print("Shield recharged!")

    def take_damage(self):
        """Handles damage logic: shield breaks first, then invincibility, then death."""
        if self.shield_active and not self.invincible:
            self.shield_active = False  # Break the shield
            self.last_shield_recharge = time.time()  # Start recharge timer
            self.set_invincibility()  # Trigger 2 seconds of invincibility
            print("⚠️ Shield broken! Player is now invincible for 2 seconds.")

    def draw(self, screen):
        """Draws the player ship and particles."""
        angle_rad = math.radians(self.angle)

        # Triangle points relative to the center
        front = (self.x + math.cos(angle_rad) * self.size, self.y - math.sin(angle_rad) * self.size)
        left = (self.x + math.cos(angle_rad + 2.5) * self.size * 0.6, self.y - math.sin(angle_rad + 2.5) * self.size * 0.6)
        right = (self.x + math.cos(angle_rad - 2.5) * self.size * 0.6, self.y - math.sin(angle_rad - 2.5) * self.size * 0.6)

        # Draw particles first (so they appear behind the ship)
        for particle in self.particles:
            particle.draw(screen)

        # Draw player (blink effect when invincible)
        if not self.invincible or (self.invincibility_timer % 10 < 5):  # Blink effect
            pygame.draw.polygon(screen, WHITE, [front, left, right], 1)

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
                pygame.draw.circle(screen, (100, 100, 255), (int(self.x + offset_x), int(self.y + offset_y)), 3)

    def _generate_exhaust(self):
        """Adds new particles behind the ship."""
        angle_rad = math.radians(self.angle)
        exhaust_x = self.x - math.cos(angle_rad) * self.size * 1.2
        exhaust_y = self.y + math.sin(angle_rad) * self.size * 1.2
        self.particles.append(Particle(exhaust_x, exhaust_y, self.angle, random.uniform(1, 3)))

    def _draw_thruster(self, screen, angle_rad, left, right):
        """Draws a flickering thrust effect behind the ship."""
        flicker_size = random.uniform(self.size * 0.4, self.size * 0.6)
        thruster_tip = (
            self.x - math.cos(angle_rad) * flicker_size * 2,
            self.y + math.sin(angle_rad) * flicker_size * 2
        )
        pygame.draw.polygon(screen, ORANGE, [thruster_tip, left, right])

    def death_animation(self, screen):
        """Plays a shattering effect when the player dies."""
        explosion_particles = []  # Temporary explosion effect
        fragments = []  # Pieces of the ship

        angle_rad = math.radians(self.angle)

        # Define original triangle points
        front = (self.x + math.cos(angle_rad) * self.size, self.y - math.sin(angle_rad) * self.size)
        left = (self.x + math.cos(angle_rad + 2.5) * self.size * 0.6, self.y - math.sin(angle_rad + 2.5) * self.size * 0.6)
        right = (self.x + math.cos(angle_rad - 2.5) * self.size * 0.6, self.y - math.sin(angle_rad - 2.5) * self.size * 0.6)

        # Split into 3 moving fragments
        fragments.append({"pos": front, "vel": (random.uniform(-2, 2), random.uniform(-2, 2))})
        fragments.append({"pos": left, "vel": (random.uniform(-2, 2), random.uniform(-2, 2))})
        fragments.append({"pos": right, "vel": (random.uniform(-2, 2), random.uniform(-2, 2))})

        # Generate explosion particles
        for _ in range(15):
            explosion_particles.append(Particle(self.x, self.y, random.uniform(0, 360), random.uniform(1, 3)))

        # Animation loop
        for _ in range(30):  # Roughly half a second of animation
            screen.fill((0, 0, 0))  # Clear screen

            # Draw ship fragments
            for fragment in fragments:
                fragment["pos"] = (fragment["pos"][0] + fragment["vel"][0], fragment["pos"][1] + fragment["vel"][1])
                pygame.draw.polygon(screen, WHITE, [fragment["pos"], fragment["pos"], fragment["pos"]], 1)

            # Draw explosion particles
            for particle in explosion_particles:
                particle.update()
                particle.draw(screen)

            pygame.display.flip()
            pygame.time.delay(15)  # Small delay for smooth animation
