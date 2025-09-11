import pygame
from Game.ui.button import Button
from Game.scenes.scenes import Scene
from Game.scenes.gameplay import GameplayScene
from Game.scenes.menu import MenuScene


class CharacterSelectionScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)
        self.font2 = pygame.font.SysFont(None, 30)
        self.title = self.font.render("Selecione o Lutador", True, (255, 255, 255))

        # Carregar imagem de fundo
        try:
            self.background = pygame.image.load("public/fundo.jpeg").convert()
            screen_size = self.game.screen.get_size()
            self.background = pygame.transform.scale(self.background, screen_size)
        except FileNotFoundError:
            print("Fundo não encontrado. Usando preto.")
            screen_size = self.game.screen.get_size()
            self.background = pygame.Surface(screen_size)
            self.background.fill((0, 0, 0))

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
            "Assassino": "Henrique, naufrago nas praias do condado e capturado roubando uma lorde, esse estrangeiro foi tomado como prisioneiro e agora luta por sua liberdade, na arena.",
            "Cavaleiro": "Sula, o fracassado e desertor na batalha dos sete exércitos. Sula busca o perdão prometido em vitória na arena.",
            "Mago": "Arnabin, um velho sábio (ou louco) do novo continente. Ele se diverte com seus experimentos em humanos e procura se entreter na arena."
        }
        self.selected_character = None  # Personagem em hover ou selecionado
        self.description_text = None  # Texto da descrição a ser renderizado


    def render_text_wrapped(self, text, font, color, max_width):
            """
            Renderiza um texto quebrando em múltiplas linhas se passar do max_width.
            Retorna uma lista de superfícies (cada uma é uma linha renderizada).
            """
            words = text.split(" ")
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)

            return [font.render(line, True, color) for line in lines]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Voltar ao menu
                    self.game.change_scene(MenuScene(self.game))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.char1_button.foi_clicado(event):
                    self.game.selected_character = "Assassino"  # Salvar personagem selecionado
                    self.game.change_scene(GameplayScene(self.game))
                if self.char2_button.foi_clicado(event):
                    self.game.selected_character = "Cavaleiro"
                    self.game.change_scene(GameplayScene(self.game))
                if self.char3_button.foi_clicado(event):
                    self.game.selected_character = "Mago"
                    self.game.change_scene(GameplayScene(self.game))

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.char1_button.checar_hover(mouse_pos)
        self.char2_button.checar_hover(mouse_pos)
        self.char3_button.checar_hover(mouse_pos)

        # Atualizar descrição com base no hover
        if self.char1_button.hovered:
            self.selected_character = "Assassino"

            self.description_text = self.render_text_wrapped(
                self.descriptions["Assassino"], self.font2, (255, 255, 255), max_width=400
            )
            
        elif self.char2_button.hovered:
            self.selected_character = "Cavaleiro"
            self.description_text = self.render_text_wrapped(
                self.descriptions["Cavaleiro"], self.font2, (255, 255, 255), max_width=400
            )
        elif self.char3_button.hovered:
            self.selected_character = "Mago"
            self.description_text = self.render_text_wrapped(
                self.descriptions["Mago"], self.font2, (255, 255, 255), max_width=400
            )
        else:
            self.selected_character = None
            self.description_text = None

    def draw_text_box(self, screen, lines, x, y, padding=10):
        # calcula largura e altura do box
        width = max(line.get_width() for line in lines) + 2 * padding
        height = len(lines) * self.font2.get_linesize() + 2 * padding

        # cria uma surface transparente
        box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, 150))  # preto com 150 de alpha

        # desenha a caixa
        screen.blit(box_surface, (x, y))

        # desenha o texto dentro
        offset_y = padding
        for line in lines:
            screen.blit(line, (x + padding, y + offset_y))
            offset_y += self.font2.get_linesize()



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
            if self.char1_button.hovered:
                self.draw_text_box(screen, self.description_text, 320, 200)

            if self.char2_button.hovered:
                self.draw_text_box(screen, self.description_text, 320, 300)

            if self.char3_button.hovered:
                self.draw_text_box(screen, self.description_text, 320, 400)