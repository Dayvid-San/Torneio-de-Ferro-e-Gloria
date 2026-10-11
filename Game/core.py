import os
import random

import pygame

from Game import config
from Game.assets import Assets
from Game.scenes import create_scene


class Game:
    """Dono da janela, do loop e da cena atual. `step()` avança um quadro e é
    o ponto de entrada tanto do loop real quanto dos testes headless."""

    def __init__(self, seed: int | None = None, headless: bool = False):
        if headless:
            os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
            os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()
        self.assets = Assets()
        self.rng = random.Random(seed)
        self.running = True
        self.selected_character_id: str | None = None
        self.scene = None
        self.go_to("menu")

    def go_to(self, scene_name: str, **kwargs) -> None:
        self.scene = create_scene(scene_name, self, **kwargs)

    def step(self, events, dt: float) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        self.scene.handle_events(events)
        self.scene.update(dt)
        self.scene.draw(self.screen)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000
            self.step(pygame.event.get(), dt)
            pygame.display.flip()
        pygame.quit()
