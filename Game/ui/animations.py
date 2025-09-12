import pygame

class Animation:
    def __init__(self, image_paths, frame_duration=0.1, scale_size=(100, 100), flip_x=False):
        self.__frames = []
        self.__frame_duration = frame_duration * 1000  #
        self.__frame_index = 0
        self.__last_frame_time = pygame.time.get_ticks()
        self.__scale_size = scale_size
        self.__playing = True
        self.__flip_x = flip_x

        if not image_paths:
            print("Lista de caminhos vazia. Usando placeholder.")
            self._create_placeholder()
            return

        for i, path in enumerate(image_paths):
            try:
                frame = pygame.image.load(path).convert_alpha()
                frame = pygame.transform.scale(frame, self.__scale_size)
                if self.__flip_x:
                    frame = pygame.transform.flip(frame, True, False) 
                self.__frames.append(frame)
            except (FileNotFoundError, pygame.error) as e:
                print(f"Erro ao carregar frame {i+1} ({path}): {e}. Usando placeholder.")
                self._create_placeholder_frame()
        if not self.__frames:
            print(f"Nenhum frame carregado de {image_paths}. Usando placeholder.")
            self._create_placeholder()

    def _create_placeholder(self):
        frame = pygame.Surface(self.__scale_size)
        frame.fill((100, 100, 100))
        pygame.draw.rect(frame, (255, 0, 0), (0, 0, self.__scale_size[0], 10))
        if self.__flip_x:
            frame = pygame.transform.flip(frame, True, False)
        self.__frames = [frame]

    def _create_placeholder_frame(self):
        frame = pygame.Surface(self.__scale_size)
        frame.fill((150, 150, 150))
        if self.__flip_x:
            frame = pygame.transform.flip(frame, True, False)
        self.__frames.append(frame)

    def update(self):
        if not self.__playing or len(self.__frames) <= 1:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.__last_frame_time >= self.__frame_duration:
            self.__frame_index = (self.__frame_index + 1) % len(self.__frames)
            self.__last_frame_time = current_time

    def get_current_frame(self):
        if not self.__frames:
            frame = pygame.Surface(self.__scale_size)
            frame.fill((255, 0, 0))
            if self.__flip_x:
                frame = pygame.transform.flip(frame, True, False)
            return frame
        return self.__frames[self.__frame_index]

    def reset(self):
        self.__frame_index = 0
        self.__last_frame_time = pygame.time.get_ticks()

    def set_frames(self, new_paths, reset_index=True):
        self.__init__(new_paths, self.__frame_duration / 1000, self.__scale_size, self.__flip_x)
        if reset_index:
            self.reset()

    def pause(self, paused=True):
        self.__playing = not paused