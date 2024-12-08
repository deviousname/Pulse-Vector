import random
import pygame
from pygame.math import Vector2
from constants import WIDTH, HEIGHT, MIN_DEPTH, MAX_DEPTH, STAR_COLOR

class Star:
    def __init__(self, x, y, depth):
        """Initialize a star with position (x, y) and depth."""
        self.position = Vector2(x, y)
        self.velocity = Vector2(random.uniform(-50, 50), random.uniform(-50, 50))  # Random movement
        self.depth = depth
        self.size = random.randint(1, 3)
        self.relative_velocity = Vector2(0, 0)  # Velocity relative to player

    def update(self, player_velocity, depth_change, delta_time, is_target=False):
        """
        Update the star's position and depth, and calculate relative velocity to the player.
        Args:
            player_velocity (Vector2): The player's velocity.
            depth_change (float): The change in depth.
            delta_time (float): The delta time between frames.
            is_target (bool): Whether this star is the target.
        """
        # **Depth Adjustment and Wrapping**
        old_depth = self.depth
        self.depth += depth_change
        wrapped_depth = False

        # Handle depth wrapping
        if self.depth > MAX_DEPTH:
            self.depth = MIN_DEPTH
            wrapped_depth = True
        elif self.depth < MIN_DEPTH:
            self.depth = MAX_DEPTH
            wrapped_depth = True

        # Handle depth-based position inversion when wrapping
        if wrapped_depth:
            self.position.x = WIDTH - self.position.x
            self.position.y = HEIGHT - self.position.y

        # **Parallax Effect Based on Depth**
        parallax_factor = 1.0 / max(self.depth, MIN_DEPTH)
        self.position.x -= player_velocity.x * parallax_factor * delta_time
        self.position.y -= player_velocity.y * parallax_factor * delta_time

        # **Relative Velocity Calculation**
        self.relative_velocity = self.velocity - player_velocity

        # **2D Wrapping with Inversion Logic**
        # Handle horizontal wrapping
        if self.position.x < 0:
            self.position.x = WIDTH + self.position.x
            self.position.y = HEIGHT - self.position.y
        elif self.position.x > WIDTH:
            self.position.x = self.position.x - WIDTH
            self.position.y = HEIGHT - self.position.y

        # Handle vertical wrapping
        if self.position.y < 0:
            self.position.y = HEIGHT + self.position.y
            self.position.x = WIDTH - self.position.x
        elif self.position.y > HEIGHT:
            self.position.y = self.position.y - HEIGHT
            self.position.x = WIDTH - self.position.x

        # **Ensure Position Stays Within Bounds**
        self.position.x = max(0.1, min(self.position.x, WIDTH - 0.1))
        self.position.y = max(0.1, min(self.position.y, HEIGHT - 0.1))

    def draw(self, surface):
        """
        Draw the star on the screen.
        Args:
            surface (pygame.Surface): The Pygame surface to draw on.
        """
        radius = max(1, int(self.size / self.depth))  # Scale size based on depth
        pygame.draw.circle(surface, STAR_COLOR, (int(self.position.x), int(self.position.y)), radius)
