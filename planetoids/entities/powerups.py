import random
import time
import math

import pygame

from planetoids.core.config import config
from planetoids.core.logger import logger
from planetoids.core.settings import get_font_path

class PowerUp:
    """Base class for all power-ups."""
    subclasses = []

    def __init__(self, game_state, x, y, radius=20):
        """Initialize power-up properties."""
        self.game_state = game_state
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = random.uniform(-1.5, 1.5)
        self.speed_y = random.uniform(-1.5, 1.5)
        self.spawn_time = time.time()  # Store the spawn time

        logger.info(f"Spawned {repr(self)}")

        self.particles = [{"x": self.x, "y": self.y, "vx": random.uniform(-0.5, 0.5), "vy": random.uniform(-0.5, 0.5)}
                  for _ in range(6)]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PowerUp.subclasses.append(cls)  # Register each subclass

    @classmethod
    def get_powerup_type(cls):
        """Selects an asteroid type based on weighted probabilities"""
        powerup_classes = cls.subclasses
        weights = [subclass.spawn_chance for subclass in powerup_classes]
        powerup_type = random.choices(powerup_classes, weights=weights, k=1)[0]
        logger.info(f"Randomly selected powerup type {powerup_type}")
        return powerup_type

    @classmethod
    def get_powerups(cls):
        return cls.subclasses

    def update(self):
        """Move the power-up using delta time scaling and handle expiration."""
        self.x += self.speed_x * self.game_state.dt * 60  # ✅ Scale movement by dt
        self.y += self.speed_y * self.game_state.dt * 60

        self.x %= config.WIDTH
        self.y %= config.HEIGHT

        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vx"] += random.uniform(-0.05, 0.05)
            p["vy"] += random.uniform(-0.05, 0.05)

    def draw(self, screen):
        """Draw the power-up with a blinking effect before expiration."""

        if self._should_skip_drawing():
            return  # Do not draw expired or blinking power-ups

        self._draw_glow(screen)
        self._draw_main_powerup(screen)
        self._draw_powerup_symbol(screen)

        for p in self.particles:
            pygame.draw.circle(screen, getattr(self, "color", config.CYAN), (int(p["x"]), int(p["y"])), 2)

    def _should_skip_drawing(self):
        """Determines if the power-up should be skipped for blinking or expiration."""
        if self.is_expired():
            return True

        elapsed_time = time.time() - self.spawn_time
        return elapsed_time > 10 and int(elapsed_time * 5) % 2 == 0  # Blinks after 10s
        return False  # Always draw, just with varying transparency

    def _draw_glow(self, screen):
        """Draws animated tendrils of energy around the power-up."""
        glow_surface = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        
        pulse = 2 + (math.sin(pygame.time.get_ticks() * 0.005) * 2)  # Subtle pulsing
        center = (self.radius * 2, self.radius * 2)
        
        for _ in range(5):  
            if random.random() < 0.7: 
                angle = random.uniform(0, math.tau)
                length = random.uniform(self.radius, self.radius * 2.5)
                end_x = center[0] + math.cos(angle) * length
                end_y = center[1] + math.sin(angle) * length
                
                color = (*getattr(self, "color", config.CYAN), random.randint(50, 180))
                pygame.draw.line(glow_surface, color, center, (end_x, end_y), random.randint(1, 3)) 
                for i in range(4):
                    alpha = max(0, 150 - (i * 40))
                    pygame.draw.circle(glow_surface, (*getattr(self, "color", config.CYAN), alpha), center, int(self.radius + pulse + (i * 2)))

        screen.blit(glow_surface, (self.x - self.radius * 2, self.y - self.radius * 2), special_flags=pygame.BLEND_ADD)

    def _draw_main_powerup(self, screen):
        """Draws the main body of the power-up."""
        pygame.draw.circle(screen, getattr(self, "color", config.CYAN), (int(self.x), int(self.y)), self.radius)

    def _draw_powerup_symbol(self, screen):
        """Draws the symbol or letter representing the power-up."""
        font = pygame.font.Font(get_font_path(), 32)
        text = font.render(self.get_symbol(), True, (0, 0, 0))
        screen.blit(text, (self.x-6, self.y-14))

    def is_expired(self):
        """Check if the power-up should disappear."""
        return time.time() - self.spawn_time > 15  # Disappear after 10 seconds

    def __repr__(self):
        return f"{self.__class__.__name__}(x={round(self.x)}, y={round(self.y)}, radius={self.radius})"

class TrishotPowerUp(PowerUp):
    """Trishot power-up that enables triple bullets for a limited time."""
    spawn_chance = 1.0
    color = (255, 165, 0)  # Orange

    def __init__(self, game_state, x, y):
        """Initialize the trishot power-up."""
        super().__init__(game_state, x, y)

    def apply(self, player):
        """Grants the player trishot mode."""
        player.enable_trishot()

    def get_symbol(self):
        """Display 'T' inside the power-up."""
        return "T"

class ShieldPowerUp(PowerUp):
    """Shield power-up that reenables player's shield"""
    spawn_chance = 1.0
    color = (0, 255, 255)  # Cyan

    def __init__(self, game_state, x, y):
        """Initialize the shield power-up."""
        super().__init__(game_state, x, y)

    def apply(self, player):
        """Grants the player shield."""
        player.activate_shield()

    def get_symbol(self):
        """Display 'S' inside the power-up."""
        return "S"

class QuadShotPowerUp(PowerUp):
    """QuadShot power-up that enables four-directional bullets for a limited time."""
    spawn_chance = 1.0
    color = (255, 0, 255) 

    def apply(self, player):
        """Grants the player QuadShot mode."""
        player.enable_quadshot()

    def get_symbol(self):
        return "Q"

class RicochetShotPowerUp(PowerUp):
    """Ricochet Shot power-up that makes bullets bounce off asteroids once."""
    spawn_chance = 1.0
    color = (0, 255, 0)

    def apply(self, player):
        """Grants the player Ricochet mode."""
        player.enable_ricochet()

    def get_symbol(self):
        return "R"

class InvincibilityPowerUp(PowerUp):
    """Invincibility powerup"""
    spawn_chance = 1.0
    color = (255, 255, 0)

    def apply(self, player):
        """Grants the player Invincibility mode."""
        player.enable_invincibility()

    def get_symbol(self):
        return "I"

class TemporalSlowdownPowerUp(PowerUp):
    """Slows all asteroids dramatically for a few seconds."""
    spawn_chance = 1.0
    color = (135, 206, 250)

    def apply(self, game_state):
        """Activates slow-motion effect on all asteroids."""
        game_state.asteroid_slowdown_active = True
        pygame.time.set_timer(pygame.USEREVENT + 5, 5000)  # Slowdown lasts 5 seconds

    def get_symbol(self):
        return "Δ"
