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

    # surface
    pygame.Surface.fill(disp, BLACK)

    # leo vars generales
    mouse_position = pygame.mouse.get_pos()
    mouse_vector = pygame.math.Vector2(mouse_position)
    mouse_angle = pygame.math.Vector2().angle_to(mouse_vector - player.current_pos)
    keys = pygame.key.get_pressed()
    dt = clock.tick(60) / 1000

    # if player has lives, the game renders
    if player.lives > 0:
        # check evets to shoot
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                bullets.append(Projectile(player.ship_front, mouse_angle))

        # reads player movement
        player.move(disp, mouse_angle, keys, dt)

        # spawns enemies
        if len(enemies) < MAX_ENEMIES:
            if random.randint(0, MAX_ENEMIES) == MAX_ENEMIES / 2:
                enemies.append(Enemy(color=MAGENTA))
            else:
                enemies.append(Enemy())

        # draws each bullet
        for bullet in bullets:
            bullet.shoot(disp)
            if not bullet.valid:
                bullets.remove(bullet)
        # draw enemies
        for enemy in enemies:
            enemy.move(disp)
            if not enemy.valid:
                enemies.remove(enemy)

            # check if player collides with enemy
            if is_between(
                round(player.current_pos.x, 0),
                [enemy.current_pos.x, enemy.current_pos.x + enemy.side],
            ) and is_between(
                round(player.current_pos.y, 0),
                [enemy.current_pos.y, enemy.current_pos.y + enemy.side],
            ):
                player.lives -= 1

            # check if bullet collides with enemy
            for bullet in bullets:
                if is_between(
                    round(bullet.current_pos.x, 0),
                    [enemy.current_pos.x, enemy.current_pos.x + enemy.side],
                ) and is_between(
                    round(bullet.current_pos.y, 0),
                    [enemy.current_pos.y, enemy.current_pos.y + enemy.side],
                ):
                    player.score += 1

                    enemies.remove(enemy)
                    bullets.remove(bullet)

                    if enemy.color == MAGENTA:
                        player.size += 10
                        player.score += 1
                        player.multiplier += 0.3

        # display player points and lives
        display_text(disp, f"Points: {player.score}", 10, 680, 15)
        display_text(disp, f"Lives: {player.lives}", 600, 680, 15)

    # if the player has not lives the games shows GAME OVER screen
    elif player.lives == 0:
        display_text(disp, "GAME OVER", 250, 250)
        display_text(disp, f"Points: {player.score}", 250, 300)

        # if player press R, gameplay restarts
        display_text(disp, f"Press R to restart", 250, 350, 30)
        if keys[pygame.K_r]:
            player_pos, player, bullets, enemies = start_game()

    pygame.display.update()
