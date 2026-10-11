import pygame

from Game.config import RED, WHITE


def draw_health_bar(screen, x, y, hp, max_hp, width=200, height=20) -> None:
    fill = int(width * hp / max_hp) if max_hp else 0
    color = RED if hp > 0.2 * max_hp else (255, 100, 100)
    pygame.draw.rect(screen, color, (x, y, fill, height))
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)
