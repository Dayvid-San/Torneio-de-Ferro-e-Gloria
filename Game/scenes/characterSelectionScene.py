import pygame
from Game.scenes.scenes import Scene

class CharacterSelectionScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)
        self.text = self.font.render("Tela de Seleção de Personagens", True, (255, 255, 255))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Voltar ao menu ao pressionar ESC
                    from Game.scenes.menu import MenuScene
                    self.game.change_scene(MenuScene(self.game))

    def update(self):
        pass  # Aqui você pode adicionar lógica para atualizar a seleção de personagens

    def draw(self, screen):
        screen.fill((30, 30, 100))  # Fundo azul escuro para diferenciar do menu
        screen.blit(self.text, (200, 300))  # Centraliza o texto (ajuste conforme resolução)