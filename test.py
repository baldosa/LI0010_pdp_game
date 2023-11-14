import pygame
import random
import math


def display_text(
    display,
    text,
    x,
    y,
    size=50,
):
    # try:
    text = str(text)
    font = pygame.font.Font("TerminessNerdFont-Regular.ttf", size)
    text = font.render(text, True, (255, 255, 255))
    display.blit(text, (x, y))

    # except Exception as e:
    #     print("Font Error, saw it coming")
    #     raise e


def is_between(val: float, from_to: list) -> bool:
    """
    Recives a val and a list with to values, from and to
    Returns True if val is between those two values
    """
    if len(from_to) == 2:
        if from_to[0] <= val <= from_to[1]:
            return True
        else:
            return False
    else:
        print("wrong list size")


class PlayerShip:
    def __init__(self, starting_pos):
        self.starting_pos = starting_pos  # where we started, dunno why we save it yet
        self.current_pos = starting_pos  # current ship position
        self.points = [(-0.5, -0.866), (-0.5, 0.866), (2.0, 0.0)]  # triangle vertex
        self.scale = 10  # amount moving
        self.size = 1  # size of the ship
        self.score = 0  # player score
        self.lives = 3  # player lives

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
        self.radius = 5
        self.length = 1

    def shoot(self, display):
        pygame.draw.circle(
            display, (255, 255, 255), self.current_pos, self.radius, width=1
        )


class Enemy:
    def __init__(self, color=(255, 255, 255)):
        self.starting_pos = pygame.math.Vector2(
            random.randint(0, 700),
            random.randint(0, 700),
        )  # where we started, dunno why we save it yet
        self.current_pos = self.starting_pos  # current projectile position
        self.angle = random.randint(-180, 180)
        self.speed = 1
        self.length = 1
        self.side = random.randint(15, 50)
        self.R = None
        self.color = color

    def move(self, display):
        self.R = pygame.draw.rect(
            display,
            self.color,
            (self.current_pos, (self.side, self.side)),
            0,
        )


pygame.font.init()  # you have to call this at the start,
# if you want to use this module.

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
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    # surface
    pygame.Surface.fill(disp, (0, 0, 0))

    if player.lives > 0:
        point = player.move(disp, mouse_angle, keys, dt)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                bullets.append(Projectile(point, mouse_angle))

        if len(enemies) < max_enemies:
            enemies.append(Enemy())

        for bullet in bullets:
            bullet.length += 0.1
            bullet.current_pos.y = (
                math.sin(math.radians(bullet.angle)) * bullet.length
            ) + (bullet.current_pos.y)
            bullet.current_pos.x = (
                math.cos(math.radians(bullet.angle)) * bullet.length
            ) + (bullet.current_pos.x)

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
            enemy.current_pos.y = (
                math.sin(math.radians(enemy.angle)) * enemy.length
            ) + (enemy.current_pos.y)
            enemy.current_pos.x = (
                math.cos(math.radians(enemy.angle)) * enemy.length
            ) + (enemy.current_pos.x)

            if (
                enemy.current_pos.x < 0
                or enemy.current_pos.y < 0
                or enemy.current_pos.x > 700
                or enemy.current_pos.y > 700
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
                    enemies.remove(enemy)
                    bullets.remove(bullet)
        display_text(disp, f"Points: {player.score}", 10, 680, 15)
    elif player.lives == 0:
        display_text(disp, "GAME OVER", 250, 250)
        display_text(disp, f"Points: {player.score}", 250, 300)

    pygame.display.update()
