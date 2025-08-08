import pygame

class Button:
    def __init__(self, x, y, largura, altura, texto, fonte, cor, cor_hover):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.fonte = fonte
        self.cor = cor
        self.cor_hover = cor_hover
        self.hovered = False

    def desenhar(self, tela):
        cor = self.cor_hover if self.hovered else self.cor
        pygame.draw.rect(tela, cor, self.rect)

        texto_renderizado = self.fonte.render(self.texto, True, (0, 0, 0))
        tela.blit(texto_renderizado, texto_renderizado.get_rect(center=self.rect.center))

    def checar_hover(self, pos_mouse):
        self.hovered = self.rect.collidepoint(pos_mouse)

    def foi_clicado(self, evento):
        return self.hovered and evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1
