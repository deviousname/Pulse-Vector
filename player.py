import pygame
from pygame.math import Vector2
from constants import *
from utils import *

class Player:
    def __init__(self):
        self.position = Vector2(WIDTH // 2, HEIGHT // 2)
        self.velocity = Vector2()
        self.depth = 1.0
        self.last_direction = "up"

        self.scroll_states = ["inward", "middle", "outward"]
        self.wheel = 0
        self.wasd_active = False  # Tracks if any of the WASD keys are pressed
        self.scroll_active = False  # Tracks if the mouse scroll was recently used
        self.space_active = False  # Tracks if space is being held

        self.direction = "up"  # This should now always be accurate
        self.scroll_mode = "middle"
        self.boost_velocity = Vector2(0, 0)
        self.boost_decay_rate = 0.995  # Decay slower to allow boost to last
        self.boost_duration = 0.0
        self.max_boost_duration = 0.5  # Seconds of boost

    def handle_target_release(self, target_star, orbital_velocity):
        if target_star is None:
            return

        boost_direction = DIRECTION_VECTORS.get(self.direction, Vector2(0, -1))  # Use ship's facing direction
        boost_direction = Vector2(boost_direction).normalize()  # Normalize the vector

        MAX_BOOST_SPEED = 500
        relative_speed = target_star.relative_velocity.length()
        boost_magnitude = min(relative_speed * 2.0, MAX_BOOST_SPEED)
        self.boost_velocity = boost_direction * boost_magnitude
        self.boost_duration = self.max_boost_duration

    def update_boost(self, delta_time):
        if self.boost_duration > 0:
            self.boost_duration -= delta_time
            self.boost_velocity *= self.boost_decay_rate
            return self.velocity + self.boost_velocity
        return self.velocity

    def handle_input(self, delta_time):
        """Handles player input from the keyboard."""
        keys_pressed = pygame.key.get_pressed()
        depth_change = 0.0

        # Check if WASD keys are pressed
        self.wasd_active = any([
            keys_pressed[pygame.K_w], 
            keys_pressed[pygame.K_a], 
            keys_pressed[pygame.K_s], 
            keys_pressed[pygame.K_d]
        ])
        
        # Check if the space bar is being held
        self.space_active = keys_pressed[pygame.K_SPACE]

        # Determine movement direction
        current_direction = get_direction(keys_pressed, BASE_DIRECTION_MAP)

        # Update last known direction if moving
        if current_direction:
            self.last_direction = current_direction

        # Calculate player acceleration
        acceleration = Vector2(
            (keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]) * PLAYER_SPEED,
            (keys_pressed[pygame.K_s] - keys_pressed[pygame.K_w]) * PLAYER_SPEED
        )

        # Handle depth change (Q, E, and scroll wheel)
        depth_change += (keys_pressed[pygame.K_q] - keys_pressed[pygame.K_e]) * DEPTH_RATE * delta_time
        depth_change += -self.wheel * DEPTH_RATE * delta_time
        self.wheel = 0  # Reset wheel after using it

        # Update player velocity
        self.velocity = acceleration * delta_time

        # Update player position and apply inverse toroidal wrapping
        self.position += self.velocity

        if self.position.x < 0:
            self.position.x += WIDTH
            self.position.y = HEIGHT - self.position.y
        elif self.position.x > WIDTH:
            self.position.x -= WIDTH
            self.position.y = HEIGHT - self.position.y

        if self.position.y < 0:
            self.position.y += HEIGHT
            self.position.x = WIDTH - self.position.x
        elif self.position.y > HEIGHT:
            self.position.y -= HEIGHT
            self.position.x = WIDTH - self.position.x

        # **Update Player Direction**
        if not self.scroll_active and not self.wasd_active:
            # No scroll input and no movement input, return to middle state
            self.scroll_mode = "middle"
        elif not self.scroll_active and self.wasd_active:
            # No scroll input, but player is moving, keep the current position
            pass

        # Set the final direction based on movement and scroll mode
        if self.scroll_mode == "middle":
            self.direction = current_direction or self.last_direction
        else:
            self.direction = f"{current_direction or self.last_direction}_{self.scroll_mode}"

        # If no WASD movement, maintain last known direction
        if not self.wasd_active:
            self.direction = self.last_direction  # Revert to last known direction

        return depth_change

    def handle_wheel(self, y):
        """Handle scroll wheel to switch between in, mid, and out positions"""
        current_index = self.scroll_states.index(self.scroll_mode)
        
        if y < 0 and current_index < len(self.scroll_states) - 1:
            # Scroll down, but do not loop
            self.scroll_mode = self.scroll_states[current_index + 1]
            self.scroll_active = True
        elif y > 0 and current_index > 0:
            # Scroll up, but do not loop
            self.scroll_mode = self.scroll_states[current_index - 1]
            self.scroll_active = True
        
        # Reset scroll after use
        if self.scroll_mode == "outward":
            self.wheel = -1
        elif self.scroll_mode == "inward":
            self.wheel = 1
        else:
            self.wheel = 0
