# Game/entities/character.py
import pygame
from Game.ui.animations import Animation

class Character:
    def __init__(self, name, data, is_flipped=False):
        self.name = name
        self.stats = data['stats']
        self.max_health = 100
        self.current_health = self.max_health
        self.is_flipped = is_flipped
        self.is_defending = False
        
        # Carrega todas as animações do personagem
        self.animations = self._load_animations(data['animations'])
        self.current_animation = self.animations['idle']

    def _load_animations(self, animation_paths):
        animations = {}
        for key, paths in animation_paths.items():
            # A classe Animation já lida com o carregamento das imagens
            animations[key] = Animation(paths, frame_duration=0.25, scale_size=(200, 200), flip_x=self.is_flipped)
        return animations

    def set_action(self, action_type):
        """Muda a animação atual e a reinicia."""
        if action_type in self.animations:
            self.current_animation = self.animations[action_type]
            self.current_animation.reset()
        else:
            # Se uma animação de ação não existir, volta para idle
            self.current_animation = self.animations['idle']

    def take_damage(self, amount):
        damage_taken = amount
        if self.is_defending:
            defense_value = self.stats.get("defense", 0)
            damage_taken = max(0, amount - defense_value) # Garante que o dano não seja negativo
            print(f"{self.name} defendeu {defense_value} de dano!")
            self.is_defending = False # A defesa é consumida após um ataque

        self.current_health = max(0, self.current_health - damage_taken)
        print(f"{self.name} tomou {damage_taken} de dano, vida restante: {self.current_health}")

    def defend(self):
        self.is_defending = True
        print(f"{self.name} está se preparando para defender.")

    def heal(self): 
        heal_amount = self.stats.get("heal", 0)
        self.current_health = min(self.max_health, self.current_health + heal_amount)
        print(f"{self.name} se curou em {heal_amount}, vida atual: {self.current_health}")

    def get_damage(self, attack_type):
        return self.stats.get(attack_type, 0)
    
    def is_dead(self):
        return self.current_health <= 0

    def update(self):
        self.current_animation.update()

    def draw(self, screen, position):
        screen.blit(self.current_animation.get_current_frame(), position)