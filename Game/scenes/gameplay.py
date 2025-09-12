import pygame
import random
from Game.ui.animations import Animation
from Game.ui.button import Button
from Game.scenes.scenes import Scene
from Game.scenes.menu import MenuScene

from Game.scenes.personagem import Personagem
from mago import Mago
from cavaleiro import Cavaleiro
from assasino import Assasino

class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)
        self.clock = pygame.time.Clock()
        self.action_delay_start = 0
        self.is_action_in_progress = False
        self.last_attacker = None
        self.pending_opponent = False  # Novo flag para sequencializar ações

        # Tamanho da tela
        self.screen_width, self.screen_height = self.game.screen.get_size()

        # Carregar fundo da arena
        try:
            self.background = pygame.image.load("public/fundo.jpeg").convert()
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except FileNotFoundError:
            print("Arquivo 'public/fundo.jpeg' não encontrado. Usando fundo preto.")
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((0, 0, 0))

        # Personagens disponíveis e stats

        Personagem_Assasino = Assasino(25,15)
        Personagem_Cavaleiro = Cavaleiro(30,10)
        Personagem_Mago = Mago(10,35)


        self.characters = ["Assassino", "Cavaleiro", "Mago"]
        self.character_stats = {
            "Assassino": {"physical": Personagem_Assasino.getFisica(), "magic": Personagem_Assasino.getMagia(), "idle_paths": ["public/moveChar/right_assassino_idle_1.png", "public/moveChar/right_assassino_idle_2.png"],
                          "physical_paths": ["public/moveChar/right_assassino_ataque_fisico_1.png", "public/moveChar/right_assassino_ataque_fisico_2.png"],
                          "magic_paths": ["public/moveChar/right_assassino_magico_1.png", "public/moveChar/right_assassino_magico_2.png"]},
            "Cavaleiro": {"physical": Personagem_Cavaleiro.getFisica(), "magic": Personagem_Cavaleiro.getMagia(), "idle_paths": ["public/moveChar/right_cavaleiro_idle_1.png", "public/moveChar/right_cavaleiro_idle_2.png"],
                          "physical_paths": ["public/moveChar/right_cavaleiro_ataque_fisico_1.png", "public/moveChar/right_cavaleiro_ataque_fisico_2.png"],
                          "magic_paths": ["public/moveChar/right_cavaleiro_magico_1.png", "public/moveChar/right_cavaleiro_magico_2.png"]},
            "Mago": {"physical": Personagem_Mago.getFisica(), "magic": Personagem_Mago.getMagia(), "idle_paths": ["public/moveChar/right_mago_idle_1.png", "public/moveChar/right_mago_idle_2.png"],
                     "physical_paths": ["public/moveChar/right_mago_ataque_fisico_1.png", "public/moveChar/right_mago_ataque_fisico_2.png"],
                     "magic_paths": ["public/moveChar/right_mago_magico_1.png", "public/moveChar/right_mago_magico_2.png"]}
        }

        # Personagem selecionado
        self.player_character = self.game.selected_character or "Assassino"
        available_opponents = [char for char in self.characters if char != self.player_character]
        self.opponent_character = random.choice(available_opponents)

        # Carregar animações
        self.player_animation = self.load_animation(self.player_character, "idle")
        self.opponent_animation = self.load_animation(self.opponent_character, "idle", flip_x=True)

        # Atributos de combate
        self.player_health = 100
        self.max_health = 100
        self.opponent_health = 100
        self.is_player_turn = True
        self.game_over = False
        self.winner_text = None
        self.end_time = 0

        # Botões de ações
        button_width = 150
        button_height = 50
        button_y = self.screen_height - 100
        self.physical_button = Button(self.screen_width // 3 - button_width // 2, button_y, button_width, button_height, "Ataque Físico", self.font, (200, 200, 200), (255, 255, 255))
        self.magic_button = Button(2 * self.screen_width // 3 - button_width // 2, button_y, button_width, button_height, "Magia", self.font, (200, 200, 200), (255, 255, 255))

        # Textos
        self.player_text = self.font.render(self.player_character, True, (255, 255, 255))
        self.opponent_text = self.font.render(self.opponent_character, True, (255, 255, 255))
        self.turn_text = self.font.render("Seu Turno", True, (255, 255, 255))

    def load_animation(self, character, action_type="idle", flip_x=False):
        """Carrega animação baseada no tipo, com opção de flip."""
        paths_key = f"{action_type}_paths" if action_type != "idle" else "idle_paths"
        paths = self.character_stats[character].get(paths_key, [])
        try:
            return Animation(paths, frame_duration=0.25, scale_size=(200, 200), flip_x=flip_x)
        except FileNotFoundError:
            print(f"Animação {action_type} para {character} não encontrada. Usando estática.")
            static_path = f"public/IconesJogo/{character.lower()}.jpeg"
            return Animation([static_path], frame_duration=0.15, scale_size=(200, 200), flip_x=flip_x)

    def handle_events(self, events):
        if self.game_over:
            return
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_scene(MenuScene(self.game))
            if event.type == pygame.MOUSEBUTTONDOWN and self.is_player_turn:
                if self.physical_button.foi_clicado(event):
                    self.perform_action("physical", self.player_character, self.opponent_character)
                    self.end_player_turn()
                elif self.magic_button.foi_clicado(event):
                    self.perform_action("magic", self.player_character, self.opponent_character)
                    self.end_player_turn()

    def perform_action(self, action, attacker, target):
        """Executa ação, calcula dano, troca animação."""
        self.last_attacker = attacker
        flip_x = attacker == self.opponent_character
        if attacker == self.player_character:
            self.player_animation = self.load_animation(attacker, action)
            self.player_animation.reset()
        else:
            self.opponent_animation = self.load_animation(attacker, action, flip_x=flip_x)
            self.opponent_animation.reset()

        # Calcular dano
        damage = self.character_stats[attacker][action]
        if attacker == self.player_character:
            self.opponent_health = max(0, self.opponent_health - damage)
            print(f"{attacker} usou {action.capitalize()}, causando {damage} de dano a {target}.")
        else:
            self.player_health = max(0, self.player_health - damage)
            print(f"{attacker} usou {action.capitalize()}, causando {damage} de dano a {target}.")

        # Iniciar delay não-bloqueante
        self.is_action_in_progress = True
        self.action_delay_start = pygame.time.get_ticks()

    def end_player_turn(self):
        """Finaliza turno do jogador e sinaliza ação do oponente."""
        self.pending_opponent = True
        self.is_player_turn = False
        self.turn_text = self.font.render("Turno do Oponente", True, (255, 255, 255))

    def update(self):
        if self.game_over:
            if pygame.time.get_ticks() > self.end_time:
                self.game.change_scene(MenuScene(self.game))
            return

        # Atualizar animações sempre
        self.player_animation.update()
        self.opponent_animation.update()

        # Gerenciar delay de ação
        if self.is_action_in_progress:
            if pygame.time.get_ticks() - self.action_delay_start >= 800:
                # Fim do delay: voltar para idle
                if self.last_attacker == self.player_character:
                    self.player_animation = self.load_animation(self.player_character, "idle", flip_x=False)
                elif self.last_attacker == self.opponent_character:
                    self.opponent_animation = self.load_animation(self.opponent_character, "idle", flip_x=True)

                self.is_action_in_progress = False

                if self.pending_opponent:
                    self.pending_opponent = False
                    opponent_action = random.choice(["physical", "magic"])
                    self.perform_action(opponent_action, self.opponent_character, self.player_character)
                else:
                    if not self.is_player_turn:
                        self.is_player_turn = True
                        self.turn_text = self.font.render("Seu Turno", True, (255, 255, 255))

        # Verificar fim do jogo
        if self.player_health <= 0:
            self.game_over = True
            self.winner_text = self.font.render("Você Perdeu!", True, (255, 0, 0))
            self.end_time = pygame.time.get_ticks() + 2000
        elif self.opponent_health <= 0:
            self.game_over = True
            self.winner_text = self.font.render("Você Venceu!", True, (0, 255, 0))
            self.end_time = pygame.time.get_ticks() + 2000

        self.clock.tick(60)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        player_x = self.screen_width // 4 - 100
        opponent_x = 3 * self.screen_width // 4 - 100
        char_y = self.screen_height // 2

        screen.blit(self.player_animation.get_current_frame(), (player_x, char_y))
        screen.blit(self.player_text, (player_x, char_y - 70))
        health_width = int(200 * (self.player_health / self.max_health))
        health_color = (255, 0, 0) if self.player_health > 20 else (255, 100, 100)
        pygame.draw.rect(screen, health_color, (player_x, char_y - 50, health_width, 20))
        pygame.draw.rect(screen, (255, 255, 255), (player_x, char_y - 50, 200, 20), 2)

        screen.blit(self.opponent_animation.get_current_frame(), (opponent_x, char_y))
        screen.blit(self.opponent_text, (opponent_x, char_y - 70))
        health_width = int(200 * (self.opponent_health / self.max_health))
        health_color = (255, 0, 0) if self.opponent_health > 20 else (255, 100, 100)
        pygame.draw.rect(screen, health_color, (opponent_x, char_y - 50, health_width, 20))
        pygame.draw.rect(screen, (255, 255, 255), (opponent_x, char_y - 50, 200, 20), 2)

        if self.is_player_turn and not self.game_over and not self.is_action_in_progress:
            self.physical_button.desenhar(screen)
            self.magic_button.desenhar(screen)

        screen.blit(self.turn_text, (self.screen_width // 2 - 100, 50))
        if self.game_over and self.winner_text:
            screen.blit(self.winner_text, (self.screen_width // 2 - 150, self.screen_height // 2 - 50))