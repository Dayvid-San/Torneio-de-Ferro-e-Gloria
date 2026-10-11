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
    game.selected_character_id = "mago"
    for name, kwargs in (("menu", {}), ("character_select", {}), ("gameplay", {}),
                         ("result", dict(won=True, turns=5, opponent_id="cavaleiro"))):
        game.go_to(name, **kwargs)
        run(game, 0.5)
    assert not game.assets.missing, game.assets.missing


def play_fight(game, action=ActionType.PHYSICAL):
    scene = game.scene
    assert type(scene).__name__ == "GameplayScene"
    for _ in range(50):
        if scene.battle.is_over:
            break
        if scene.phase == "input":
            game.step(click(scene.buttons[action].rect.center), DT)
        run(game, 1.0)
    assert scene.battle.is_over
    run(game, 2.5)  # tempo de EndDelay -> tela de resultado


def start_tournament(game, char="cavaleiro"):
    run(game, 0.1)
    game.step(click(game.scene.buttons["torneio"].rect.center), DT)
    assert type(game.scene).__name__ == "CharacterSelectScene"
    game.step(click(game.scene.buttons[char].rect.center), DT)


def test_tournament_flow_ends_in_result_with_next_action(game, monkeypatch):
    start_tournament(game)
    scene = game.scene
    assert game.tournament is not None and scene.round_label == f"Rodada 1/{game.tournament.total_rounds}"
    assert scene.defs[Side.PLAYER].id == "cavaleiro"
    assert scene.defs[Side.OPPONENT].id == game.tournament.opponents[0]

    # força vitória do jogador para o teste não depender de sorte
    foe = scene.battle.fighter(Side.OPPONENT)
    foe.take_damage(foe.hp - 1)
    play_fight(game)
    result = game.scene
    assert type(result).__name__ == "ResultScene" and result.won
    assert "next" in result.actions and game.tournament.round_number == 2

    game.step(click(result.actions["next"].rect.center), DT)
    assert game.scene.round_label == f"Rodada 2/{game.tournament.total_rounds}"
    assert game.scene.defs[Side.OPPONENT].id == game.tournament.opponents[1]


def test_tournament_loss_offers_new_tournament_then_menu(game):
    start_tournament(game)
    me = game.scene.battle.fighter(Side.PLAYER)
    me.take_damage(me.hp - 1)
    game.scene.battle.turn_side = Side.OPPONENT  # oponente golpeia primeiro
    run(game, 1.0)
    game.scene.perform()
    run(game, 5.0)
    result = game.scene
    assert type(result).__name__ == "ResultScene" and not result.won
    assert game.tournament.eliminated and "new" in result.actions
    game.step(click(result.actions["menu"].rect.center), DT)
    assert type(game.scene).__name__ == "MenuScene"


def test_quick_duel_has_rematch_and_no_tournament(game):
    run(game, 0.1)
    game.step(click(game.scene.buttons["duelo"].rect.center), DT)
    game.step(click(game.scene.buttons["mago"].rect.center), DT)
    assert game.tournament is None and game.scene.round_label == "Duelo Rápido"
    foe = game.scene.battle.fighter(Side.OPPONENT)
    foe.take_damage(foe.hp - 1)
    play_fight(game)
    assert "rematch" in game.scene.actions
    game.step(click(game.scene.actions["rematch"].rect.center), DT)
    assert type(game.scene).__name__ == "GameplayScene"


def test_menu_quit_stops_game(game):
    run(game, 0.1)
    game.step(click(game.scene.buttons["sair"].rect.center), DT)
    assert not game.running


def test_hotkeys_and_disabled_magic(game):
    game.selected_character_id = "mago"
    game.go_to("gameplay")
    scene = game.scene
    game.step([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_2)], DT)
    assert scene.last_event.action is ActionType.MAGIC
    run(game, 1.0)  # oponente joga e devolve a vez
    me = scene.battle.fighter(Side.PLAYER)
    me.spend_mana(me.mana)
    hp = scene.battle.fighter(Side.OPPONENT).hp
    game.step([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_2)], DT)
    assert scene.battle.fighter(Side.OPPONENT).hp == hp  # sem mana: ignorado


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


def test_skill_button_and_hotkey_use_class_skill_then_enter_cooldown(game):
    game.selected_character_id = "assassino"
    game.go_to("gameplay", arena_id="lamina")
    scene = game.scene
    run(game, 0.1)
    assert scene.arena.id == "lamina" and "Golpe Furtivo" in scene._skill_label
    game.step([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_3)], DT)
    assert scene.last_event.skill == "Golpe Furtivo" and scene.last_event.crit
    run(game, 2.0)  # ação do jogador (0,8s) + do oponente (0,8s) e a vez volta
    assert scene.phase == "input"
    assert not scene.buttons[ActionType.SKILL].enabled and "(" in scene._skill_label


def test_arena_and_tournament_arena_are_used_by_gameplay(game):
    start_tournament(game)
    assert game.scene.arena.id == game.tournament.current_arena
