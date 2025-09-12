from Game.ui.animations import Animation
import random

class Character:
    def __init__(self, name, data, is_flipped=False):
        self.__name = name
        self.__stats = data['stats']
        self.__max_health = 100
        self.__current_health = self.__max_health
        self.__is_flipped = is_flipped
        self.__is_defending = False
        
        # Carrega todas as animações do personagem
        self.__animations = self._load_animations(data['animations'])
        self.__current_animation = self.__animations['idle']

    def _load_animations(self, animation_paths):
        animations = {}
        for key, paths in animation_paths.items():
            animations[key] = Animation(paths, frame_duration=0.25, scale_size=(200, 200), flip_x=self.__is_flipped)
        return animations

    def get_name(self):
        """Retorna o nome do personagem."""
        return self.__name

    def get_current_health(self):
        """Retorna a vida atual do personagem."""
        return self.__current_health

    def get_max_health(self):
        """Retorna a vida máxima do personagem."""
        return self.__max_health

    def get_is_defending(self):
        """Retorna se o personagem está defendendo."""
        return self.__is_defending

    def set_action(self, action_type):
        """Muda a animação atual e a reinicia."""
        if action_type in self.__animations:
            self.__current_animation = self.__animations[action_type]
            self.__current_animation.reset()
        else:
            self.__current_animation = self.__animations['idle']
       
    def take_damage(self, amount):
        damage_taken = amount
        
        if self.__is_defending:
            block_chance = self.__stats.get("perfect_block_chance", 0)
            if random.random() < block_chance:
                print(f"BLOQUEIO PERFEITO! {self.__name} não sofreu dano!")
                damage_taken = 0
            else:
                defense_value = self.__stats.get("defense", 0)
                damage_taken = max(0, amount - defense_value)
                print(f"{self.__name} defendeu {defense_value} de dano!")
            
            self.__is_defending = False
        
        self.__current_health = max(0, self.__current_health - damage_taken)
        print(f"{self.__name} tomou {damage_taken} de dano, vida restante: {self.__current_health}")

    def defend(self):
        self.__is_defending = True
        print(f"{self.__name} está se preparando para defender.")

    def heal(self): 
        heal_amount = self.__stats.get("heal", 0)
        self.__current_health = min(self.__max_health, self.__current_health + heal_amount)
        print(f"{self.__name} se curou em {heal_amount}, vida atual: {self.__current_health}")

    def get_damage(self, attack_type):
        return self.__stats.get(attack_type, 0)
    
    def is_dead(self):
        return self.__current_health <= 0

    def update(self):
        self.__current_animation.update()

    def draw(self, screen, position):
        screen.blit(self.__current_animation.get_current_frame(), position)