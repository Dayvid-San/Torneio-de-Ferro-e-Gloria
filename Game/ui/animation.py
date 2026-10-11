import pygame


class Animation:
    """Sequência de frames avançada por delta time (segundos)."""

    def __init__(self, frames: list[pygame.Surface], frame_duration: float = 0.25):
        if not frames:
            raise ValueError("Animation precisa de ao menos um frame")
        self.frames = frames
        self.frame_duration = frame_duration
        self.index = 0
        self._elapsed = 0.0

    def update(self, dt: float) -> None:
        if len(self.frames) <= 1:
            return
        self._elapsed += dt
        while self._elapsed >= self.frame_duration:
            self._elapsed -= self.frame_duration
            self.index = (self.index + 1) % len(self.frames)

    @property
    def frame(self) -> pygame.Surface:
        return self.frames[self.index]

    def reset(self) -> None:
        self.index = 0
        self._elapsed = 0.0
