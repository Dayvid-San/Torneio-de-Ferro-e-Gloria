"""Guardas estruturais: pegam regressões de arquitetura e assets quebrados."""
import ast
from pathlib import Path

from Game.data.characters import CHARACTERS, SPRITE_KIND

ROOT = Path(__file__).resolve().parent.parent


def test_domain_does_not_import_pygame():
    for path in (ROOT / "Game" / "domain").glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            assert not any(n.split(".")[0] in {"pygame"} or n.startswith("Game.scenes")
                           or n.startswith("Game.ui") for n in names), f"{path.name} importa UI"


def test_every_character_asset_exists():
    for c in CHARACTERS.values():
        assert (ROOT / c.icon).exists(), c.icon
        for kind in SPRITE_KIND.values():
            for p in c.sprite_paths(kind):
                assert (ROOT / p).exists(), p


def test_character_ids_unique_and_creatable():
    for cid, c in CHARACTERS.items():
        assert cid == c.id and c.create().is_alive
