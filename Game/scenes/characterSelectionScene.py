import pygame
from Game.ui.button import Button
from Game.scenes.scenes import Scene
from Game.scenes.gameplay import GameplayScene
from Game.scenes.menu import MenuScene

# Importar as novas classes
from Game.utills.characterData import CharacterData
from Game.managers.characterManager import CharacterSelectionManager
from Game.utills.textRenderer import TextRenderer



class CharacterSelectionScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)
        self.font2 = pygame.font.SysFont(None, 30)
        self.title = self.font.render("Selecione o Lutador", True, (255, 255, 255))

        # Carregar fundo
        self.load_background()
        
        # Instanciar o manager de personagens
        self.character_manager = CharacterSelectionManager()
        self.character_manager.load_images(size=(80, 80))

        # Criar os botões dinamicamente
        self.buttons = {}
        for i, char in enumerate(self.character_manager.characters):
            button = Button(150, 200 + i * 100, 150, 50, char.name, self.font, (200, 200, 200), (255, 255, 255))
            self.buttons[char.name] = button

        self.selected_character = None
        self.description_text = None

    def load_background(self):
        try:
            self.background = pygame.image.load("public/fundo.jpeg").convert()
            screen_size = self.game.screen.get_size()
            self.background = pygame.transform.scale(self.background, screen_size)
        except FileNotFoundError:
            print("Fundo não encontrado. Usando preto.")
            self.background = pygame.Surface(self.game.screen.get_size())
            self.background.fill((0, 0, 0))

    def render_text_wrapped(self, text, font, color, max_width):
        # Usa a classe utilitária
        return TextRenderer.render_wrapped(text, font, color, max_width)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene(MenuScene(self.game))
            
            # Checa o clique para cada botão, como no seu código original
            for name, button in self.buttons.items():
                if button.foi_clicado(event):
                    self.game.selected_character = name
                    self.game.change_scene(GameplayScene(self.game))
                    return # Sai do loop para evitar múltiplas transições

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        hovered_char_name = None
        
        # Checa o hover para todos os botões
        for name, button in self.buttons.items():
            button.checar_hover(mouse_pos)
            if button.hovered:
                hovered_char_name = name
        
        # Atualiza a descrição apenas se houver um novo personagem em hover
        if hovered_char_name and self.selected_character != hovered_char_name:
            self.selected_character = hovered_char_name
            char_data = self.character_manager.get_character_data(hovered_char_name)
            self.description_text = self.render_text_wrapped(
                char_data.description, self.font2, (255, 255, 255), max_width=400
            )
        elif not hovered_char_name:
            self.selected_character = None
            self.description_text = None

    def draw_text_box(self, screen, lines, x, y, padding=10):
        width = max(line.get_width() for line in lines) + 2 * padding
        height = len(lines) * self.font2.get_linesize() + 2 * padding
        box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, 150))
        screen.blit(box_surface, (x, y))
        offset_y = padding
        for line in lines:
            screen.blit(line, (x + padding, y + offset_y))
            offset_y += self.font2.get_linesize()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.title, (200, 100))

        for name, button in self.buttons.items():
            char_data = self.character_manager.get_character_data(name)
            
            # Desenha a imagem e o botão
            screen.blit(char_data.image, (button.rect.x - 100, button.rect.y))
            button.desenhar(screen)

            # Desenha a caixa de texto se o botão estiver em hover
            if button.hovered and self.description_text:
                self.draw_text_box(screen, self.description_text, button.rect.x + button.rect.width + 20, button.rect.y)