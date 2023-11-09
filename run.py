import pygame
import random
import math


def is_between(val, min_val, max_val):
    if min_val > val < max_val:
        return True


class PlayerShip:
    def __init__(self, starting_pos):
        self.starting_pos = starting_pos  # where we started, dunno why we save it yet
        self.current_pos = starting_pos  # current ship position
        self.points = [(-0.5, -0.866), (-0.5, 0.866), (2.0, 0.0)]  # triangle vertex
        self.scale = 10  # amount moving
        self.size = 1  # size of the ship
        self.score = 0  # player score

    def move(self, display, angle, pressed_keys, dt):
        if pressed_keys[pygame.K_w]:
            self.current_pos.y -= 100 * dt

        if pressed_keys[pygame.K_s]:
            self.current_pos.y += 100 * dt

        if pressed_keys[pygame.K_a]:
            self.current_pos.x -= 100 * dt

        if pressed_keys[pygame.K_d]:
            self.current_pos.x += 100 * dt

        if self.current_pos.x > 700:
            self.current_pos.x = 0

        if self.current_pos.y > 700:
            self.current_pos.y = 0

        if self.current_pos.x < 0:
            self.current_pos.x = 700

        if self.current_pos.y < 0:
            self.current_pos.y = 700

        rotated_point = [pygame.math.Vector2(p).rotate(angle) for p in self.points]
        triangle_points = [(self.current_pos + p * self.scale) for p in rotated_point]
        pygame.draw.polygon(display, (255, 255, 255), triangle_points)
        return triangle_points[2]  # returns front point


class Projectile:
    def __init__(self, starting_pos, angle):
        self.starting_pos = starting_pos  # where we started, dunno why we save it yet
        self.current_pos = starting_pos  # current projectile position
        self.angle = angle
        self.speed = 1
        self.radius = 10
        self.length = 1

    def shoot(self, display):
        pygame.draw.circle(display, (255, 255, 255), self.current_pos, self.radius)


class Enemy:
    def __init__(self):
        self.starting_pos = pygame.math.Vector2(
            (random.randint(0, 700), random.randint(0, 700))
        )  # where we started, dunno why we save it yet
        self.current_pos = self.starting_pos  # current projectile position
        self.angle = random.randint(-180, 180)
        self.speed = 1
        self.radius = random.randint(10, 50)
        self.length = 1

    def move(self, display):
        pygame.draw.circle(display, (255, 255, 255), self.current_pos, self.radius)


disp = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()

player_pos = pygame.math.Vector2((random.randint(0, 700), random.randint(0, 700)))
player = PlayerShip(player_pos)
bullets = []
enemies = []
max_enemies = 4

run = True
while run:
    events = pygame.event.get()

    # seteo vars generales
    mouse_position = pygame.mouse.get_pos()
    mouse_vector = pygame.math.Vector2(mouse_position)
    mouse_angle = pygame.math.Vector2().angle_to(mouse_vector - player.current_pos)
    keys = pygame.key.get_pressed()
    dt = clock.tick(60) / 1000

    # surface
    pygame.Surface.fill(disp, (0, 0, 0))
    point = player.move(disp, mouse_angle, keys, dt)

    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            bullets.append(Projectile(point, mouse_angle))

    if len(enemies) < max_enemies:
        # amount_to_spawn = random.randint(0, max_enemies - len(enemies))
        # print("spawning: ", amount_to_spawn)
        # for i in range(0, amount_to_spawn):
        enemies.append(Enemy())

    for bullet in bullets:
        bullet.length += 10
        bullet.current_pos.y = math.sin(math.radians(bullet.angle)) * bullet.length + (
            bullet.current_pos.y
        )
        bullet.current_pos.x = math.cos(math.radians(bullet.angle)) * bullet.length + (
            bullet.current_pos.x
        )

        if (
            bullet.current_pos.x < 0
            or bullet.current_pos.y < 0
            or bullet.current_pos.x > 700
            or bullet.current_pos.y > 700
        ):
            bullets.remove(bullet)

        bullet.shoot(disp)

    for enemy in enemies:
        enemy.length += 0.1
        enemy.current_pos.y = math.sin(math.radians(enemy.angle)) * enemy.length + (
            enemy.current_pos.y
        )
        enemy.current_pos.x = math.cos(math.radians(enemy.angle)) * enemy.length + (
            enemy.current_pos.x
        )
        if (
            enemy.current_pos.x < 0
            or enemy.current_pos.y < 0
            or enemy.current_pos.x > 700
            or enemy.current_pos.y > 700
        ):
            enemies.remove(enemy)

        enemy.move(disp)

    pygame.display.update()
