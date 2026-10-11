import random

import pytest

from Game.domain.actions import ActionType, Side
from Game.domain.ai import GreedyPolicy, RandomPolicy
from Game.domain.battle import Battle, BattleOver, IllegalAction
from Game.domain.fighter import Assassin, Knight, Mage


def test_player_acts_first_and_turns_alternate():
    b = Battle(Knight(), Mage(), policy=GreedyPolicy())
    assert b.turn_side is Side.PLAYER
    e1 = b.act(ActionType.PHYSICAL)
    assert (e1.actor, e1.damage, e1.target_hp) == (Side.PLAYER, 29, 71)
    assert b.turn_side is Side.OPPONENT
    e2 = b.act(ActionType.MAGIC)
    assert (e2.actor, e2.action, e2.damage) == (Side.OPPONENT, ActionType.MAGIC, 33)


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
    b = Battle(Knight(), Mage(), modifiers=(double,), rng=FixedRng(0.99))
    assert b.act(ActionType.PHYSICAL).damage == 59  # 60 - defesa 1


def test_same_seed_same_fight():
    def run(seed):
        rng = random.Random(seed)
        b = Battle(Assassin(), Mage(), policy=RandomPolicy(rng), rng=rng)
        while not b.is_over:
            b.act(ActionType.PHYSICAL) if b.turn_side is Side.PLAYER else b.act()
        return b.history
    assert run(7) == run(7)


class FixedRng(random.Random):
    def __init__(self, value):
        super().__init__(0)
        self.value = value

    def random(self):
        return self.value


def test_crit_multiplies_power_before_defense():
    # Cavaleiro 30 x1.5 = 45, menos defesa física 1 do Mago
    b = Battle(Knight(), Mage(), rng=FixedRng(0.0))
    e = b.act(ActionType.PHYSICAL)
    assert e.crit and e.damage == 44


def test_no_crit_when_roll_is_high():
    b = Battle(Knight(), Mage(), rng=FixedRng(0.99))
    e = b.act(ActionType.PHYSICAL)
    assert not e.crit and e.damage == 29


def test_defense_reduces_damage_with_minimum_one():
    weak = Mage()
    weak.physical = 1
    b = Battle(weak, Knight(), rng=FixedRng(0.99))
    assert b.act(ActionType.PHYSICAL).damage == 1


def test_magic_spends_mana_and_regens():
    b = Battle(Mage(), Knight(), rng=FixedRng(0.99))
    e = b.act(ActionType.MAGIC)
    assert e.mana_spent == 15 and e.actor_mana == 30 - 15 + 8


def test_illegal_magic_without_mana_raises_and_policies_avoid_it():
    mage = Mage()
    mage.spend_mana(mage.mana)
    b = Battle(mage, Knight(), rng=FixedRng(0.99))
    with pytest.raises(IllegalAction):
        b.act(ActionType.MAGIC)
    assert b.history == []
    for policy in (GreedyPolicy(), RandomPolicy(random.Random(1))):
        assert policy.choose(b, Side.PLAYER) is ActionType.PHYSICAL
