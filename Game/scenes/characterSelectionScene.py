import pygame
from Game.ui.button import Button
from Game.scenes.scenes import Scene


class CharacterSelectionScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)
        self.title = self.font.render("Seleção de Personagens", True, (255, 255, 255))

        # Carregar imagem de fundo
        self.background = pygame.image.load("public/fundo.jpeg").convert()

        # Botões dos personagens (seletores)
        self.char1_button = Button(150, 200, 150, 50, "Assassino", self.font, (200, 200, 200), (255, 255, 255))
        self.char2_button = Button(150, 300, 150, 50, "Cavaleiro", self.font, (200, 200, 200), (255, 255, 255))
        self.char3_button = Button(150, 400, 150, 50, "Mago", self.font, (200, 200, 200), (255, 255, 255))

        # Imagens dos personagens (à esquerda dos botões)
        self.char1_image = pygame.image.load("public/IconesJogo/assassino.jpeg").convert_alpha()
        self.char2_image = pygame.image.load("public/IconesJogo/cavaleiro.jpeg").convert_alpha()
        self.char3_image = pygame.image.load("public/IconesJogo/mago.jpeg").convert_alpha()

        # Escalar imagens para um tamanho uniforme (ex.: 80x80 pixels)
        self.char1_image = pygame.transform.scale(self.char1_image, (80, 80))
        self.char2_image = pygame.transform.scale(self.char2_image, (80, 80))
        self.char3_image = pygame.transform.scale(self.char3_image, (80, 80))

        # Descrições dos personagens
        self.descriptions = {
            "Assassino": "Um assassino ágil com precisão mortal e ataques à distância.",
            "Cavaleiro": "Um guerreiro valente com força bruta e habilidades de combate corpo a corpo.",
            "Mago": "Um mago sábio que domina feitiços de fogo e gelo."
        }
        self.selected_character = None  # Personagem em hover ou selecionado
        self.description_text = None  # Texto da descrição a ser renderizado

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Voltar ao menu
                    from Game.scenes.menu import MenuScene
                    self.game.change_scene(MenuScene(self.game))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.char1_button.foi_clicado(event):
                    self.game.selected_character = "Assassino"  # Salvar personagem selecionado
                    from Game.scenes.gameplay import GameplayScene
                    self.game.change_scene(GameplayScene(self.game))
                if self.char2_button.foi_clicado(event):
                    self.game.selected_character = "Cavaleiro"
                    from Game.scenes.gameplay import GameplayScene
                    self.game.change_scene(GameplayScene(self.game))
                if self.char3_button.foi_clicado(event):
                    self.game.selected_character = "Mago"
                    from Game.scenes.gameplay import GameplayScene
                    self.game.change_scene(GameplayScene(self.game))

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.char1_button.checar_hover(mouse_pos)
        self.char2_button.checar_hover(mouse_pos)
        self.char3_button.checar_hover(mouse_pos)

        # Atualizar descrição com base no hover
        if self.char1_button.hovered:
            self.selected_character = "Assassino"
            self.description_text = self.font.render(self.descriptions["Assassino"], True, (255, 255, 255))
        elif self.char2_button.hovered:
            self.selected_character = "Cavaleiro"
            self.description_text = self.font.render(self.descriptions["Cavaleiro"], True, (255, 255, 255))
        elif self.char3_button.hovered:
            self.selected_character = "Mago"
            self.description_text = self.font.render(self.descriptions["Mago"], True, (255, 255, 255))
        else:
            self.selected_character = None
            self.description_text = None

    def draw(self, screen):
        # Desenhar fundo
        screen.blit(self.background, (0, 0))

        # Desenhar título
        screen.blit(self.title, (200, 100))

        # Desenhar imagens dos personagens (à esquerda dos botões)
        screen.blit(self.char1_image, (50, 200))  # Alinhado com o botão 1
        screen.blit(self.char2_image, (50, 300))  # Alinhado com o botão 2
        screen.blit(self.char3_image, (50, 400))  # Alinhado com o botão 3

        # Desenhar botões dos personagens
        self.char1_button.desenhar(screen)
        self.char2_button.desenhar(screen)
        self.char3_button.desenhar(screen)

        # Desenhar descrição do personagem em hover (à direita)
        if self.description_text:
            screen.blit(self.description_text, (350, 200))