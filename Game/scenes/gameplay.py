import pygame
from Game.scenes.scene_base import Scene  # Com Game.
from Game.scenes.menu import MenuScene  # Com Game.


class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.playerPos = [100, 100]
        self.speed = 5

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene(MenuScene(self.game))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.playerPos[0] -= self.speed
        if keys[pygame.K_RIGHT]:
            self.playerPos[0] += self.speed
        if keys[pygame.K_UP]:
            self.playerPos[1] -= self.speed
        if keys[pygame.K_DOWN]:
            self.playerPos[1] += self.speed

    def draw(self, screen):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (*self.playerPos, 50, 50))