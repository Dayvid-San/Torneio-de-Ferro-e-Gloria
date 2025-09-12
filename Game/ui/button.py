import pygame

class Button:
    def __init__(self, x, y, largura, altura, texto, fonte, cor, cor_hover, cor_texto=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.fonte = fonte
        self.cor = cor
        self.cor_hover = cor_hover
        self.cor_texto = cor_texto 
        self.hovered = False
        self.pressed = False  
        self.texto_renderizado = self.fonte.render(texto, True, self.cor_texto)

    def desenhar(self, tela):
        # Cor dinâmica: pressed > hover > normal
        if self.pressed:
            cor = tuple(max(0, c - 50) for c in self.cor)  # Mais escura no pressed
        elif self.hovered:
            cor = self.cor_hover
        else:
            cor = self.cor
        
        pygame.draw.rect(tela, cor, self.rect)
        # Borda para estilo pixel art
        pygame.draw.rect(tela, (255, 255, 255), self.rect, 2)  
        
        # Centralizar e desenhar texto
        text_rect = self.texto_renderizado.get_rect(center=self.rect.center)
        tela.blit(self.texto_renderizado, text_rect)

    def checar_hover(self, pos_mouse):
    
        self.hovered = self.rect.collidepoint(pos_mouse)

    def foi_clicado(self, evento):
       
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self.pressed = True  # Ativa pressed
                return True
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            self.pressed = False  # Desativa ao soltar
        return False

    def update(self, eventos): 
        for evento in eventos:
            if self.foi_clicado(evento):
                pass  # Ação já retornada
    