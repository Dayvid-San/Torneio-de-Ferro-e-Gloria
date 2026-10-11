import pygame

from Game.config import RED, WHITE


def draw_bar(screen, x, y, value, max_value, color, width=200, height=20) -> None:
    fill = int(width * value / max_value) if max_value else 0
    pygame.draw.rect(screen, color, (x, y, fill, height))
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)


def draw_health_bar(screen, x, y, hp, max_hp, width=200, height=20) -> None:
    color = RED if hp > 0.2 * max_hp else (255, 100, 100)
    draw_bar(screen, x, y, hp, max_hp, color, width, height)


def draw_mana_bar(screen, x, y, mana, max_mana, width=200, height=10) -> None:
    draw_bar(screen, x, y, mana, max_mana, (60, 120, 255), width, height)
