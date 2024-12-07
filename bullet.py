import pygame
from pygame.math import Vector2
from constants import *
import math

class Bullet:
    def __init__(self, position, direction, initial_depth, spaceship_width, spaceship_height):
        self.position = Vector2(position)
        self.direction = direction
        self.initial_depth = initial_depth
        self.depth = initial_depth

        base_speed = 200
        base_direction = direction.split("_")[0]
        self.direction_vector = Vector2(DIRECTION_VECTORS.get(base_direction, (0, -1)))

        if self.direction_vector == Vector2(0, 0):
            self.direction_vector = Vector2(0, -1)

        self.velocity = self.direction_vector * base_speed

        if "inward" in direction:
            self.target_depth = MIN_DEPTH
            self.depth_change = 0.25
            self.velocity *= 0.25
        elif "outward" in direction:
            self.target_depth = BULLET_MAX_DEPTH
            self.depth_change = -0.25
            self.velocity *= 0.25
        else:
            self.target_depth = initial_depth
            self.depth_change = 0.0

        ship_size = min(spaceship_width, spaceship_height)
        self.base_size = max(1, int(ship_size / (2 * self.initial_depth)))

        self.lifespan = 2000 if self.depth_change == 0 else 1000
        self.creation_time = pygame.time.get_ticks()
        self.alive = True

    def update(self, delta_time):
        current_time = pygame.time.get_ticks()
        if (current_time - self.creation_time) > self.lifespan:
            self.alive = False
            return

        self.depth += self.depth_change * delta_time

        # If the bullet has gone out of the depth range, mark it as inactive
        if self.depth < MIN_DEPTH or self.depth > BULLET_MAX_DEPTH:
            self.alive = False
            return

        parallax_factor = max(1e-6, 2.0 / self.depth)
        
        # **Bullet Speed Adjustment by Type**
        if "inward" in self.direction:
            speed_modifier = INWARD_BULLET_SPEED_MOD
            self.position += self.velocity * speed_modifier * delta_time
        elif "outward" in self.direction:
            speed_modifier = OUTWARD_BULLET_SPEED_MOD
            self.position += self.velocity * speed_modifier * parallax_factor * delta_time
        else:
            speed_modifier = NEUTRAL_BULLET_SPEED_MOD
            self.position += self.velocity * speed_modifier * delta_time

        # **Inverse Toroidal Wrapping for Bullets**
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


    def draw(self, surface):
        dynamic_size = max(1, int(self.base_size / (self.depth ** 3.14))) // 2
        color_factor = (self.depth - MIN_DEPTH) / (BULLET_MAX_DEPTH - MIN_DEPTH) * 3
        red_value = int(255 - 127 * color_factor)
        color = (red_value, 0, 0)
        pygame.draw.circle(surface, color, (int(self.position.x), int(self.position.y)), dynamic_size)
