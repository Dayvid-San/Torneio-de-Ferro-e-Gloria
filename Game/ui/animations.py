import pygame
class Animation:
    def __init__(self, image_paths, frame_duration=0.1, scale_size=(100, 100)):
        self.frames = []
        self.frame_duration = frame_duration
        self.frame_index = 0
        self.last_frame_time = pygame.time.get_ticks() / 1000.0
        self.scale_size = scale_size
        self.player_attack_animation = self.load_character_animation(self.player_character, action="attack")
        self.current_player_animation = self.player_animation


    def perform_action(self, action, attacker, target):
        if attacker == self.player_character:
            self.current_player_animation = self.player_attack_animation
            # Resetar para idle após 1 segundo
            self.reset_animation_time = pygame.time.get_ticks() + 1000
        try:
            for path in image_paths:
                frame = pygame.image.load(path).convert_alpha()
                frame = pygame.transform.scale(frame, scale_size)
                self.frames.append(frame)
        except FileNotFoundError:
            print(f"Imagens de animação {image_paths} não encontradas. Usando placeholder.")
            frame = pygame.Surface(scale_size)
            frame.fill((100, 100, 100))
            self.frames = [frame]
        if not self.frames:
            frame = pygame.Surface(scale_size)
            frame.fill((100, 100, 100))
            self.frames = [frame]
    def update(self):
        self.player_animation.update()
        self.opponent_animation.update()
        if hasattr(self, 'reset_animation_time') and pygame.time.get_ticks() > self.reset_animation_time:
            self.current_player_animation = self.player_animation
    def get_current_frame(self):
        return self.frames[self.frame_index]


    def draw(self, screen):
    # ... substituir player_animation por current_player_animation ...
        screen.blit(self.current_player_animation.get_current_frame(), (150, 300))