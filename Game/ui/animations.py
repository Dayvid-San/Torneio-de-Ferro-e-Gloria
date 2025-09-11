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
        self.frame_duration = frame_duration * 1000  # Converter para ms para precisão
        self.frame_index = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.scale_size = scale_size
        self.playing = True  # Flag para pausar animação se necessário

        # Carregar quadros com fallback por frame
        if not image_paths:
            print("Lista de caminhos vazia. Usando placeholder.")
            self._create_placeholder()
            return

        for i, path in enumerate(image_paths):
            try:
                frame = pygame.image.load(path).convert_alpha()
                frame = pygame.transform.scale(frame, scale_size)
                self.frames.append(frame)
            except (FileNotFoundError, pygame.error) as e:
                print(f"Erro ao carregar frame {i+1} ({path}): {e}. Usando placeholder para este frame.")
                self._create_placeholder_frame()
        # Se nenhum frame carregou, use placeholder
        if not self.frames:
            print(f"Nenhum frame carregado de {image_paths}. Usando placeholder completo.")
            self._create_placeholder()

    def _create_placeholder(self):
        """Cria um único frame placeholder para toda a animação."""
        frame = pygame.Surface(self.scale_size)
        frame.fill((100, 100, 100))  # Placeholder cinza
        pygame.draw.rect(frame, (255, 0, 0), (0, 0, self.scale_size[0], 10))  # Barra vermelha para debug
        self.frames = [frame]

    def _create_placeholder_frame(self):
        """Cria um frame placeholder individual."""
        frame = pygame.Surface(self.scale_size)
        frame.fill((150, 150, 150))  # Cinza mais claro para frames isolados
        self.frames.append(frame)

    def update(self):
        """Atualiza o quadro atual com base no tempo. Só atualiza se playing=True."""
        if not self.playing or len(self.frames) <= 1:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time >= self.frame_duration:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_frame_time = current_time

    def get_current_frame(self):
        """Retorna o quadro atual da animação."""
        if not self.frames:
            # Fallback final de emergência
            frame = pygame.Surface(self.scale_size)
            frame.fill((255, 0, 0))  # Vermelho para erro crítico
            return frame
        return self.frames[self.frame_index]

    def reset(self):
        """Reseta a animação para o primeiro frame (útil para ataques)."""
        self.frame_index = 0
        self.last_frame_time = pygame.time.get_ticks()

    def set_frames(self, new_paths, reset_index=True):
        """Troca os frames dinamicamente (ex: de idle para attack)."""
        self.__init__(new_paths, self.frame_duration / 1000, self.scale_size)  # Reinit com novos paths
        if reset_index:
            self.reset()

    def pause(self, paused=True):
        """Pausa/retoma a animação."""
        self.playing = not paused