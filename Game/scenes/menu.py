import pygame
from Game.ui.button import Button
from Game.scenes.scenes import Scene  # Use Game. aqui também

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)
        self.play_button = Button(300, 250, 200, 60, "Jogar", self.font, (200,200,200), (255,255,255))

    def handle_events(self, events):
        for event in events:
            if self.play_button.foi_clicado(event):
                from Game.scenes.gameplay import GameplayScene
                self.game.change_scene(GameplayScene(self.game))

    def update(self):
        self.play_button.checar_hover(pygame.mouse.get_pos())

    def draw(self, screen):
        screen.fill((50, 50, 50))
        self.play_button.desenhar(screen)