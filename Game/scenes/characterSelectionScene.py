# characterSelectionScene.py (VERSÃO FINAL)

import pygame
from Game.ui.button import Button
from Game.scenes.scenes import Scene
from Game.scenes.gameplay import GameplayScene
from Game.scenes.menu import MenuScene

# Importando nossos novos módulos e dados
from Game.data.character_data import CHARACTER_DATA
from Game.ui.text_box import TextBox

class CharacterSelectionScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)
        self.font2 = pygame.font.SysFont(None, 30)
        self.title = self.font.render("Selecione o Lutador", True, (255, 255, 255))

        # Carregar fundo
        try:
            self.background = pygame.image.load("public/fundo.jpeg").convert()
            screen_size = self.game.screen.get_size()
            self.background = pygame.transform.scale(self.background, screen_size)
        except FileNotFoundError:
            # ... (código de fallback)
            pass

        # --- LÓGICA DINÂMICA DE CRIAÇÃO ---
        self.character_widgets = []
        self.description_box = None
        
        start_y = 200
        y_increment = 100
        
        # Itera sobre os dados centralizados para criar os widgets dinamicamente
        for i, (char_name, char_data) in enumerate(CHARACTER_DATA.items()):
            y_pos = start_y + i * y_increment
            
            button = Button(150, y_pos, 150, 50, char_name, self.font, (200, 200, 200), (255, 255, 255))
            
            try:
                icon = pygame.image.load(char_data["icon_path"]).convert_alpha()
                icon = pygame.transform.scale(icon, (80, 80))
            except FileNotFoundError:
                icon = pygame.Surface((80, 80)) # Placeholder
            
            # Agrupa os widgets de cada personagem
            self.character_widgets.append({
                "name": char_name,
                "data": char_data,
                "button": button,
                "icon": icon,
                "pos_y": y_pos
            })
        # --- FIM DA LÓGICA DINÂMICA ---

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene(MenuScene(self.game))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Itera sobre os botões para verificar cliques
                for widget in self.character_widgets:
                    if widget["button"].foi_clicado(event):
                        self.game.selected_character = widget["name"]
                        self.game.change_scene(GameplayScene(self.game))
                        return # Sai do loop após a mudança de cena

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        
        hovered_char = None
        # Itera para checar hover e atualizar a caixa de descrição
        for widget in self.character_widgets:
            widget["button"].checar_hover(mouse_pos)
            if widget["button"].hovered:
                hovered_char = widget
        
        if hovered_char:
            self.description_box = TextBox(
                x=320,
                y=hovered_char["pos_y"],
                max_width=400,
                text=hovered_char["data"]["description"],
                font=self.font2
            )
        else:
            self.description_box = None

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.title, (200, 100))

        # Itera para desenhar todos os ícones e botões
        for widget in self.character_widgets:
            screen.blit(widget["icon"], (50, widget["pos_y"]))
            widget["button"].desenhar(screen)
        
        # Se houver uma caixa de descrição ativa, a desenha
        if self.description_box:
            self.description_box.draw(screen)