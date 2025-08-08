import pygame

VERMELHO = (255, 0, 0)

class Jogador:
    def __init__(self, x, y):
        self.largura = 50
        self.altura = 50
        self.x = x
        self.y = y
        self.velocidade = 5

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidade
        if teclas[pygame.K_UP]:
            self.y -= self.velocidade
        if teclas[pygame.K_DOWN]:
            self.y += self.velocidade

    def desenhar(self, tela):
        pygame.draw.rect(tela, VERMELHO, (self.x, self.y, self.largura, self.altura))
