# Game/ui/action_box.py
import pygame

class ActionBox:
    def __init__(self, x, y, width, height, options, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.font = font
        self.active = True
        self.hovered_index = -1  # -1 significa que nenhuma opção está sob o mouse
        self.border_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        self.text_color_normal = (200, 200, 200)
        self.text_color_hover = (255, 255, 0) # Dourado para destacar
        self.padding = 20

        self._prepare_options()

    def _prepare_options(self):
        """Pré-calcula as áreas de clique e renderiza os textos."""
        self.rendered_options = []
        self.option_rects = []
        
        option_width = self.rect.width / len(self.options)
        
        for i, option_text in enumerate(self.options):
            # Renderiza o texto para as duas cores (normal e hover)
            surf_normal = self.font.render(option_text, True, self.text_color_normal)
            surf_hover = self.font.render(option_text, True, self.text_color_hover)
            self.rendered_options.append({"normal": surf_normal, "hover": surf_hover})

            # Calcula a área de clique para esta opção
            pos_x = self.rect.x + (i * option_width)
            rect = pygame.Rect(pos_x, self.rect.y, option_width, self.rect.height)
            self.option_rects.append(rect)

    def update(self, mouse_pos):
        if not self.active:
            self.hovered_index = -1
            return

        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                self.hovered_index = i
                return
        self.hovered_index = -1

    def handle_click(self, event):
        
        if not self.active or event.type != pygame.MOUSEBUTTONDOWN or self.hovered_index == -1:
            return None

        # Confirma que o clique foi em cima da opção destacada
        if self.option_rects[self.hovered_index].collidepoint(event.pos):
            return self.options[self.hovered_index]
        
        return None

    def draw(self, screen):
        #Desenha a caixa, as opções e o efeito de hover
        if not self.active:
            return

        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        for i, rendered in enumerate(self.rendered_options):
            # Escolhe qual superfície de texto desenhar (normal ou hover)
            if i == self.hovered_index:
                text_surf = rendered["hover"]
            else:
                text_surf = rendered["normal"]
            
            # Centraliza o texto dentro da sua área de opção
            option_rect = self.option_rects[i]
            text_rect = text_surf.get_rect(center=option_rect.center)
            screen.blit(text_surf, text_rect)