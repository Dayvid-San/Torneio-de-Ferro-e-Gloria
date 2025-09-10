import pygame

class Animation:
    def __init__(self, image_paths, frame_duration=0.1, scale_size=(100, 100)):
        """Inicializa a animação com uma lista de caminhos de imagens.
        
        Args:
            image_paths (list): Lista de caminhos para as imagens dos quadros.
            frame_duration (float): Tempo por quadro em segundos (ex.: 0.1 para 10 FPS).
            scale_size (tuple): Tamanho para escalar os quadros (ex.: (100, 100)).
        """
        self.frames = []
        self.frame_duration = frame_duration
        self.frame_index = 0
        self.last_frame_time = pygame.time.get_ticks() / 1000.0
        self.scale_size = scale_size

        # Carregar quadros com fallback
        try:
            for path in image_paths:
                frame = pygame.image.load(path).convert_alpha()
                frame = pygame.transform.scale(frame, scale_size)
                self.frames.append(frame)
        except FileNotFoundError:
            print(f"Imagens de animação {image_paths} não encontradas. Usando placeholder.")
            frame = pygame.Surface(scale_size)
            frame.fill((100, 100, 100))  # Placeholder cinza
            self.frames = [frame]

        # Garantir que haja pelo menos um quadro
        if not self.frames:
            frame = pygame.Surface(scale_size)
            frame.fill((100, 100, 100))
            self.frames = [frame]

    def update(self):
        """Atualiza o quadro atual com base no tempo."""
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.last_frame_time >= self.frame_duration:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_frame_time = current_time

    def get_current_frame(self):
        """Retorna o quadro atual da animação."""
        return self.frames[self.frame_index]