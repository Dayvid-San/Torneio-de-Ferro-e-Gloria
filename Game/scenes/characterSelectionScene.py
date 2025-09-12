import pygame
from Game.ui.button import Button
from Game.scenes.scenes import Scene
from Game.scenes.gameplay import GameplayScene
from Game.scenes.menu import MenuScene
from Game.data.character_data import CHARACTER_DATA
from Game.ui.text_box import TextBox

class CharacterSelectionScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.__font = pygame.font.SysFont(None, 40)
        self.__font2 = pygame.font.SysFont(None, 30)
        self.__title = self.__font.render("Selecione o Lutador", True, (255, 255, 255))
        self.__character_widgets = []
        self.__description_box = None
        self.__background = self.__load_background()

        # Lógica dinâmica de criação
        start_y = 200
        y_increment = 100

        for i, (char_name, char_data) in enumerate(CHARACTER_DATA.items()):
            y_pos = start_y + i * y_increment
            button = Button(150, y_pos, 150, 50, char_name, self.__font, (200, 200, 200), (255, 255, 255))
            
            try:
                icon = pygame.image.load(char_data["icon_path"]).convert_alpha()
                icon = pygame.transform.scale(icon, (80, 80))
            except FileNotFoundError:
                icon = pygame.Surface((80, 80))  # Placeholder
            
            self.__character_widgets.append({
                "name": char_name,
                "data": char_data,
                "button": button,
                "icon": icon,
                "pos_y": y_pos
            })

    def __load_background(self):
        try:
            background = pygame.image.load("public/fundo.jpeg").convert()
            screen_size = self.game.screen.get_size()
            background = pygame.transform.scale(background, screen_size)
        except FileNotFoundError:
            print("Erro: Imagem 'public/fundo.jpeg' não encontrada")
            background = pygame.Surface(self.game.screen.get_size())
            background.fill((0, 0, 0))
        except pygame.error as e:
            print(f"Erro ao carregar/redimensionar imagem: {e}")
            background = pygame.Surface(self.game.screen.get_size())
            background.fill((0, 0, 0))
        return background

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene(MenuScene(self.game))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for widget in self.__character_widgets:
                    if widget["button"].foi_clicado(event):
                        self.game.selected_character = widget["name"]
                        self.game.change_scene(GameplayScene(self.game))
                        return

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        hovered_char = None
        for widget in self.__character_widgets:
            widget["button"].checar_hover(mouse_pos)
            if widget["button"].hovered:
                hovered_char = widget
        
        if hovered_char:
            self.__description_box = TextBox(
                x=320,
                y=hovered_char["pos_y"],
                max_width=400,
                text=hovered_char["data"]["description"],
                font=self.__font2
            )
        else:
            self.__description_box = None

    def draw(self, screen):
        screen.blit(self.__background, (0, 0))
        screen.blit(self.__title, (200, 100))
        for widget in self.__character_widgets:
            screen.blit(widget["icon"], (50, widget["pos_y"]))
            widget["button"].desenhar(screen)
        
        if self.__description_box:
            self.__description_box.draw(screen)