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
        labels = {"torneio": "Torneio", "duelo": "Duelo Rápido", "sair": "Sair"}
        self.buttons = {
            key: Button(280, 230 + i * 80, 240, 60, text, font, GREY, WHITE)
            for i, (key, text) in enumerate(labels.items())
        }
        self.hint = game.assets.font(24).render("M: som on/off", True, WHITE)

    def handle_events(self, events):
        for event in events:
            for key, button in self.buttons.items():
                if not button.was_clicked(event):
                    continue
                if key == "sair":
                    self.game.running = False
                else:
                    self.game.mode = key
                    self.game.go_to("character_select")
                return

    def update(self, dt):
        mouse = pygame.mouse.get_pos()
        for button in self.buttons.values():
            button.update_hover(mouse)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for button in self.buttons.values():
            button.draw(screen)
        screen.blit(self.hint, (10, screen.get_height() - 30))
