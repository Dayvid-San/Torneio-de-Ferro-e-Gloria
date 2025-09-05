import pygame
from Game.ui.button import Button
from Game.scenes.scenes import Scene


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)
        self.select_character = Button(300, 250, 200, 60, "Jogadores", self.font, (200,200,200), (255,255,255))

    def handle_events(self, events):
        for event in events:
            # Logica do botões
            if self.select_character.foi_clicado(event):
                from Game.scenes.characterSelectionScene import CharacterSelectionScene
                self.game.change_scene(CharacterSelectionScene(self.game))

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.select_character.checar_hover(mouse_pos)

    def draw(self, screen):
        screen.fill((50, 50, 50))
        self.select_character.desenhar(screen)