import random
import pygame
from pygame.math import Vector2
from constants import WIDTH, HEIGHT, MIN_DEPTH, MAX_DEPTH, STAR_COLOR
from utils import wrap_depth

class Star:
    def __init__(self, x, y, depth):
        self.position = Vector2(x, y)
        self.depth = depth
        self.size = random.randint(1, 3)

    def update(self, velocity, depth_change, delta_time, is_target=False):
        """Update star position and depth with inverse toroidal wrapping."""
        if is_target:
            self.depth = max(MIN_DEPTH, min(MAX_DEPTH, self.depth + depth_change))
            parallax_factor = 1.0 / self.depth
            new_x = self.position.x - velocity.x * parallax_factor * delta_time
            new_y = self.position.y - velocity.y * parallax_factor * delta_time
            self.position.update(new_x, new_y)
        else:
            self.depth = wrap_depth(self.depth + depth_change)
            parallax_factor = 1.0 / self.depth
            self.position.x -= velocity.x * parallax_factor * delta_time
            self.position.y -= velocity.y * parallax_factor * delta_time

        # Inverse Toroidal Wrapping
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
        radius = max(1, int(self.size / self.depth))
        pygame.draw.circle(surface, STAR_COLOR, (int(self.position.x), int(self.position.y)), radius)
