import random

import pytest

from Game.domain.actions import ActionType, Side
from Game.domain.ai import GreedyPolicy, RandomPolicy
from Game.domain.battle import Battle, BattleOver
from Game.domain.fighter import Assassin, Knight, Mage


def test_player_acts_first_and_turns_alternate():
    b = Battle(Knight(), Mage(), policy=GreedyPolicy())
    assert b.turn_side is Side.PLAYER
    e1 = b.act(ActionType.PHYSICAL)
    assert (e1.actor, e1.damage, e1.target_hp) == (Side.PLAYER, 30, 70)
    assert b.turn_side is Side.OPPONENT
    e2 = b.act()  # policy: Mage usa magia
    assert (e2.actor, e2.action, e2.damage) == (Side.OPPONENT, ActionType.MAGIC, 35)


def test_winner_and_no_actions_after_end():
    b = Battle(Knight(), Mage(), policy=GreedyPolicy())
    while not b.is_over:
        b.act(ActionType.PHYSICAL) if b.turn_side is Side.PLAYER else b.act()
    assert b.winner is not None
    assert b.history[-1].defeated
    with pytest.raises(BattleOver):
        b.act()


def test_always_terminates_and_hp_consistent():
    rng = random.Random(0)
    for _ in range(200):
        a, b = rng.choice([Assassin, Knight, Mage])(), rng.choice([Assassin, Knight, Mage])()
        battle = Battle(a, b, policy=RandomPolicy(rng))
        n = 0
        while not battle.is_over:
            battle.act(); n += 1
            assert n <= 100
        assert min(a.hp, b.hp) == 0


def test_modifiers_hook():
    double = lambda atk, dfn, act, dmg: dmg * 2  # noqa: E731
    b = Battle(Knight(), Mage(), modifiers=(double,))
    assert b.act(ActionType.PHYSICAL).damage == 60


def test_same_seed_same_fight():
    def run(seed):
        b = Battle(Assassin(), Mage(), policy=RandomPolicy(random.Random(seed)))
        while not b.is_over:
            b.act(ActionType.PHYSICAL) if b.turn_side is Side.PLAYER else b.act()
        return b.history
    assert run(7) == run(7)
