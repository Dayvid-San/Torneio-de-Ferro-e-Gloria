# Game/ui/text_box.py
import pygame

class TextBox:
    """
    Uma caixa de texto que renderiza um texto longo em múltiplas linhas
    dentro de um fundo semitransparente.
    """
    def __init__(self, x, y, max_width, text, font, font_color=(255, 255, 255), bg_color=(0, 0, 0, 150), padding=10):
        self.x = x
        self.y = y
        self.padding = padding
        self.font = font
        self.font_color = font_color
        self.bg_color = bg_color
        
        self.lines_surfaces = self._wrap_text(text, font, max_width)
        
        box_width = max(line.get_width() for line in self.lines_surfaces) + 2 * padding
        box_height = len(self.lines_surfaces) * font.get_linesize() + 2 * padding
        
        self.box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        self.box_surface.fill(self.bg_color)

    def _wrap_text(self, text, font, max_width):
        """Quebra o texto em múltiplas linhas e retorna uma lista de superfícies renderizadas."""
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line}{word} "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = f"{word} "
        lines.append(current_line)

        return [font.render(line, True, self.font_color) for line in lines]

    def draw(self, screen):
        """Desenha a caixa de fundo e o texto na tela."""
        screen.blit(self.box_surface, (self.x, self.y))
        
        offset_y = self.padding
        for line in self.lines_surfaces:
            screen.blit(line, (self.x + self.padding, self.y + offset_y))
            offset_y += self.font.get_linesize()