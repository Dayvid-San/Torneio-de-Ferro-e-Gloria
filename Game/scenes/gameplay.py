import pygame
import random
from Game.ui.animations import Animation
from Game.scenes.scenes import Scene

class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)

        # Carregar fundo da arena (com fallback se não encontrado)
        try:
            self.background = pygame.image.load("public/fundo.jpeg").convert()
            screen_size = self.game.screen.get_size() if hasattr(self.game, 'screen') else (800, 600)
            self.background = pygame.transform.scale(self.background, screen_size)
        except FileNotFoundError:
            print("Arquivo 'public/arena.jpeg' não encontrado. Usando fundo preto.")
            screen_size = self.game.screen.get_size() if hasattr(self.game, 'screen') else (800, 600)
            self.background = pygame.Surface(screen_size)
            self.background.fill((0, 0, 0))

        # Lista de personagens disponíveis
        self.characters = ["Assassino", "Cavaleiro", "Mago"]

        # Personagem selecionado
        self.player_character = self.game.selected_character
        if not self.player_character:
            print("Nenhum personagem selecionado. Usando padrão: Assassino.")
            self.player_character = "Assassino"

        # Escolher oponente aleatoriamente (excluindo o personagem selecionado)
        available_opponents = [char for char in self.characters if char != self.player_character]
        self.opponent_character = random.choice(available_opponents)

        # Carregar animações idle do jogador e do oponente
        self.player_animation = self.load_character_animation(self.player_character)
        self.opponent_animation = self.load_character_animation(self.opponent_character)

        # Textos para exibir os nomes
        self.player_text = self.font.render(self.player_character, True, (255, 255, 255))
        self.opponent_text = self.font.render(self.opponent_character, True, (255, 255, 255))


    def load_character_animation(self, character):
        """Carrega a animação idle do personagem."""
        animation_paths = {
            "Assassino": [
                "public/moveChar/assassino_idle_1.png",
                "public/moveChar/assassino_idle_2.png",
            ],
            "Cavaleiro": [
                "public/moveChar/cavaleiro_idle_1.png",
                "public/moveChar/cavaleiro_idle_2.png",
            ],
            "Mago": [
                "public/moveChar/mago_idle_1.png",
                "public/moveChar/mago_idle_2.png",
            ]
        }
        # Tentar carregar animação idle; fallback para imagem estática
        try:
            return Animation(animation_paths[character], frame_duration=0.4, scale_size=(100, 100))
        except FileNotFoundError:
            print(f"Animação idle para {character} não encontrada. Usando imagem estática.")
            static_path = f"public/IconesJogo/{character.lower()}.jpeg"
            return Animation([static_path], frame_duration=0.1, scale_size=(100, 100))

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
        self.player_animation.update()
        self.opponent_animation.update()


    def draw(self, screen):
        # Desenhar fundo
        screen.blit(self.background, (0, 0))

        # Desenhar sprite do jogador (esquerda)
        screen.blit(self.player_animation.get_current_frame(), (150, 420))
        screen.blit(self.player_text, (150, 350))  # Nome acima do sprite

        # Desenhar sprite do oponente (direita)
        screen.blit(self.opponent_animation.get_current_frame(), (550, 420))
        screen.blit(self.opponent_text, (550, 350))  # Nome acima do sprite