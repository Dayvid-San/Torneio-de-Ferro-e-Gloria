# gameplay.py (VERSÃO FINAL)

import pygame
import random
from Game.ui.button import Button
from Game.scenes.scenes import Scene
from Game.scenes.menu import MenuScene

# Importando nossos novos módulos
from Game.data.character_data import CHARACTER_DATA
from Game.scenes.character import Character #por enquanto não alocamos a classe character no pasta entities
from Game.ui.health_bar import HealthBar #por enquanto não alocamos a classe character no pasta data
# from Game.config import * # Descomente se for usar o config.py

class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # --- CONFIGURAÇÃO INICIAL ---
        self.font = pygame.font.SysFont(None, 40)
        self.screen_width, self.screen_height = self.game.screen.get_size()
        self.clock = pygame.time.Clock()

        # Carregar fundo
        self.background = pygame.image.load("public/fundo.jpeg").convert()
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        
        # --- LÓGICA DE CRIAÇÃO DOS PERSONAGENS ---
        available_chars = list(CHARACTER_DATA.keys())
        player_name = self.game.selected_character or random.choice(available_chars)
        
        available_opponents = [name for name in available_chars if name != player_name]
        opponent_name = random.choice(available_opponents)

        self.player = Character(player_name, CHARACTER_DATA[player_name])
        self.opponent = Character(opponent_name, CHARACTER_DATA[opponent_name], is_flipped=True)
        
        # --- CONFIGURAÇÃO DA INTERFACE (UI) ---
        player_x = self.screen_width // 4 - 100
        opponent_x = 3 * self.screen_width // 4 - 100
        char_y = self.screen_height // 2
        
        self.player_pos = (player_x, char_y)
        self.opponent_pos = (opponent_x, char_y)
        
        self.player_health_bar = HealthBar(player_x, char_y - 50, 200, 20, self.player)
        self.opponent_health_bar = HealthBar(opponent_x, char_y - 50, 200, 20, self.opponent)

        self.player_text = self.font.render(self.player.name, True, (255, 255, 255))
        self.opponent_text = self.font.render(self.opponent.name, True, (255, 255, 255))

        button_y = self.screen_height - 100
        self.physical_button = Button(self.screen_width // 3 - 75, button_y, 150, 50, "Ataque Físico", self.font, (200,200,200), (255,255,255))
        self.magic_button = Button(2 * self.screen_width // 3 - 75, button_y, 150, 50, "Magia", self.font, (200,200,200), (255,255,255))

        # --- CONTROLE DE ESTADO DA CENA ---
        self.is_player_turn = True
        self.turn_text = self.font.render("Seu Turno", True, (255, 255, 255))
        self.is_action_in_progress = False
        self.pending_opponent = False
        self.last_attacker = None
        self.game_over = False
        self.winner_text = None

    def handle_events(self, events):
        if self.game_over: return
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene(MenuScene(self.game))
            if event.type == pygame.MOUSEBUTTONDOWN and self.is_player_turn and not self.is_action_in_progress:
                if self.physical_button.foi_clicado(event):
                    self.perform_action("physical", self.player, self.opponent)
                    self.end_player_turn()
                elif self.magic_button.foi_clicado(event):
                    self.perform_action("magic", self.player, self.opponent)
                    self.end_player_turn()

    def perform_action(self, action_type, attacker, target):
        self.last_attacker = attacker
        attacker.set_action(action_type)
        damage = attacker.get_damage(action_type)
        target.take_damage(damage)
        self.is_action_in_progress = True
        self.action_delay_start = pygame.time.get_ticks()

    def end_player_turn(self):
        self.pending_opponent = True
        self.is_player_turn = False
        self.turn_text = self.font.render("Turno do Oponente", True, (255, 255, 255))

    def update(self):
        if self.game_over:
            if pygame.time.get_ticks() > self.end_time: self.game.change_scene(MenuScene(self.game))
            return

        self.player.update()
        self.opponent.update()

        if self.is_action_in_progress:
            if pygame.time.get_ticks() - self.action_delay_start >= 800: # ACTION_ANIMATION_MS
                self.last_attacker.set_action('idle')
                self.is_action_in_progress = False
                if self.pending_opponent:
                    self.pending_opponent = False
                    opponent_action = random.choice(["physical", "magic"])
                    self.perform_action(opponent_action, self.opponent, self.player)
                elif not self.is_player_turn:
                    self.is_player_turn = True
                    self.turn_text = self.font.render("Seu Turno", True, (255, 255, 255))

        if not self.game_over:
            if self.player.is_dead():
                self.end_game("Você Perdeu!", (255, 0, 0))
            elif self.opponent.is_dead():
                self.end_game("Você Venceu!", (0, 255, 0))
        
        self.clock.tick(60)
    
    def end_game(self, message, color):
        self.game_over = True
        self.winner_text = self.font.render(message, True, color)
        self.end_time = pygame.time.get_ticks() + 2000 # END_GAME_DELAY_MS

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Os próprios objetos se desenham
        self.player.draw(screen, self.player_pos)
        self.opponent.draw(screen, self.opponent_pos)

        # A UI se desenha
        self.player_health_bar.draw(screen)
        self.opponent_health_bar.draw(screen)
        screen.blit(self.player_text, (self.player_pos[0], self.player_pos[1] - 80))
        screen.blit(self.opponent_text, (self.opponent_pos[0], self.opponent_pos[1] - 80))

        if self.is_player_turn and not self.game_over and not self.is_action_in_progress:
            self.physical_button.desenhar(screen)
            self.magic_button.desenhar(screen)
        
        if not self.game_over:
            screen.blit(self.turn_text, (self.screen_width // 2 - 100, 50))
        else:
            text_rect = self.winner_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
            screen.blit(self.winner_text, text_rect)