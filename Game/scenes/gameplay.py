import pygame
import random
from Game.ui.button import Button
from Game.scenes.scenes import Scene
from Game.scenes.menu import MenuScene
from config import ARENA_GROUND_Y,CHARACTER_HEIGHT 

from Game.data.tower_data import TOWER_NORMAL
from Game.data.character_data import CHARACTER_DATA
from Game.scenes.character import Character #por enquanto não alocamos a classe character no pasta entities
from Game.ui.health_bar import HealthBar #por enquanto não alocamos a classe character no pasta data
from Game.ui.action_box import ActionBox

class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # --- CONFIGURAÇÃO INICIAL ---
        self.font = pygame.font.SysFont(None, 40)
        self.big_font = pygame.font.SysFont(None, 74)
        self.screen_width, self.screen_height = self.game.screen.get_size()
        self.clock = pygame.time.Clock()

        # Carregar fundo
        self.background = pygame.image.load("public/fundo.jpeg").convert()
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        
        # --- LÓGICA DE CRIAÇÃO DOS PERSONAGENS ---
        available_chars = list(CHARACTER_DATA.keys())
        player_name = self.game.selected_character or random.choice(available_chars)
        
        if self.game.is_in_tower_mode:
            floor = self.game.current_tower_floor
            if floor < len(TOWER_NORMAL):
                opponent_name = TOWER_NORMAL[floor]
            else:
                # O que fazer se a torre acabar? Por enquanto, um oponente aleatório.
                opponent_name = random.choice([name for name in available_chars if name != player_name])
        else:
            # Modo Normal: oponente aleatório como antes
            available_opponents = [name for name in available_chars if name != player_name]
            opponent_name = random.choice(available_opponents)

        self.player = Character(player_name, CHARACTER_DATA[player_name])
        self.opponent = Character(opponent_name, CHARACTER_DATA[opponent_name], is_flipped=True)
        
        available_opponents = [name for name in available_chars if name != player_name]
        opponent_name = random.choice(available_opponents)

        self.player = Character(player_name, CHARACTER_DATA[player_name])
        self.opponent = Character(opponent_name, CHARACTER_DATA[opponent_name], is_flipped=True)
        
        # --- CONFIGURAÇÃO DA INTERFACE (UI) ---
        player_x = self.screen_width // 4 - 100
        opponent_x = 3 * self.screen_width // 4 - 100
        char_y = ARENA_GROUND_Y - CHARACTER_HEIGHT # out: 320
        
        self.player_pos = (player_x, char_y)
        self.opponent_pos = (opponent_x, char_y)
        
        self.player_health_bar = HealthBar(player_x, char_y - 50, 200, 20, self.player)
        self.opponent_health_bar = HealthBar(opponent_x, char_y - 50, 200, 20, self.opponent)

        self.player_text = self.font.render(self.player.name, True, (255, 255, 255))
        self.opponent_text = self.font.render(self.opponent.name, True, (255, 255, 255))

        #button_y = self.screen_height - 100
        #self.physical_button = Button(self.screen_width // 3 - 75, button_y, 150, 50, "Ataque Físico", self.font, (200,200,200), (255,255,255))
        #self.magic_button = Button(2 * self.screen_width // 3 - 75, button_y, 150, 50, "Magia", self.font, (200,200,200), (255,255,255))
        action_box_y = self.screen_height - 100
        options = ["ATK", "SPELL", "DEF", "HEAL"] 
        self.action_box = ActionBox(
            x=50, 
            y=action_box_y, 
            width=self.screen_width - 100, 
            height=80, 
            options=options, 
            font=self.font
        )
        # --- CONTROLE DE ESTADO DA CENA ---
        self.is_player_turn = True
        self.turn_text = self.font.render("Seu Turno", True, (255, 255, 255))
        self.is_action_in_progress = False
        self.pending_opponent = False
        self.last_attacker = None
        self.game_over = False
        self.winner_text = None
        self.player_won = False
        self.tower_cleared = False

    def handle_events(self, events):
        if self.game_over: return
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene(MenuScene(self.game))

            if self.is_player_turn and not self.is_action_in_progress:
                selected_action = self.action_box.handle_click(event)
                if selected_action:
                    if selected_action == "ATK":
                        self.perform_action("physical", self.player, self.opponent)
                        self.end_player_turn()
                    elif selected_action == "SPELL":
                        self.perform_action("magic", self.player, self.opponent)
                        self.end_player_turn()
                    elif selected_action == "DEF": 
                        self.player.defend()
                        self.perform_action("defend", self.player, self.opponent) # "defend" como tipo de ação
                    elif selected_action == "HEAL": 
                        self.player.heal()
                        self.perform_action("heal", self.player, self.opponent) # "heal" como tipo de ação
                    self.end_player_turn()

    def perform_action(self, action_type, attacker, target):
        self.last_attacker = attacker
        attacker.set_action(action_type)

        # Ações que causam dano
        if action_type in ["physical", "magic"]:
            damage = attacker.get_damage(action_type)
            target.take_damage(damage)

        self.is_action_in_progress = True
        self.action_delay_start = pygame.time.get_ticks()

    def end_player_turn(self):
        self.pending_opponent = True
        self.is_player_turn = False
        self.turn_text = self.font.render("Turno do Oponente", True, (255, 255, 255))

    def update(self):
        # PARTE 1: LÓGICA DE FIM DE JOGO E TRANSIÇÃO DE CENAS
        if self.game_over:
            if pygame.time.get_ticks() > self.end_time:
                if self.tower_cleared:
                    self.game.change_scene(MenuScene(self.game))
                    return

                if self.player_won and self.game.is_in_tower_mode:
                    self.game.current_tower_floor += 1
                    
                    if self.game.current_tower_floor < len(TOWER_NORMAL):
                        self.game.change_scene(GameplayScene(self.game))
                    else:
                        self.tower_cleared = True
                        self.winner_text = self.big_font.render("TORRE CONQUISTADA!", True, (255, 215, 0))
                        self.end_time = pygame.time.get_ticks() + 4000
                else:
                    self.game.change_scene(MenuScene(self.game))
            return 

        # PARTE 2LÓGICA DE JOGO ATIVO (QUANDO NÃO É GAME OVER) 
        self.player.update()
        self.opponent.update()
        self.action_box.update(pygame.mouse.get_pos())

        if self.is_action_in_progress:
            if pygame.time.get_ticks() - self.action_delay_start >= 800:
                self.last_attacker.set_action('idle')
                self.is_action_in_progress = False
                if self.pending_opponent:
                    self.pending_opponent = False
                    
                    #  IA DO OPONENTE ATUALIZADA 
                    chosen_action = None
                    
                    # Regra de Emergência: Curar com vida baixa é prioridade.
                    # Usamos 35% da vida máxima como gatilho.
                    if self.opponent.current_health < self.opponent.max_health * 0.35:
                        # Tem uma chance alta de curar, mas não é 100% garantido para não ser previsível.
                        if random.random() < 0.8: # 80% de chance de curar
                             chosen_action = "heal"

                    # Se nenhuma ação de emergência foi escolhida, decide com base na "personalidade".
                    if not chosen_action:
                        actions = []
                        weights = []
                        
                        # Personalidade do Mago: Foco em Magia e Cura
                        if "Mago" in self.opponent.name or "Aprendiz" in self.opponent.name:
                            actions = ["magic", "heal", "defend", "physical"]
                            weights = [65, 20, 10, 5] # 65% chance de usar magia, 5% de ataque físico
                        
                        # Personalidade do Cavaleiro: Foco em Ataque Físico e Defesa
                        elif "Cavaleiro" in self.opponent.name or "Guarda" in self.opponent.name:
                            actions = ["physical", "defend", "magic", "heal"]
                            weights = [55, 30, 10, 5] # 55% de chance de ataque físico, 30% de defesa
                        
                        # Personalidade do Assassino (e padrão): Agressivo
                        else:
                            actions = ["physical", "magic", "heal", "defend"]
                            weights = [45, 40, 10, 5] # Focado em atacar, raramente defende

                        chosen_action = random.choices(actions, weights, k=1)[0]

                    # Executa a ação escolhida.
                    print(f"IA ({self.opponent.name}) escolheu: {chosen_action}") 
                    
                    if chosen_action == "defend":
                        if not self.opponent.is_defending: self.opponent.defend()
                        self.perform_action("defend", self.opponent, self.player)
                    elif chosen_action == "heal":
                        self.opponent.heal()
                        self.perform_action("heal", self.opponent, self.player)
                    else: # Se a ação for "physical" ou "magic"
                        self.perform_action(chosen_action, self.opponent, self.player)
                        
            elif not self.is_player_turn:
                    self.is_player_turn = True
                    self.turn_text = self.font.render("Seu Turno", True, (255, 255, 255))

        if not self.game_over:
            if self.player.is_dead():
                self.end_game("Você Perdeu!", (255, 0, 0), player_won=False)
            elif self.opponent.is_dead():
                self.end_game("Você Venceu!", (0, 255, 0), player_won=True)
        
        self.clock.tick(60)
    
    def end_game(self, message, color, player_won):
        self.game_over = True
        self.winner_text = self.font.render(message, True, color)
        self.player_won = player_won
        self.end_time = pygame.time.get_ticks() + 2000

        # ... (código normal do update: self.player.update(), etc.)
        self.player.update()
        self.opponent.update()
        self.action_box.update(pygame.mouse.get_pos())

        if self.is_action_in_progress:
            if pygame.time.get_ticks() - self.action_delay_start >= 800:
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
                self.end_game("Você Perdeu!", (255, 0, 0), player_won=False)
            elif self.opponent.is_dead():
                self.end_game("Você Venceu!", (0, 255, 0), player_won=True)
        
        self.clock.tick(60)
    
    def end_game(self, message, color, player_won):
        self.game_over = True
        self.winner_text = self.font.render(message, True, color)
        self.player_won = player_won # <-- MUDANÇA: Usamos a flag em vez de checar a cor
        self.end_time = pygame.time.get_ticks() + 2000

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        self.player.draw(screen, self.player_pos)
        self.opponent.draw(screen, self.opponent_pos)

        self.player_health_bar.draw(screen)
        self.opponent_health_bar.draw(screen)
        screen.blit(self.player_text, (self.player_pos[0], self.player_pos[1] - 80))
        screen.blit(self.opponent_text, (self.opponent_pos[0], self.opponent_pos[1] - 80))

        if self.is_player_turn and not self.game_over and not self.is_action_in_progress:
            self.action_box.draw(screen)
        
        if self.game_over and self.winner_text:
            text_rect = self.winner_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
            screen.blit(self.winner_text, text_rect)
        elif not self.game_over:
            screen.blit(self.turn_text, (self.screen_width // 2 - 100, 50))