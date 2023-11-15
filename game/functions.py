import pygame
from game.settings import WHITE


def display_text(
    display,
    text,
    x,
    y,
    size=50,
):
    font = pygame.font.Font("terminus.ttf", size)
    text = font.render(str(text), True, WHITE)
    display.blit(text, (x, y))


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
