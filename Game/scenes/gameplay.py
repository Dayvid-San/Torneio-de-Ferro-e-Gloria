import pygame
import random
from Game.ui.animations import Animation
from Game.ui.button import Button
from Game.scenes.scenes import Scene

class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)

        # Carregar fundo da arena
        try:
            self.background = pygame.image.load("public/fundo.jpeg").convert()
            screen_size = self.game.screen.get_size() if hasattr(self.game, 'screen') else (800, 600)
            self.background = pygame.transform.scale(self.background, screen_size)
        except FileNotFoundError:
            print("Arquivo 'public/fundo.jpeg' não encontrado. Usando fundo preto.")
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

        # Escolher oponente aleatoriamente
        available_opponents = [char for char in self.characters if char != self.player_character]
        self.opponent_character = random.choice(available_opponents)

        # Carregar animações idle
        self.player_animation = self.load_character_animation(self.player_character)
        self.opponent_animation = self.load_character_animation(self.opponent_character)

        # Atributos de combate
        self.player_health = 100
        self.opponent_health = 100
        self.is_player_turn = True  # Começa com o turno do jogador

        # Botões de ações
        screen_width = screen_size[0] if 'screen_size' in locals() else 800
        button_y = screen_size[1] - 100 if 'screen_size' in locals() else 500
        self.physical_button = Button(screen_width // 3 - 75, button_y, 150, 50, "Ataque Físico", self.font, (200, 200, 200), (255, 255, 255))
        self.magic_button = Button(2 * screen_width // 3 - 75, button_y, 150, 50, "Magia", self.font, (200, 200, 200), (255, 255, 255))

        # Textos para nomes e turno
        self.player_text = self.font.render(self.player_character, True, (255, 255, 255))
        self.opponent_text = self.font.render(self.opponent_character, True, (255, 255, 255))
        self.turn_text = self.font.render("Turno do Jogador", True, (255, 255, 255))

    def load_character_animation(self, character):
        """Carrega a animação idle do personagem."""
        animation_paths = {
            "Assassino": [
                "public/moveChar/assassino_idle_1.png",
                "public/moveChar/assassino_idle_2.png",
                "public/moveChar/assassino_idle_3.png"
            ],
            "Cavaleiro": [
                "public/moveChar/cavaleiro_idle_1.png",
                "public/moveChar/cavaleiro_idle_2.png",
                "public/moveChar/cavaleiro_idle_3.png"
            ],
            "Mago": [
                "public/moveChar/mago_idle_1.png",
                "public/moveChar/mago_idle_2.png",
                "public/moveChar/mago_idle_3.png"
            ]
        }
        try:
            return Animation(animation_paths[character], frame_duration=0.1, scale_size=(100, 100))
        except FileNotFoundError:
            print(f"Animação idle para {character} não encontrada. Usando imagem estática.")
            static_path = f"public/IconesJogo/{character.lower()}.jpeg"
            try:
                return Animation([static_path], frame_duration=0.1, scale_size=(100, 100))
            except FileNotFoundError:
                print(f"Imagem estática {static_path} não encontrada. Usando placeholder.")
                return Animation([], frame_duration=0.1, scale_size=(100, 100))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Voltar ao menu
                    from Game.scenes.menu import MenuScene
                    self.game.change_scene(MenuScene(self.game))
            if event.type == pygame.MOUSEBUTTONDOWN and self.is_player_turn:
                if self.physical_button.foi_clicado(event):
                    self.perform_action("physical", self.player_character, self.opponent_character)
                    self.end_player_turn()
                elif self.magic_button.foi_clicado(event):
                    self.perform_action("magic", self.player_character, self.opponent_character)
                    self.end_player_turn()

    def perform_action(self, action, attacker, target):
        """Executa uma ação de combate."""
        if action == "physical":
            damage = 20
            if attacker == self.player_character:
                self.opponent_health -= damage
                print(f"{attacker} usou Ataque Físico, causando {damage} de dano a {target}.")
            else:
                self.player_health -= damage
                print(f"{attacker} usou Ataque Físico, causando {damage} de dano a {target}.")
        elif action == "magic":
            damage = 30
            if attacker == self.player_character:
                self.opponent_health -= damage
                print(f"{attacker} usou Magia, causando {damage} de dano a {target}.")
            else:
                self.player_health -= damage
                print(f"{attacker} usou Magia, causando {damage} de dano a {target}.")

    def end_player_turn(self):
        """Finaliza o turno do jogador e inicia o turno do oponente."""
        self.is_player_turn = False
        self.turn_text = self.font.render("Turno do Oponente", True, (255, 255, 255))
        # Oponente escolhe uma ação aleatoriamente
        opponent_action = random.choice(["physical", "magic"])
        self.perform_action(opponent_action, self.opponent_character, self.player_character)
        self.is_player_turn = True
        self.turn_text = self.font.render("Turno do Jogador", True, (255, 255, 255))

    def update(self):
        # Atualizar animações
        self.player_animation.update()
        self.opponent_animation.update()
        # Verificar fim do jogo
        if self.player_health <= 0:
            print("Oponente venceu!")
            from Game.scenes.menu import MenuScene
            self.game.change_scene(MenuScene(self.game))
        elif self.opponent_health <= 0:
            print("Jogador venceu!")
            from Game.scenes.menu import MenuScene
            self.game.change_scene(MenuScene(self.game))

    def draw(self, screen):
        # Desenhar fundo
        screen.blit(self.background, (0, 0))

        # Desenhar sprite do jogador (esquerda)
        screen.blit(self.player_animation.get_current_frame(), (150, 300))
        screen.blit(self.player_text, (150, 250))
        pygame.draw.rect(screen, (255, 0, 0), (150, 220, max(0, self.player_health), 20))

        # Desenhar sprite do oponente (direita)
        screen.blit(self.opponent_animation.get_current_frame(), (550, 300))
        screen.blit(self.opponent_text, (550, 250))
        pygame.draw.rect(screen, (255, 0, 0), (550, 220, max(0, self.opponent_health), 20))

        # Desenhar botões (apenas no turno do jogador)
        if self.is_player_turn:
            self.physical_button.desenhar(screen)
            self.magic_button.desenhar(screen)

        # Desenhar texto do turno
        screen.blit(self.turn_text, (300, 50))