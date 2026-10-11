"""Registro de cenas. Cenas se referenciam por nome (`game.go_to("menu")`),
o que elimina imports circulares entre elas. Import é preguiçoso."""
import importlib

_REGISTRY = {
    "menu": ("Game.scenes.menu", "MenuScene"),
    "character_select": ("Game.scenes.character_select", "CharacterSelectScene"),
    "gameplay": ("Game.scenes.gameplay", "GameplayScene"),
}


def create_scene(name: str, game, **kwargs):
    module_name, class_name = _REGISTRY[name]
    cls = getattr(importlib.import_module(module_name), class_name)
    return cls(game, **kwargs)


SCENE_NAMES = tuple(_REGISTRY)
