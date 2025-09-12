import pygame
from Game.ui.button import Button
from Game.scenes.scenes import Scene


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)
        self.title = self.font.render("Torneio de Ferro e Sangue", True, (225, 165, 0))
        self.select_character_button = Button(300, 250, 200, 60, "Modo Normal", self.font, (200, 200, 200), (255, 255, 255))
        self.tower_mode_button = Button(300, 350, 200, 60, "Modo Torre", self.font, (200, 200, 200), (255, 255, 255))
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
            self.dark_overlay = pygame.Surface(self.background.get_size(), pygame.SRCALPHA)
            self.dark_overlay.fill((0, 0, 0, 180))  # 120 = nível de escuridão (0-255)


    def handle_events(self, events):
        for event in events:
            if self.select_character_button.foi_clicado(event):
                # Modo Normal não é o modo torre
                self.game.is_in_tower_mode = False
                from Game.scenes.characterSelectionScene import CharacterSelectionScene
                self.game.change_scene(CharacterSelectionScene(self.game))

            if self.tower_mode_button.foi_clicado(event):
                # ATIVA O MODO TORRE E INICIA A PRIMEIRA LUTA
                self.game.is_in_tower_mode = True
                self.game.current_tower_floor = 0
                from Game.scenes.characterSelectionScene import CharacterSelectionScene
                self.game.change_scene(CharacterSelectionScene(self.game))

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.select_character_button.checar_hover(mouse_pos)
        self.tower_mode_button.checar_hover(mouse_pos)

    def draw(self, screen):
        self.select_character_button.desenhar(screen)
        self.tower_mode_button.desenhar(screen)