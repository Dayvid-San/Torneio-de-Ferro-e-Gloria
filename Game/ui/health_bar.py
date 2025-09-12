# Game/ui/health_bar.py
import pygame

class HealthBar:
    """Uma barra de vida que se desenha e atualiza com base em um personagem."""
    def __init__(self, x, y, width, height, character):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.character = character # Referência ao personagem que a barra representa

        self.border_color = (255, 255, 255)
        self.background_color = (50, 50, 50)
        self.low_health_color = (255, 0, 0)
        self.high_health_color = (0, 255, 0)
    
    def draw(self, screen):
        """Desenha a barra de vida na tela."""
        # Calcula a porcentagem de vida
        health_ratio = self.character.current_health / self.character.max_health
        
        # Interpola a cor de verde para vermelho
        current_color = (
            self.low_health_color[0] + (self.high_health_color[0] - self.low_health_color[0]) * health_ratio,
            self.high_health_color[1] + (self.low_health_color[1] - self.high_health_color[1]) * (1 - health_ratio),
            0
        )
        
        # Desenha o fundo da barra
        pygame.draw.rect(screen, self.background_color, (self.x, self.y, self.width, self.height))
        
        # Desenha a vida atual
        if health_ratio > 0:
            pygame.draw.rect(screen, current_color, (self.x, self.y, self.width * health_ratio, self.height))
        
        # Desenha a borda
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 2)