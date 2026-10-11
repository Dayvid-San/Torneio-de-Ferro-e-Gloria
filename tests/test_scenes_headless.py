"""Fluxo completo do jogo em modo headless: menu -> seleção -> luta -> menu."""
import pygame

from Game.domain.actions import ActionType, Side

DT = 1 / 60


def click(pos):
    return [pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos),
            pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=pos)]


def run(game, seconds, events=()):
    game.step(list(events), DT)
    for _ in range(int(seconds / DT)):
        game.step([], DT)


def test_every_scene_draws_without_missing_assets(game):
    for name in ("menu", "character_select", "gameplay"):
        game.go_to(name)
        run(game, 0.5)
    assert not game.assets.missing, game.assets.missing


def test_full_flow_menu_to_victory_and_back(game):
    run(game, 0.1)
    game.step(click(game.scene.play_button.rect.center), DT)
    assert type(game.scene).__name__ == "CharacterSelectScene"

    game.step(click(game.scene.buttons["cavaleiro"].rect.center), DT)
    scene = game.scene
    assert type(scene).__name__ == "GameplayScene"
    assert scene.defs[Side.PLAYER].id == "cavaleiro"
    assert scene.defs[Side.OPPONENT].id != "cavaleiro"

    for _ in range(50):
        if scene.battle.is_over:
            break
        if scene.phase == "input":
            game.step(click(scene.buttons[ActionType.PHYSICAL].rect.center), DT)
        run(game, 1.0)
    assert scene.battle.is_over

    run(game, 2.5)
    assert type(game.scene).__name__ == "MenuScene"


def test_buttons_ignored_while_opponent_acts(game):
    game.selected_character_id = "mago"
    game.go_to("gameplay")
    scene = game.scene
    game.step(click(scene.buttons[ActionType.MAGIC].rect.center), DT)
    assert scene.phase == "acting"
    hp_before = scene.battle.fighter(Side.OPPONENT).hp
    game.step(click(scene.buttons[ActionType.MAGIC].rect.center), DT)
    assert scene.battle.fighter(Side.OPPONENT).hp == hp_before


def test_escape_returns_to_menu(game):
    game.selected_character_id = "mago"
    game.go_to("gameplay")
    game.step([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)], DT)
    assert type(game.scene).__name__ == "MenuScene"
