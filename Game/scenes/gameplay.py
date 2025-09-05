import pygame
import random
from Game.scenes.scenes import Scene

class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)

        # Carregar fundo da arena
        self.background = pygame.image.load("public/fundo.jpeg").convert()

        # Lista de personagens disponíveis
        self.characters = ["Assassino", "Cavaleiro", "Mago"]

        # Personagem selecionado
        self.player_character = self.game.selected_character

        # Escolher oponente aleatoriamente (excluindo o personagem selecionado)
        available_opponents = [char for char in self.characters if char != self.player_character]
        self.opponent_character = random.choice(available_opponents)

        # Carregar sprites do jogador e do oponente
        self.player_sprite = self.load_character_sprite(self.player_character)
        self.opponent_sprite = self.load_character_sprite(self.opponent_character)

        # Escalar sprites para um tamanho uniforme (ex.: 100x100 pixels)
        self.player_sprite = pygame.transform.scale(self.player_sprite, (100, 100))
        self.opponent_sprite = pygame.transform.scale(self.opponent_sprite, (100, 100))

        # Textos para exibir os nomes
        self.player_text = self.font.render(self.player_character, True, (255, 255, 255))
        self.opponent_text = self.font.render(self.opponent_character, True, (255, 255, 255))

    def load_character_sprite(self, character):
        """Carrega o sprite do personagem com base no nome."""
        sprite_paths = {
            "Assassino": "public/IconesJogo/assassino.jpeg",
            "Cavaleiro": "public/IconesJogo/cavaleiro.jpeg",
            "Mago": "public/IconesJogo/mago.jpeg"
        }
        return pygame.image.load(sprite_paths[character]).convert_alpha()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Voltar ao menu
                    from Game.scenes.menu import MenuScene
                    self.game.change_scene(MenuScene(self.game))

    def update(self):
        pass  # Adicione lógica de combate aqui (ex.: animações, turnos)

    def draw(self, screen):
        # Desenhar fundo
        screen.blit(self.background, (0, 0))

        # Desenhar sprite do jogador (esquerda)
        screen.blit(self.player_sprite, (150, 300))
        screen.blit(self.player_text, (150, 250))  # Nome acima do sprite

        # Desenhar sprite do oponente (direita)
        screen.blit(self.opponent_sprite, (550, 300))
        screen.blit(self.opponent_text, (550, 250))  # Nome acima do sprite