import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)  # assets são carregados por caminho relativo (public/...)

import pytest  # noqa: E402


@pytest.fixture
def game():
    from Game.core import Game
    g = Game(seed=42, headless=True)
    yield g
    import pygame
    pygame.quit()
