import pygame


class Assets:
    """Carrega e faz cache de imagens e fontes. Nunca levanta por arquivo
    ausente: devolve um placeholder visível e registra em `missing`."""

    def __init__(self):
        self._images: dict[tuple, pygame.Surface] = {}
        self._fonts: dict[int, pygame.font.Font] = {}
        self.missing: set[str] = set()

    def font(self, size: int) -> pygame.font.Font:
        if size not in self._fonts:
            self._fonts[size] = pygame.font.SysFont(None, size)
        return self._fonts[size]

    def image(self, path: str, size: tuple[int, int] | None = None,
              flip_x: bool = False, alpha: bool = True) -> pygame.Surface:
        key = (path, size, flip_x, alpha)
        if key not in self._images:
            self._images[key] = self._load(path, size, flip_x, alpha)
        return self._images[key]

    def _load(self, path, size, flip_x, alpha) -> pygame.Surface:
        try:
            surf = pygame.image.load(path)
            surf = surf.convert_alpha() if alpha else surf.convert()
        except (FileNotFoundError, pygame.error):
            self.missing.add(path)
            surf = pygame.Surface(size or (64, 64), pygame.SRCALPHA)
            surf.fill((255, 0, 255, 140))
        if size:
            surf = pygame.transform.scale(surf, size)
        if flip_x:
            surf = pygame.transform.flip(surf, True, False)
        return surf
