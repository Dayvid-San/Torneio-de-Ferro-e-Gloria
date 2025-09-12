import pygame
import random
from Game.ui.button import Button
from Game.scenes.scenes import Scene
from Game.scenes.menu import MenuScene
from config import ARENA_GROUND_Y, CHARACTER_HEIGHT
from Game.data.tower_data import TOWER_NORMAL
from Game.data.character_data import CHARACTER_DATA
from Game.scenes.character import Character
from Game.ui.health_bar import HealthBar
from Game.ui.action_box import ActionBox

class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # --- CONFIGURAÇÃO INICIAL ---
        self.__font = pygame.font.SysFont(None, 40)
        self.__big_font = pygame.font.SysFont(None, 74)
        self.__screen_width, self.__screen_height = self.game.screen.get_size()
        self.__clock = pygame.time.Clock()

        # Carregar fundo
        self.__background = pygame.image.load("public/fundo.jpeg").convert()
        self.__background = pygame.transform.scale(self.__background, (self.__screen_width, self.__screen_height))
        
        # --- LÓGICA DE CRIAÇÃO DOS PERSONAGENS ---
        available_chars = list(CHARACTER_DATA.keys())
        player_name = self.game.selected_character or random.choice(available_chars)
        
        if self.game.is_in_tower_mode:
            floor = self.game.current_tower_floor
            if floor < len(TOWER_NORMAL):
                opponent_name = TOWER_NORMAL[floor]
            else:
                opponent_name = random.choice([name for name in available_chars if name != player_name])
        else:
            available_opponents = [name for name in available_chars if name != player_name]
            opponent_name = random.choice(available_opponents)

        self.__player = Character(player_name, CHARACTER_DATA[player_name])
        self.__opponent = Character(opponent_name, CHARACTER_DATA[opponent_name], is_flipped=True)
        
        # --- CONFIGURAÇÃO DA INTERFACE (UI) ---
        player_x = self.__screen_width // 4 - 100
        opponent_x = 3 * self.__screen_width // 4 - 100
        char_y = ARENA_GROUND_Y - CHARACTER_HEIGHT
        
        self.__player_pos = (player_x, char_y)
        self.__opponent_pos = (opponent_x, char_y)
        
        self.__player_health_bar = HealthBar(player_x, char_y - 50, 200, 20, self.__player)
        self.__opponent_health_bar = HealthBar(opponent_x, char_y - 50, 200, 20, self.__opponent)

        self.__player_text = self.__font.render(self.__player.get_name(), True, (255, 255, 255))
        self.__opponent_text = self.__font.render(self.__opponent.get_name(), True, (255, 255, 255))

        action_box_y = self.__screen_height - 100
        options = ["ATK", "SPELL", "DEF", "HEAL"]
        self.__action_box = ActionBox(
            x=50, 
            y=action_box_y, 
            width=self.__screen_width - 100, 
            height=80, 
            options=options, 
            font=self.__font
        )
        # --- CONTROLE DE ESTADO DA CENA ---
        self.__is_player_turn = True
        self.__turn_text = self.__font.render("Seu Turno", True, (255, 255, 255))
        self.__is_action_in_progress = False
        self.__pending_opponent = False
        self.__last_attacker = None
        self.__game_over = False
        self.__winner_text = None
        self.__player_won = False
        self.__tower_cleared = False

    def handle_events(self, events):
        if self.__game_over: return
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene(MenuScene(self.game))

            if self.__is_player_turn and not self.__is_action_in_progress:
                selected_action = self.__action_box.handle_click(event)
                if selected_action:
                    if selected_action == "ATK":
                        self.perform_action("physical", self.__player, self.__opponent)
                        self.end_player_turn()
                    elif selected_action == "SPELL":
                        self.perform_action("magic", self.__player, self.__opponent)
                        self.end_player_turn()
                    elif selected_action == "DEF": 
                        self.__player.defend()
                        self.perform_action("defend", self.__player, self.__opponent)
                    elif selected_action == "HEAL": 
                        self.__player.heal()
                        self.perform_action("heal", self.__player, self.__opponent)
                    self.end_player_turn()

    def perform_action(self, action_type, attacker, target):
        self.__last_attacker = attacker
        attacker.set_action(action_type)

        if action_type in ["physical", "magic"]:
            damage = attacker.get_damage(action_type)
            target.take_damage(damage)

        self.__is_action_in_progress = True
        self.__action_delay_start = pygame.time.get_ticks()

    def end_player_turn(self):
        self.__pending_opponent = True
        self.__is_player_turn = False
        self.__turn_text = self.__font.render("Turno do Oponente", True, (255, 255, 255))

    def update(self):
        if self.__game_over:
            if pygame.time.get_ticks() > self.__end_time:
                if self.__tower_cleared:
                    self.game.change_scene(MenuScene(self.game))
                    return

                if self.__player_won and self.game.is_in_tower_mode:
                    self.game.current_tower_floor += 1
                    
                    if self.game.current_tower_floor < len(TOWER_NORMAL):
                        self.game.change_scene(GameplayScene(self.game))
                    else:
                        self.__tower_cleared = True
                        self.__winner_text = self.__big_font.render("TORRE CONQUISTADA!", True, (255, 215, 0))
                        self.__end_time = pygame.time.get_ticks() + 4000
                else:
                    self.game.change_scene(MenuScene(self.game))
            return 

        self.__player.update()
        self.__opponent.update()
        self.__action_box.update(pygame.mouse.get_pos())

        if self.__is_action_in_progress:
            if pygame.time.get_ticks() - self.__action_delay_start >= 800:
                self.__last_attacker.set_action('idle')
                self.__is_action_in_progress = False
                if self.__pending_opponent:
                    self.__pending_opponent = False
                    
                    chosen_action = None
                    
                    if self.__opponent.get_current_health() < self.__opponent.get_max_health() * 0.35:
                        if random.random() < 0.8:
                            chosen_action = "heal"

                    if not chosen_action:
                        actions = []
                        weights = []
                        
                        if "Mago" in self.__opponent.get_name() or "Aprendiz" in self.__opponent.get_name():
                            actions = ["magic", "heal", "defend", "physical"]
                            weights = [65, 20, 10, 5]
                        
                        elif "Cavaleiro" in self.__opponent.get_name() or "Guarda" in self.__opponent.get_name():
                            actions = ["physical", "defend", "magic", "heal"]
                            weights = [55, 30, 10, 5]
                        
                        else:
                            actions = ["physical", "magic", "heal", "defend"]
                            weights = [45, 40, 10, 5]

                        chosen_action = random.choices(actions, weights, k=1)[0]

                    print(f"IA ({self.__opponent.get_name()}) escolheu: {chosen_action}")
                    
                    if chosen_action == "defend":
                        if not self.__opponent.get_is_defending():
                            self.__opponent.defend()
                        self.perform_action("defend", self.__opponent, self.__player)
                    elif chosen_action == "heal":
                        self.__opponent.heal()
                        self.perform_action("heal", self.__opponent, self.__player)
                    else:
                        self.perform_action(chosen_action, self.__opponent, self.__player)
                        
            elif not self.__is_player_turn:
                self.__is_player_turn = True
                self.__turn_text = self.__font.render("Seu Turno", True, (255, 255, 255))

        if not self.__game_over:
            if self.__player.is_dead():
                self.end_game("Você Perdeu!", (255, 0, 0), player_won=False)
            elif self.__opponent.is_dead():
                self.end_game("Você Venceu!", (0, 255, 0), player_won=True)
        
        self.__clock.tick(60)

    def end_game(self, message, color, player_won):
        self.__game_over = True
        self.__winner_text = self.__font.render(message, True, color)
        self.__player_won = player_won
        self.__end_time = pygame.time.get_ticks() + 2000

    def draw(self, screen):
        screen.blit(self.__background, (0, 0))

        self.__player.draw(screen, self.__player_pos)
        self.__opponent.draw(screen, self.__opponent_pos)

        self.__player_health_bar.draw(screen)
        self.__opponent_health_bar.draw(screen)
        screen.blit(self.__player_text, (self.__player_pos[0], self.__player_pos[1] - 80))
        screen.blit(self.__opponent_text, (self.__opponent_pos[0], self.__opponent_pos[1] - 80))

        if self.__is_player_turn and not self.__game_over and not self.__is_action_in_progress:
            self.__action_box.draw(screen)
        
        if self.__game_over and self.__winner_text:
            text_rect = self.__winner_text.get_rect(center=(self.__screen_width / 2, self.__screen_height / 2))
            screen.blit(self.__winner_text, text_rect)
        elif not self.__game_over:
            screen.blit(self.__turn_text, (self.__screen_width // 2 - 100, 50))