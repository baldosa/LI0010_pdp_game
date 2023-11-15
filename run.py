import pygame
import random
import math

from game.entities import PlayerShip, Enemy, Projectile
from game.functions import display_text, is_between
from game.settings import WHITE, MAGENTA, BLACK, LATERAL_SCREEN_SIZE, MAX_ENEMIES


def start_game():
    player_pos = pygame.math.Vector2(
        (random.randint(0, LATERAL_SCREEN_SIZE), random.randint(0, LATERAL_SCREEN_SIZE))
    )
    player = PlayerShip(player_pos)
    bullets = []
    enemies = []
    return player_pos, player, bullets, enemies


# init game
pygame.font.init()
disp = pygame.display.set_mode((LATERAL_SCREEN_SIZE, LATERAL_SCREEN_SIZE))
clock = pygame.time.Clock()
player_pos, player, bullets, enemies = start_game()
run = True

while run:
    # read events
    events = pygame.event.get()

    # exit game
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    pygame.Surface.fill(disp, BLACK)

    # leo vars generales
    mouse_position = pygame.mouse.get_pos()
    mouse_vector = pygame.math.Vector2(mouse_position)
    mouse_angle = pygame.math.Vector2().angle_to(mouse_vector - player.current_pos)
    keys = pygame.key.get_pressed()
    dt = clock.tick(60) / 1000

    # surface

    if player.lives > 0:
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                bullets.append(Projectile(player.ship_front, mouse_angle))

        player.move(disp, mouse_angle, keys, dt)

        if len(enemies) < MAX_ENEMIES:
            if random.randint(0, MAX_ENEMIES) == MAX_ENEMIES / 2:
                enemies.append(Enemy(color=MAGENTA))
            else:
                enemies.append(Enemy())

        for bullet in bullets:
            bullet.length += 1
            bullet.current_pos.y = (
                math.sin(math.radians(bullet.angle)) * bullet.length
            ) + (bullet.current_pos.y)
            bullet.current_pos.x = (
                math.cos(math.radians(bullet.angle)) * bullet.length
            ) + (bullet.current_pos.x)

            if (
                bullet.current_pos.x < 0
                or bullet.current_pos.y < 0
                or bullet.current_pos.x > LATERAL_SCREEN_SIZE
                or bullet.current_pos.y > LATERAL_SCREEN_SIZE
            ):
                bullets.remove(bullet)

            bullet.shoot(disp)

        for enemy in enemies:
            enemy.length += 0.1
            enemy.current_pos.y = (
                math.sin(math.radians(enemy.angle)) * enemy.length
            ) + (enemy.current_pos.y)
            enemy.current_pos.x = (
                math.cos(math.radians(enemy.angle)) * enemy.length
            ) + (enemy.current_pos.x)

            if (
                enemy.current_pos.x < 0
                or enemy.current_pos.y < 0
                or enemy.current_pos.x > LATERAL_SCREEN_SIZE
                or enemy.current_pos.y > LATERAL_SCREEN_SIZE
            ):
                enemies.remove(enemy)

            enemy.move(disp)
            if is_between(
                round(player.current_pos.x, 0),
                [enemy.current_pos.x, enemy.current_pos.x + enemy.side],
            ) and is_between(
                round(player.current_pos.y, 0),
                [enemy.current_pos.y, enemy.current_pos.y + enemy.side],
            ):
                player.lives -= 1

            for bullet in bullets:
                if is_between(
                    round(bullet.current_pos.x, 0),
                    [enemy.current_pos.x, enemy.current_pos.x + enemy.side],
                ) and is_between(
                    round(bullet.current_pos.y, 0),
                    [enemy.current_pos.y, enemy.current_pos.y + enemy.side],
                ):
                    player.score += 1
                    if enemy.color == MAGENTA:
                        player.size += 10
                        player.score += 1
                    enemies.remove(enemy)
                    bullets.remove(bullet)

        display_text(disp, f"Points: {player.score}", 10, 680, 15)
        display_text(disp, f"Lives: {player.lives}", 600, 680, 15)

    elif player.lives == 0:
        display_text(disp, "GAME OVER", 250, 250)
        display_text(disp, f"Points: {player.score}", 250, 300)
        display_text(disp, f"Press R to restart", 250, 350, 30)
        if keys[pygame.K_r]:
            player_pos, player, bullets, enemies = start_game()

    pygame.display.update()
