import pygame

from Game.config import GREY, WHITE
from Game.scenes.base import Scene
from Game.ui.button import Button


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        font = game.assets.font(40)
        self.background = game.assets.image(
            "public/torneio_ferro_e_sangue.png", game.screen.get_size(), alpha=False)
        self.play_button = Button(300, 250, 200, 60, "Jogadores", font, GREY, WHITE)

    def handle_events(self, events):
        for event in events:
            if self.play_button.was_clicked(event):
                self.game.go_to("character_select")

    def update(self, dt):
        self.play_button.update_hover(pygame.mouse.get_pos())

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.play_button.draw(screen)
