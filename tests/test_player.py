import math

import pytest
import pygame
from unittest.mock import patch

from planetoids.entities.player import Player
from planetoids.core.settings import Settings
from planetoids.entities.bullet import Bullet
from planetoids.core.config import WIDTH, HEIGHT

@pytest.fixture
def player():
    """Fixture to create a fresh player instance before each test."""
    pygame.init()  # Initialize pygame to avoid errors
    settings = Settings()
    return Player(settings)


def simulate_key_presses(player, keys, frames=1):
    """
    Simulates updating the game for a given number of frames with specific key presses.

    Args:
        player (Player): The player instance to update.
        keys (list[int]): A list of Pygame key constants to simulate as being pressed.
        frames (int): Number of frames (updates) to simulate.
    """
    key_states = [0] * 512  # Pygame has 512 possible scancodes
    for key in keys:
        key_states[key] = 1  # Mark specified keys as "pressed"

    with patch("pygame.key.get_pressed") as mock_get_pressed:
        mock_get_pressed.return_value = pygame.key.ScancodeWrapper(key_states)

        for _ in range(frames):
            player.update(pygame.key.get_pressed())  # Update with mocked key input

def test_player_initialization(player):
    """Test if the player initializes with the correct default values."""
    assert player.x == WIDTH // 2  # Assuming WIDTH // 2 = 400
    assert player.y == HEIGHT // 2  # Assuming HEIGHT // 2 = 300
    assert player.velocity_x == 0
    assert player.velocity_y == 0
    assert player.invincible is True
    assert player.invincibility_timer == 120
    assert player.shield_active is True

def test_player_shooting(player):
    """Test that shooting generates the correct number of bullets."""
    player.angle = 0  # Facing right
    bullets = player.shoot()
    assert isinstance(bullets, list)
    assert all(isinstance(b, Bullet) for b in bullets)
    assert len(bullets) == 1  # Default shooting fires 1 bullet

    # Test Trishot
    player.enable_trishot()
    bullets = player.shoot()
    assert len(bullets) == 3  # Trishot should fire 3 bullets

    # Test Quadshot
    player.enable_quadshot()
    bullets = player.shoot()
    assert len(bullets) == 4  # Quadshot should fire 4 bullets

def test_player_movement(player):
    """Test movement mechanics with acceleration and speed limiting."""
    keys = {pygame.K_UP: True, pygame.K_LEFT: False, pygame.K_RIGHT: False}
    initial_x, initial_y = player.x, player.y

    player.update(keys)

    assert player.thrusting is True
    assert player.velocity_x != 0 or player.velocity_y != 0  # Should have some movement
    assert math.sqrt(player.velocity_x**2 + player.velocity_y**2) <= player.max_speed  # Speed cap
    assert player.x != initial_x or player.y != initial_y  # Position should change

def test_player_invincibility(player):
    """Test that invincibility timer decreases and disables correctly."""

    # Mock pygame.key.get_pressed() to return a ScancodeWrapper-like object
    with patch("pygame.key.get_pressed") as mock_get_pressed:
        # Simulate no keys pressed
        mock_get_pressed.return_value = pygame.key.ScancodeWrapper([0] * 512)

        player.invincibility_timer = 10  # Short timer
        player.update(pygame.key.get_pressed())  # Pass mocked input
        assert player.invincibility_timer == 9  # Timer should decrement
        assert player.invincible is True  # Still invincible

        for _ in range(10):
            player.update(pygame.key.get_pressed())  # Pass mocked input

        assert player.invincibility_timer == 0
        assert player.invincible is False  # Should be disabled

def test_shield_break_and_recharge(player):
    """Test that the shield breaks and recharges after time."""

    with patch("pygame.key.get_pressed") as mock_get_pressed:
        # Simulate no keys pressed
        mock_get_pressed.return_value = pygame.key.ScancodeWrapper([0] * 512)

        for _ in range(120):
            player.update(pygame.key.get_pressed())  # Pass mocked input

    player.take_damage()
    assert player.shield_active is False  # Shield should break
    assert player.invincible is True  # Invincibility triggered

    player._handle_shield_regeneration()
    assert player.shield_active is False  # Should not regenerate immediately

    # Simulate waiting 30 seconds
    player.last_shield_recharge -= 30
    player._handle_shield_regeneration()
    assert player.shield_active is True  # Shield should be restored

def test_enable_powerups(player):
    """Test enabling different powerups and their effects."""
    player.enable_quadshot()
    assert player.quadshot_active is True
    assert player.trishot_active is False  # Other powerups should be disabled

    player.enable_trishot()
    assert player.trishot_active is True
    assert player.quadshot_active is False

    player.enable_ricochet()
    assert player.ricochet_active is True
    assert player.ricochet_piercing is True

def test_explosion_effects(player):
    """Test explosion effects and cleanup."""
    player._generate_explosion()
    assert len(player.fragments) > 0  # Fragments should be generated
    assert len(player.explosion_particles) > 0

    # Simulate explosion update over time
    for _ in range(31):
        player._update_explosion()

    assert len(player.fragments) == 0
    assert len(player.explosion_particles) == 0  # Should be cleaned up

def test_screen_wraparound(player):
    """Test that the player correctly wraps around the screen edges."""

    player.x = WIDTH  # Right edge (assuming WIDTH = 800)
    simulate_key_presses(player, [])
    assert player.x == 0  # Should wrap around to the left side

    player.x = -1  # Left edge
    simulate_key_presses(player, [])
    assert player.x == WIDTH - 1  # Should wrap around to the right side

    player.y = HEIGHT  # Bottom edge (assuming HEIGHT = 600)
    simulate_key_presses(player, [])
    assert player.y == 0  # Should wrap around to the top

    player.y = -1  # Top edge
    simulate_key_presses(player, [])
    assert player.y == HEIGHT - 1  # Should wrap around to the bottom

# def test_thrust_particles_generated(player):
#     """Test that thrust particles are generated when moving forward."""
#     player.thrusting = False
#     initial_particle_count = len(player.particles)

#     simulate_key_presses(player, [pygame.K_UP])

#     assert player.thrusting is True
#     assert len(player.particles) > initial_particle_count  # New particles should be added

# def test_shield_recharges_correctly(player):
#     """Test that the shield recharges after the cooldown period."""
#     player.take_damage()
#     assert player.shield_active is False

#     # Fast-forward 30 seconds
#     player.last_shield_recharge -= 30
#     player._handle_shield_regeneration()

#     assert player.shield_active is True  # Shield should now be restored

# def test_invincibility_blink_effect(player):
#     """Test that the player blinks when invincible."""
#     player.invincible = True
#     player.invincibility_timer = 10

#     for _ in range(10):
#         assert player.invincible is True
#         player.update({})

#     assert player.invincible is False  # Should turn off after timer ends
