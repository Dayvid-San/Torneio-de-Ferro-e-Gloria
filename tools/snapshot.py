"""Gera PNGs de cada cena em modo headless (revisão visual sem abrir janela).

    python -m tools.snapshot [pasta_saida]     # padrão: snapshots/
"""
import sys
from pathlib import Path

import pygame

from Game.core import Game
from Game.domain.actions import ActionType
from Game.domain.tournament import Tournament

DT = 1 / 60


def advance(game, seconds):
    for _ in range(int(seconds / DT)):
        game.step([], DT)


def main(out="snapshots"):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    game = Game(seed=1, headless=True)

    def shot(name):
        pygame.image.save(game.screen, str(out / f"{name}.png"))
        print("salvo", out / f"{name}.png")

    advance(game, 0.2); shot("menu")

    game.go_to("character_select")
    scene = game.scene  # mouse virtual não funciona no driver dummy: força o hover
    scene.buttons["mago"].hovered = True
    scene._description = scene._describe("mago")
    scene.draw(game.screen); shot("character_select")

    game.selected_character_id = "mago"
    game.tournament = Tournament("mago", ["assassino", "cavaleiro", "mago"], game.rng)
    game.go_to("gameplay"); advance(game, 0.2); shot("gameplay_inicio")
    game.scene.perform(ActionType.MAGIC); advance(game, 0.3); shot("gameplay_ataque")

    game.tournament.record(True)
    game.go_to("result", won=True, turns=7, opponent_id="cavaleiro")
    advance(game, 0.2); shot("resultado")
    pygame.quit()
    if game.assets.missing:
        print("ASSETS AUSENTES:", sorted(game.assets.missing))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:2]))
