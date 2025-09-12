import pygame
from abc import ABC, abstractmethod

class Scene(ABC):
    def __init__(self, game):
        if game is None or not hasattr(game, 'screen'):
            raise ValueError("Scene requer um objeto game com atributo screen.")
        self._game = game
        self._screen = game.screen  
        self._clock = pygame.time.Clock()  
        self._font = pygame.font.SysFont(None, 40) 
        self._screen_width, self._screen_height = self._screen.get_size()  
        self._transition_alpha = 0  
        self._is_transitioning = False 
        self._debug_mode = False 

    def game(self):
        return self._game

    def screen(self):
        return self._screen

    def font(self):
        return self._font

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def start_transition(self, duration=500):
        self._is_transitioning = True
        self._transition_alpha = 255  # Começa opaco
        self._transition_duration = duration
        self._transition_start = pygame.time.get_ticks()

    def update_transition(self):
        if not self._is_transitioning:
            return
        elapsed = pygame.time.get_ticks() - self._transition_start
        if elapsed >= self._transition_duration:
            self._is_transitioning = False
            self._transition_alpha = 0
        else:
            self._transition_alpha = int(255 * (1 - elapsed / self._transition_duration))

    def draw_transition(self, screen):
        if self._is_transitioning:
            transition_surface = pygame.Surface((self._screen_width, self._screen_height))
            transition_surface.fill((0, 0, 0))
            transition_surface.set_alpha(self._transition_alpha)
            screen.blit(transition_surface, (0, 0))

    def pause(self):
        pass

    def resume(self):
        pass

    def toggle_debug(self):
        self._debug_mode = not self._debug_mode
        print(f"Debug mode {'ativado' if self._debug_mode else 'desativado'} para {self.__class__.__name__}")

    def log(self, message):
        if self._debug_mode:
            print(f"[DEBUG {self.__class__.__name__}]: {message}")