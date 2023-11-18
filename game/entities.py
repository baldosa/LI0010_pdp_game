import math
import pygame
import random
from game.settings import (
    WHITE,
    MAGENTA,
    BLACK,
    LATERAL_SCREEN_SIZE,
    MAX_ENEMIES,
    MULTIPLIER,
)


class PlayerShip:
    def __init__(self, starting_pos):
        self.starting_pos = starting_pos  # where we started, dunno why we save it yet
        self.current_pos = starting_pos  # current ship position
        self.points = [(-0.5, -0.866), (-0.5, 0.866), (2.0, 0.0)]  # triangle vertex
        self.multiplier = MULTIPLIER
        self.size = 10  # size of the ship
        self.score = 0  # player score
        self.lives = 3  # player lives
        self.ship_front = self.starting_pos

    def move(self, display, angle, pressed_keys, dt):
        if pressed_keys[pygame.K_w]:
            self.current_pos.y -= (100 * dt) * self.multiplier

        if pressed_keys[pygame.K_s]:
            self.current_pos.y += (100 * dt) * self.multiplier

        if pressed_keys[pygame.K_a]:
            self.current_pos.x -= (100 * dt) * self.multiplier

        if pressed_keys[pygame.K_d]:
            self.current_pos.x += (100 * dt) * self.multiplier

        if self.current_pos.x > 700:
            self.current_pos.x = 0

        if self.current_pos.y > 700:
            self.current_pos.y = 0

        if self.current_pos.x < 0:
            self.current_pos.x = 700

        if self.current_pos.y < 0:
            self.current_pos.y = 700

        rotated_point = [pygame.math.Vector2(p).rotate(angle) for p in self.points]
        triangle_points = [(self.current_pos + p * self.size) for p in rotated_point]
        pygame.draw.polygon(display, WHITE, triangle_points)
        self.ship_front = triangle_points[2]


class Projectile:
    def __init__(self, starting_pos, angle):
        self.starting_pos = starting_pos  # where we started, dunno why we save it yet
        self.current_pos = starting_pos  # current projectile position
        self.angle = angle
        self.speed = 1
        self.radius = 5
        self.length = 1
        self.valid = True
        self.multiplier = MULTIPLIER

    def shoot(self, display):
        self.length += self.speed * self.multiplier
        self.current_pos.y = (math.sin(math.radians(self.angle)) * self.length) + (
            self.current_pos.y
        )
        self.current_pos.x = (math.cos(math.radians(self.angle)) * self.length) + (
            self.current_pos.x
        )
        if (
            self.current_pos.x < 0
            or self.current_pos.y < 0
            or self.current_pos.x > LATERAL_SCREEN_SIZE
            or self.current_pos.y > LATERAL_SCREEN_SIZE
        ):
            self.valid = False
        pygame.draw.circle(display, WHITE, self.current_pos, self.radius, width=1)


class Enemy:
    def __init__(self, color=WHITE):
        self.starting_pos = pygame.math.Vector2(
            random.randint(0, 700),
            random.randint(0, 700),
        )  # where we started, dunno why we save it yet
        self.current_pos = self.starting_pos  # current projectile position
        self.angle = random.randint(-180, 180)
        self.speed = 0.1
        self.length = 1
        self.side = random.randint(15, 50)
        self.R = None
        self.color = color
        self.valid = True
        self.multiplier = MULTIPLIER

    def move(self, display):
        self.length += self.speed * self.multiplier
        self.current_pos.y = (math.sin(math.radians(self.angle)) * self.length) + (
            self.current_pos.y
        )
        self.current_pos.x = (math.cos(math.radians(self.angle)) * self.length) + (
            self.current_pos.x
        )

        if (
            self.current_pos.x < 0
            or self.current_pos.y < 0
            or self.current_pos.x > LATERAL_SCREEN_SIZE
            or self.current_pos.y > LATERAL_SCREEN_SIZE
        ):
            self.valid = False
        self.R = pygame.draw.rect(
            display,
            self.color,
            (self.current_pos, (self.side, self.side)),
            0,
        )
