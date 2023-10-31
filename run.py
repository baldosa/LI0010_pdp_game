import pygame
import math


def rotate_triangle(player_pos, scale, mouse_pos, pressed_keys, dt):
    mouse_vector = pygame.math.Vector2(mouse_pos)
    angle = pygame.math.Vector2().angle_to(mouse_vector - player_pos)

    if pressed_keys[pygame.K_w]:
        player_pos.y -= 100 * dt

    if pressed_keys[pygame.K_s]:
        player_pos.y += 100 * dt

    if pressed_keys[pygame.K_a]:
        player_pos.x -= 100 * dt

    if pressed_keys[pygame.K_d]:
        player_pos.x += 100 * dt

    points = [(-0.5, -0.866), (-0.5, 0.866), (2.0, 0.0)]
    rotated_point = [pygame.math.Vector2(p).rotate(angle) for p in points]

    triangle_points = [(player_pos + p * scale) for p in rotated_point]
    return triangle_points, player_pos


disp = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
run = True
player_pos = pygame.math.Vector2((100, 100))
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # seteo vars generales
    mouse_position = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    dt = clock.tick(60) / 1000

    # get points to draw the ship and the player position
    points, player_pos = rotate_triangle(player_pos, 10, mouse_position, keys, dt)

    pygame.Surface.fill(disp, (0, 0, 0))
    pygame.draw.polygon(disp, (255, 255, 255), points)
    pygame.display.update()
