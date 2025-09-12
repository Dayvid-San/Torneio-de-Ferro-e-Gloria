import pygame
from Game.ui.button import Button
from Game.scenes.scenes import Scene
from Game.scenes.characterSelectionScene import CharacterSelectionScene

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.__title = self.font.render("Torneio de Ferro e Sangue", True, (225, 165, 0))  # Gold color
        self.__select_character_button = Button(
            self._screen_width // 2 - 100, 250, 200, 60, "Modo Normal",
            self.font, (200, 200, 200), (255, 255, 255)
        )
        self.__tower_mode_button = Button(
            self._screen_width // 2 - 100, 350, 200, 60, "Modo Torre",
            self.font, (200, 200, 200), (255, 255, 255)
        )
        self.__load_background()
        self.start_transition(500)  # Fade-in for 500ms
        self.log("MenuScene initialized")  # Debug log

    def __load_background(self):
        """Load and scale background image with fallback."""
        try:
            self.__background = pygame.image.load("public/torneio_ferro_e_sangue.png").convert()
            self.__background = pygame.transform.scale(self.__background, (self._screen_width, self._screen_height))
            self.__dark_overlay = pygame.Surface((self._screen_width, self._screen_height), pygame.SRCALPHA)
            self.__dark_overlay.fill((0, 0, 0, 180))  # Semi-transparent overlay
        except FileNotFoundError:
            self.log("Background 'public/torneio_ferro_e_sangue.png' not found. Using gray fallback.")
            self.__background = pygame.Surface((self._screen_width, self._screen_height))
            self.__background.fill((50, 50, 50))
            self.__dark_overlay = pygame.Surface((self._screen_width, self._screen_height), pygame.SRCALPHA)
            self.__dark_overlay.fill((0, 0, 0, 180))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.__select_character_button.foi_clicado(event):
                    self.log("Modo Normal selected")
                    self.game.is_in_tower_mode = False
                    self.game.change_scene(CharacterSelectionScene(self.game))
                elif self.__tower_mode_button.foi_clicado(event):
                    self.log("Modo Torre selected")
                    self.game.is_in_tower_mode = True
                    self.game.current_tower_floor = 0
                    self.game.change_scene(CharacterSelectionScene(self.game))

    def update(self):
        self.update_transition()  # Update fade-in
        mouse_pos = pygame.mouse.get_pos()
        self.__select_character_button.checar_hover(mouse_pos)
        self.__tower_mode_button.checar_hover(mouse_pos)

    def draw(self, screen):
        screen.blit(self.__background, (0, 0))
        if hasattr(self, '__dark_overlay'):
            screen.blit(self.__dark_overlay, (0, 0))
        title_x = self._screen_width // 2 - self.__title.get_width() // 2
        screen.blit(self.__title, (title_x, 100))
        self.__select_character_button.desenhar(screen)
        self.__tower_mode_button.desenhar(screen)
        self.draw_transition(screen)  # Apply fade-in