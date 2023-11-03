import pygame
import math


class PlayerShip:
    def __init__(self, starting_pos):
        self.starting_pos = starting_pos  # where we started, dunno why we save it yet
        self.current_pos = starting_pos  # current ship position
        self.points = [(-0.5, -0.866), (-0.5, 0.866), (2.0, 0.0)]  # triangle vertex
        self.scale = 10  # amount moving
        self.size = 1  # size of the ship
        self.score = 0  # player score

    def move(self, display, mouse_pos, pressed_keys, dt):
        mouse_vector = pygame.math.Vector2(mouse_pos)
        angle = pygame.math.Vector2().angle_to(mouse_vector - self.current_pos)

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
        print(angle)
        pygame.draw.polygon(display, (255, 255, 255), triangle_points)
        return triangle_points[2]


class Projectile:
    def __init__(self, starting_pos, mouse_pos):
        self.starting_pos = starting_pos  # where we started, dunno why we save it yet
        self.current_pos = starting_pos  # current projectile position
        self.speed = 5
        self.radius = 15
        self.mouse_vector = pygame.math.Vector2(mouse_pos)
        self.angle = pygame.math.Vector2().angle_to(
            self.mouse_vector - self.current_pos
        )

    def shoot(self, display):
        pygame.draw.circle(display, (255, 255, 255), self.current_pos, self.radius)


disp = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
run = True
player_pos = pygame.math.Vector2((100, 100))
player = PlayerShip(player_pos)
bullets = []

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # seteo vars generales
    mouse_position = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    dt = clock.tick(60) / 1000

    # surface
    pygame.Surface.fill(disp, (0, 0, 0))
    point = player.move(disp, mouse_position, keys, dt)

    if pygame.mouse.get_pressed()[0]:
        if len(bullets) < 10:
            bullets.append(Projectile(point, mouse_position))

    for bullet in bullets:
        bullet.current_pos = pygame.math.Vector2(
            [x + bullet.speed for x in bullet.current_pos]
        )

        if all(i >= 700 for i in bullet.current_pos) or all(
            i <= 0 for i in bullet.current_pos
        ):
            bullets.pop(bullets.index(bullet))

    for bullet in bullets:
        print(len(bullets))
        bullet.shoot(disp)
    # print(mouse_position)
    pygame.display.update()
