import pygame
from pygame.math import Vector2
from constants import *
from utils import *
import math
from spaceship import *

class Player:
    def __init__(self):
        self.position = Vector2(WIDTH // 2, HEIGHT // 2)
        self.velocity = Vector2()
        self.depth = 1.0
        self.last_direction = "up"

        self.scroll_states = ["inward", "middle", "outward"]
        self.wheel = 0
        self.wasd_active = False
        self.scroll_active = False
        self.space_active = False
        self.depth_buffer = 1

        self.direction = "up"
        self.scroll_mode = "middle"
        self.boost_velocity = Vector2(0, 0)
        self.boost_decay_rate = 0.999
        self.boost_duration = 0.0
        self.max_boost_duration = 3
        self.depth_buffer = DEPTH_RATE * 2

        self.manual_control_active = False  # Tracks if player is actively controlling
        self.manual_control_timeout = 0.5   # How long to maintain manual control after input
        self.manual_control_timer = 0.0     # Timer for manual control timeout
        self.target_direction = "up"        # Stores the direction to target
        
    def handle_target_release(self, target_star, orbital_velocity):
        """
        Handles the slingshot boost when releasing a target star.
        Now properly considers the ship's actual facing direction.
        
        Args:
            target_star: The star being released
            orbital_velocity: Current orbital velocity around the star
        """
        if target_star is None:
            return

        # Get the raw direction without scroll modifiers
        base_direction = self.direction.split('_')[0] if '_' in self.direction else self.direction
        
        # Get the direction vector based on the ship's current facing
        boost_direction = Vector2(DIRECTION_VECTORS[base_direction])
        boost_direction = boost_direction.normalize()

        # Calculate boost magnitude based on orbital velocity
        MAX_BOOST_SPEED = 10000
        relative_speed = target_star.relative_velocity.length()
        boost_magnitude = min(relative_speed * 2.0, MAX_BOOST_SPEED)
        
        # Apply the boost in the ship's facing direction
        self.boost_velocity = boost_direction * boost_magnitude
        self.boost_duration = self.max_boost_duration

    def handle_input(self, delta_time, target_star=None):
        """
        Enhanced input handler with improved direction management.
        """
        keys_pressed = pygame.key.get_pressed()
        depth_change = 0.0

        current_manual_input = any([
            keys_pressed[pygame.K_w], 
            keys_pressed[pygame.K_a], 
            keys_pressed[pygame.K_s], 
            keys_pressed[pygame.K_d]
        ])
        
        if current_manual_input:
            self.manual_control_active = True
            self.manual_control_timer = self.manual_control_timeout
        elif self.manual_control_timer > 0:
            self.manual_control_timer -= delta_time
            if self.manual_control_timer <= 0:
                self.manual_control_active = False

        # Get the current movement direction
        current_direction = get_direction(keys_pressed, BASE_DIRECTION_MAP)
        
        # Update last_direction if we have manual input
        if current_direction:
            self.last_direction = current_direction

        # Calculate movement
        acceleration = Vector2(
            (keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]) * PLAYER_SPEED,
            (keys_pressed[pygame.K_s] - keys_pressed[pygame.K_w]) * PLAYER_SPEED
        )

        # Handle depth changes
        depth_change += (keys_pressed[pygame.K_q] - keys_pressed[pygame.K_e]) * DEPTH_RATE * delta_time
        depth_change += -self.wheel * DEPTH_RATE * delta_time
        self.wheel = 0

        self.velocity = acceleration * delta_time
        self._update_position()

        # Direction priority system with proper outward state handling
        if self.manual_control_active:
            # Use manual input direction, preserving scroll state
            base_direction = current_direction if current_direction else self.last_direction
        elif target_star:
            # Calculate direction to target
            base_direction = self.calculate_direction_to_target(target_star.position)
            if not current_manual_input:
                self.last_direction = base_direction
        else:
            base_direction = self.last_direction

        # Apply scroll mode, ensuring all directions are valid in sprite sheet
        if self.scroll_mode != "middle":
            full_direction = f"{base_direction}_{self.scroll_mode}"
            # Verify the direction exists in SPACESHIP_SHAPES
            if full_direction in SPACESHIP_SHAPES:
                self.direction = full_direction
            else:
                # Fallback to base direction if combination doesn't exist
                self.direction = base_direction
        else:
            self.direction = base_direction

        return depth_change

    def calculate_direction_to_target(self, target_position):
        """Calculate the optimal direction to face the target."""
        screen_center = Vector2(WIDTH / 2, HEIGHT / 2)
        to_target = target_position - screen_center
        
        if to_target.length() == 0:
            return self.direction
            
        angle = math.degrees(math.atan2(to_target.y, to_target.x))
        angle = (angle + 360) % 360
        
        # Adjusted angle ranges for smoother direction changes
        direction_ranges = {
            "right": (337.5, 22.5),
            "down-right": (22.5, 67.5),
            "down": (67.5, 112.5),
            "down-left": (112.5, 157.5),
            "left": (157.5, 202.5),
            "up-left": (202.5, 247.5),
            "up": (247.5, 292.5),
            "up-right": (292.5, 337.5)
        }
        
        for direction, (start, end) in direction_ranges.items():
            if start > end:  # Handles the right direction case
                if angle >= start or angle <= end:
                    return direction
            elif start <= angle <= end:
                return direction
                
        return self.last_direction 
        
    def handle_wheel(self, y, target_star=None):
        """
        Handle scroll wheel input with buffered depth limits for targeted stars.
        Maintains ship facing direction even when scroll movement is restricted.
        
        Args:
            y (int): Scroll direction (-1 for scroll down, 1 for scroll up)
            target_star (Star, optional): Currently targeted star, if any
        """
        if y != 0:
            self.manual_control_active = True
            self.manual_control_timer = self.manual_control_timeout
            
        current_index = self.scroll_states.index(self.scroll_mode)
        requested_scroll_mode = None
        
        # Determine requested scroll mode without applying it yet
        if y < 0 and current_index < len(self.scroll_states) - 1:
            requested_scroll_mode = self.scroll_states[current_index + 1]
        elif y > 0 and current_index > 0:
            requested_scroll_mode = self.scroll_states[current_index - 1]
            
        if requested_scroll_mode is None:
            return
            
        # Check depth limits only for actual movement, not direction facing
        if target_star:
            min_depth_with_buffer = MIN_DEPTH + self.depth_buffer
            max_depth_with_buffer = MAX_DEPTH - self.depth_buffer
            
            # Block scroll state change if it would exceed depth limits
            if requested_scroll_mode == "inward" and target_star.depth <= min_depth_with_buffer:
                # Allow direction update but prevent actual scrolling
                self._update_direction_only(requested_scroll_mode)
                return
                
            if requested_scroll_mode == "outward" and target_star.depth >= max_depth_with_buffer:
                # Allow direction update but prevent actual scrolling
                self._update_direction_only(requested_scroll_mode)
                return
        
        # If we reach here, apply full scroll mode change
        self.scroll_mode = requested_scroll_mode
        self.scroll_active = True
        
        # Set wheel value based on scroll mode
        if self.scroll_mode == "outward":
            self.wheel = -1
        elif self.scroll_mode == "inward":
            self.wheel = 1
        else:
            self.wheel = 0

    def _update_direction_only(self, scroll_mode):
        """
        Updates the ship's facing direction without changing scroll state or depth.
        This allows firing in any direction even when movement is restricted.
        
        Args:
            scroll_mode (str): The requested scroll mode that determines direction
        """
        # Update visual direction without changing scroll behavior
        current_direction = get_direction(pygame.key.get_pressed(), BASE_DIRECTION_MAP)
        base_direction = current_direction or self.last_direction
        
        # Set the visual direction with the scroll modifier
        if scroll_mode != "middle":
            self.direction = f"{base_direction}_{scroll_mode}"
        else:
            self.direction = base_direction
            
        # Don't update scroll_mode or wheel to prevent actual movement

    def _update_position(self):
        """Updates player position with toroidal wrapping."""
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

    def update_boost(self, delta_time):
        if self.boost_duration > 0:
            self.boost_duration -= delta_time
            self.boost_velocity *= self.boost_decay_rate
            return self.velocity + self.boost_velocity
        return self.velocity
