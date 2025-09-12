import pygame

class HealthBar:
    def __init__(self, x, y, width, height, character):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__character = character

    def draw(self, screen):
        # Calculate health ratio using getter methods
        health_ratio = self.__character.get_current_health() / self.__character.get_max_health()
        # Draw health bar
        pygame.draw.rect(screen, (255, 0, 0), (self.__x, self.__y, self.__width, self.__height))  # Background
        pygame.draw.rect(screen, (0, 255, 0), (self.__x, self.__y, self.__width * health_ratio, self.__height))  # Health