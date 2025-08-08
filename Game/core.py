import pygame
from Game.scenes.menu import MenuScene


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = MenuScene(self)

    def trocar_cena(self, nova_cena):
        self.current_scene = nova_cena

    def run(self):
        while self.running:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False

            self.current_scene.handle_events(events)
            self.current_scene.update()
            self.current_scene.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
