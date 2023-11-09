import pygame
import random
import math


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


disp = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
run = True
# player_pos = pygame.math.Vector2((random.randint(0, 700), random.randint(0, 700)))
player_pos = pygame.math.Vector2(0, 0)
player = PlayerShip(player_pos)
bullets = []

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # seteo vars generales
    mouse_position = pygame.mouse.get_pos()
    mouse_vector = pygame.math.Vector2(mouse_position)
    mouse_angle = pygame.math.Vector2().angle_to(mouse_vector - player.current_pos)
    keys = pygame.key.get_pressed()
    dt = clock.tick(60) / 1000

    # surface
    pygame.Surface.fill(disp, (0, 0, 0))
    point = player.move(disp, mouse_angle, keys, dt)

    if pygame.mouse.get_pressed()[0]:
        # if len(bullets) < 2:
        print(point)
        bullets.append(Projectile(point, mouse_angle))

    for bullet in bullets:
        bullet.length += 10
        bullet.current_pos.y = math.sin(math.radians(bullet.angle)) * bullet.length + (
            bullet.current_pos.y - bullet.starting_pos.y
        )
        bullet.current_pos.x = math.cos(math.radians(bullet.angle)) * bullet.length + (
            bullet.current_pos.x - bullet.starting_pos.x
        )
        # print(bullets[0].starting_pos)
        # print(bullets[0].current_pos)
        # print(bullet.angle)
        # print(mouse_angle)
        # print(bullets[0].speed)
        # print(bullets[0].radius)
        # print(bullets[0].length)

        bullet.shoot(disp)
        if all(i >= 700 for i in bullet.current_pos) or all(
            i <= 0 for i in bullet.current_pos
        ):
            bullets.pop(bullets.index(bullet))

    pygame.display.update()
