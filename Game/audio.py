import pygame

SOUNDS = {"attack": "public/Sons/ataque.wav", "hit": "public/Sons/dano.wav"}
MUSIC = "public/Sons/soundtrack.mp3"


class Audio:
    """Áudio tolerante a falha: sem dispositivo ou arquivo, vira no-op."""

    def __init__(self, music_volume: float = 0.3, sfx_volume: float = 0.6):
        self.muted = False
        self.enabled = False
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self.music_volume = music_volume
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            return
        for name, path in SOUNDS.items():
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(sfx_volume)
                self._sounds[name] = sound
            except (FileNotFoundError, pygame.error):
                pass

    def play(self, name: str) -> None:
        sound = self._sounds.get(name)
        if self.enabled and not self.muted and sound:
            sound.play()

    def start_music(self) -> None:
        if not self.enabled:
            return
        try:
            pygame.mixer.music.load(MUSIC)
            pygame.mixer.music.set_volume(0 if self.muted else self.music_volume)
            pygame.mixer.music.play(-1)
        except (FileNotFoundError, pygame.error):
            pass

    def toggle_mute(self) -> None:
        self.muted = not self.muted
        if self.enabled:
            pygame.mixer.music.set_volume(0 if self.muted else self.music_volume)
