import pygame
from Game.ui.button import Button
from Game.scenes.scenes import Scene


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)
        self.title = self.font.render("Torneio de Ferro e Sangue", True, (225, 165, 0))
        self.select_character = Button(300, 250, 200, 60, "Jogadores", self.font, (200, 200, 200), (255, 255, 255))
        
        # Carregar e escalar imagem de fundo
        try:
            self.background = pygame.image.load("public/torneio_ferro_e_sangue.png").convert()
            # Escalar para o tamanho da tela (assumindo 800x600 ou obtido de self.game.screen)
            screen_size = self.game.screen.get_size() if hasattr(self.game, 'screen') else (800, 600)
            self.background = pygame.transform.scale(self.background, screen_size)
        except FileNotFoundError:
            print("Arquivo 'public/torneio_ferro_e_sangue.png' não encontrado. Usando fundo cinza.")
            screen_size = self.game.screen.get_size() if hasattr(self.game, 'screen') else (800, 600)
            self.background = pygame.Surface(screen_size)
            self.background.fill((50, 50, 50))

    def handle_events(self, events):
        for event in events:
            # Lógica dos botões
            if self.select_character.foi_clicado(event):
                from Game.scenes.characterSelectionScene import CharacterSelectionScene
                self.game.change_scene(CharacterSelectionScene(self.game))

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.select_character.checar_hover(mouse_pos)

    def draw(self, screen):
        # Desenhar fundo
        screen.blit(self.background, (0, 0))
        screen.blit(self.title, (238, 100))
        # Desenhar botão
        self.select_character.desenhar(screen)