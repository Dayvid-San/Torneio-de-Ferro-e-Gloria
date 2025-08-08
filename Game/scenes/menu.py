import pygame
from Game.ui.button import Button

class MenuScene:
    def __init__(self, game):
        self.game = game
        self.fonte = pygame.font.SysFont(None, 40)
        self.botao_jogar = Button(300, 250, 200, 60, "Jogar", self.fonte, (200,200,200), (255,255,255))

    def handle_events(self, events):
        for evento in events:
            if self.botao_jogar.foi_clicado(evento):
                from scenes.jogo import GameScene
                self.game.trocar_cena(GameScene(self.game))

    def update(self):
        self.botao_jogar.checar_hover(pygame.mouse.get_pos())

    def draw(self, tela):
        tela.fill((50, 50, 50))
        self.botao_jogar.desenhar(tela)
