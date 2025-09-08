import pygame
from Game.ui.button import Button
from Game.scenes.scenes import Scene


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)
        self.select_character = Button(300, 250, 200, 60, "Jogar", self.font, (200,200,200), (255,255,255))
        self.background = pygame.image.load("public/fundo.jpeg").convert()
        self.dark_overlay = pygame.Surface(self.background.get_size(), pygame.SRCALPHA)
        self.dark_overlay.fill((0, 0, 0, 180))  # 120 = nível de escuridão (0-255)
    
    def handle_events(self, events):
        for event in events:
            # Logica do botões
            if self.select_character.foi_clicado(event):
                from Game.scenes.characterSelectionScene import CharacterSelectionScene
                self.game.change_scene(CharacterSelectionScene(self.game))
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.select_character.checar_hover(mouse_pos)

    def draw(self, screen):
        screen.fill((50, 50, 50))
        screen.blit(self.background, (0, 0))   
        screen.blit(self.dark_overlay, (0, 0))               
        self.select_character.desenhar(screen)