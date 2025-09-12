import pygame
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Torneio de Ferro e Sangue")
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_in_tower_mode = False
        self.current_tower_floor = 0
        from Game.scenes.menu import MenuScene  # Com Game
        self.currentScene = MenuScene(self)
       

    def change_scene(self, new_scene):
        self.currentScene = new_scene

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.currentScene.handle_events(events)
            self.currentScene.update()
            self.currentScene.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()