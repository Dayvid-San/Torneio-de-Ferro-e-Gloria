import pygame

from Game.config import GREY, WHITE


class Button:
    def __init__(self, x, y, width, height, text, font,
                 color=GREY, hover_color=WHITE, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.hovered = False
        self.pressed = False
        self.enabled = True
        self._label = font.render(text, True, text_color)

    def update_hover(self, mouse_pos) -> None:
        self.hovered = self.enabled and self.rect.collidepoint(mouse_pos)

    def was_clicked(self, event) -> bool:
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False
        return False

    def draw(self, screen) -> None:
        if not self.enabled:
            color = (90, 90, 90)
        elif self.pressed:
            color = tuple(max(0, c - 50) for c in self.color)
        else:
            color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        screen.blit(self._label, self._label.get_rect(center=self.rect.center))
