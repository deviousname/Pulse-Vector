import pygame
import random
from pygame.math import Vector2

from constants import *
from star import Star
from player import Player
from bullet import Bullet
from utils import draw_box
from spaceship import SPACESHIP_SHAPES, PIXEL_SIZE, draw_spaceship

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0)
        pygame.display.set_caption("Parallax Universe Simulator")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.stars = [
            Star(
                random.uniform(0, WIDTH),
                random.uniform(0, HEIGHT),
                random.uniform(MIN_DEPTH, MAX_DEPTH)
            ) for _ in range(NUM_STARS)
        ]
        self.target_star = None
        self.bullets = []
        self.last_shot_time = 0  # Track the last time a bullet was fired
        self.fire_delay = 500  # Time (ms) between shots

        pygame.event.set_allowed([
            pygame.QUIT,
            pygame.KEYDOWN,
            pygame.KEYUP,
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEWHEEL
        ])

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0  # Time since last frame in seconds
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.target_star = next(
                        (
                            star for star in reversed(self.stars)
                            if (star.position - Vector2(event.pos)).length() <= max(1, int(star.size / star.depth))
                        ), None
                )
                elif event.type == pygame.MOUSEWHEEL:
                    self.player.handle_wheel(event.y)

            # Handle player input
            depth_change = self.player.handle_input(delta_time)

            # Fire bullets if space is held and 0.5 seconds have passed since last shot
            self.handle_continuous_fire()

            if self.target_star:
                depth_change += self.center_zoom(delta_time)
            else:
                self.center_zoom(delta_time)

            for star in self.stars:
                star.update(self.player.velocity, depth_change, delta_time, star is self.target_star)

            # Sort bullets by depth to draw them in correct order
            self.bullets.sort(key=lambda b: b.depth, reverse=True)

            # Update and remove inactive bullets
            for bullet in self.bullets:
                bullet.update(delta_time)

            self.bullets = [bullet for bullet in self.bullets if bullet.alive]

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Draw the stars
            for star in self.stars:
                star.draw(self.screen)

            # Draw bullets, separating by depth
            far_bullets = [b for b in self.bullets if "inward" in b.direction or "outward" not in b.direction]
            near_bullets = [b for b in self.bullets if "outward" in b.direction]

            for bullet in far_bullets:
                bullet.draw(self.screen)

            # Draw the spaceship
            spaceship_shape = SPACESHIP_SHAPES.get(self.player.direction, SPACESHIP_SHAPES["up"])
            spaceship_width = len(spaceship_shape[0]) * PIXEL_SIZE
            spaceship_height = len(spaceship_shape) * PIXEL_SIZE
            spaceship_position = ((WIDTH - spaceship_width) // 2, (HEIGHT - spaceship_height) // 2)
            draw_spaceship(self.screen, spaceship_shape, spaceship_position)

            for bullet in near_bullets:
                bullet.draw(self.screen)

            if self.target_star:
                box_size = max(1, int(self.target_star.size / self.target_star.depth)) * 8
                draw_box(self.screen, self.target_star.position, box_size, TARGET_COLOR)

            pygame.display.flip()

    def handle_continuous_fire(self):
        """Fires a bullet every 0.5 seconds if the spacebar is held"""
        keys_pressed = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        if keys_pressed[pygame.K_SPACE]:
            if current_time - self.last_shot_time >= self.fire_delay:
                self.fire_bullet()
                self.last_shot_time = current_time

    def fire_bullet(self):
        """Fires a bullet from the spaceship"""
        direction = self.player.direction
        if self.player.scroll_mode == "outward":
            direction = f"{self.player.direction}_outward"
        
        bullet_position = Vector2(WIDTH // 2, HEIGHT // 2)
        spaceship_shape = SPACESHIP_SHAPES.get(self.player.direction, SPACESHIP_SHAPES["up"])
        spaceship_width = len(spaceship_shape[0]) * PIXEL_SIZE
        spaceship_height = len(spaceship_shape) * PIXEL_SIZE

        # Create a new bullet and add it to the list
        bullet = Bullet(bullet_position, direction, self.player.depth, spaceship_width, spaceship_height)
        self.bullets.append(bullet)


    def center_zoom(self, delta_time):
        if not self.target_star:
            return 0.0
        center = Vector2(WIDTH / 2, HEIGHT / 2)
        displacement = (center - self.target_star.position) * delta_time
        for star in self.stars:
            star.position += displacement
        for bullet in self.bullets:
            bullet.position += displacement
        depth_delta = (MIN_DEPTH - self.target_star.depth) * delta_time
        if (self.target_star.depth <= MIN_DEPTH and depth_delta < 0) or \
           (self.target_star.depth >= MAX_DEPTH and depth_delta > 0):
            return 0.0
        return depth_delta
