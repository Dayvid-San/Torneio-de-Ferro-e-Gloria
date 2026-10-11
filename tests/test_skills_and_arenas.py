import random

import pytest

from Game.data.arenas import ARENAS
from Game.domain.actions import ActionType, Side
from Game.domain.ai import HeuristicPolicy
from Game.domain.arena import Arena
from Game.domain.battle import Battle, IllegalAction
from Game.domain.effects import EffectKind
from Game.domain.fighter import Assassin, Knight, Mage
from Game.domain.tournament import Tournament
from tests.test_battle import FixedRng


def battle(a, b, arena=None, rng=0.99, **kw):
    kw = dict(kw, rng=FixedRng(rng))
    if arena is not None:
        kw["arena"] = arena
    return Battle(a, b, **kw)


# --- habilidades ---------------------------------------------------------
def test_furtive_strike_is_guaranteed_crit_and_ignores_defense():
    b = battle(Assassin(), Knight())  # rng alto: crítico normal jamais ocorreria
    e = b.act(ActionType.SKILL)
    assert e.crit and e.skill == "Golpe Furtivo"
    assert e.damage == 38  # 25 x1.5 = 38 (arredondado), sem subtrair a defesa 8


def test_shield_stance_deals_no_damage_and_raises_defense_for_two_enemy_turns():
    knight = Knight()
    b = battle(knight, Assassin())
    e = b.act(ActionType.SKILL)
    assert e.damage == 0 and not e.crit and e.effects == ("Escudo",)
    assert knight.defense_against(ActionType.PHYSICAL) == 8 + 6
    b.act(ActionType.PHYSICAL)            # 1º turno do oponente sob escudo: 25 - 14 = 11
    assert b.history[-1].damage == 11
    b.act(ActionType.PHYSICAL)            # turno do cavaleiro (escudo ainda ativo)
    b.act(ActionType.PHYSICAL)            # 2º turno do oponente: ainda protegido
    assert b.history[-1].damage == 11
    b.act(ActionType.PHYSICAL)            # cavaleiro age; escudo expira ao fim deste turno
    assert not knight.has_effect(EffectKind.DEFENSE_UP)
    b.act(ActionType.PHYSICAL)
    assert b.history[-1].damage == 25 - 8


def test_toxic_bolt_poisons_and_poison_ticks_on_holder_turns_only():
    mage, knight = Mage(), Knight()
    b = battle(mage, knight)
    e = b.act(ActionType.SKILL)
    assert e.effects == ("Veneno",) and e.mana_spent == 10
    assert knight.has_effect(EffectKind.POISON)
    hp = knight.hp
    e2 = b.act(ActionType.PHYSICAL)       # turno do cavaleiro: sofre 5 de veneno ao fim
    assert e2.self_damage == 5 and knight.hp == hp - 5
    for _ in range(4):                    # mago, cavaleiro, mago, cavaleiro
        b.act(ActionType.PHYSICAL)
    assert not knight.has_effect(EffectKind.POISON)  # durou 3 turnos do portador


def test_poison_can_kill_the_poisoned_fighter():
    mage, knight = Mage(), Knight()
    b = battle(mage, knight)
    b.act(ActionType.SKILL)
    knight.take_damage(knight.hp - 3)
    b.act(ActionType.PHYSICAL)
    assert b.is_over and b.winner is Side.PLAYER


def test_skill_cooldown_blocks_three_own_turns_then_returns():
    b = battle(Assassin(), Knight())
    assert ActionType.SKILL in b.legal_actions(Side.PLAYER)
    b.act(ActionType.SKILL)
    for _ in range(3):
        b.act(ActionType.PHYSICAL)  # oponente
        assert ActionType.SKILL not in b.legal_actions(Side.PLAYER)
        with pytest.raises(IllegalAction):
            b.act(ActionType.SKILL)
        b.act(ActionType.PHYSICAL)  # jogador
    b.act(ActionType.PHYSICAL)      # oponente
    assert ActionType.SKILL in b.legal_actions(Side.PLAYER)


def test_heuristic_policy_always_legal_and_deterministic_per_seed():
    def run(seed):
        rng = random.Random(seed)
        b = Battle(Mage(), Knight(), policy=HeuristicPolicy(rng), rng=rng)
        while not b.is_over:
            b.act()
            assert b.turn_number < 200
        return b.history
    assert run(3) == run(3)


# --- arenas --------------------------------------------------------------
def test_arena_physical_and_magic_multipliers():
    arena = Arena("t", "t", "t", physical_mult=1.5, magic_mult=0.5)
    b = battle(Knight(), Mage(), arena)
    assert b.act(ActionType.PHYSICAL).damage == 45 - 1  # 30 x1.5 - defesa 1
    assert b.act(ActionType.MAGIC).damage == round(35 * 0.5) - 2


def test_arena_crit_bonus_changes_crit_threshold():
    cripta = Arena("t", "t", "t", crit_bonus=0.5)
    base = battle(Knight(), Mage(), rng=0.45)      # chance 10% -> sem crítico
    assert not base.act(ActionType.PHYSICAL).crit
    boosted = battle(Knight(), Mage(), cripta, rng=0.45)  # chance 60% -> crítico
    assert boosted.act(ActionType.PHYSICAL).crit


def test_arena_mana_regen_bonus():
    arena = Arena("t", "t", "t", mana_regen_bonus=5)
    b = battle(Mage(), Knight(), arena)
    e = b.act(ActionType.MAGIC)
    assert e.actor_mana == 30 - 15 + 8 + 5


def test_arena_catalog_is_valid():
    assert len(ARENAS) >= 4
    for aid, a in ARENAS.items():
        assert aid == a.id and a.description and a.effects_summary


def test_tournament_assigns_an_arena_per_round_without_early_repeats():
    t = Tournament("mago", ["assassino", "cavaleiro", "mago"], random.Random(2), list(ARENAS))
    assert len(t.arenas) == t.total_rounds == 2
    assert t.arenas[0] != t.arenas[1] and set(t.arenas) <= set(ARENAS)
    assert t.current_arena == t.arenas[0]
    t.record(True)
    assert t.current_arena == t.arenas[1]


# --- novos personagens ---------------------------------------------------
def test_piercing_arrow_ignores_defense_without_crit():
    from Game.domain.fighter import Archer
    b = battle(Archer(), Knight())
    e = b.act(ActionType.SKILL)
    assert e.damage == round(26 * 1.3) and not e.crit and e.skill == "Flecha Perfurante"


def test_healing_light_heals_capped_and_costs_mana():
    from Game.domain.fighter import Cleric
    cleric = Cleric()
    cleric.take_damage(40)
    b = battle(cleric, Knight())
    e = b.act(ActionType.SKILL)
    assert e.healed == 30 and cleric.hp == 90 and e.damage == 0 and e.mana_spent == 12
    assert cleric.heal(999) == 10 and cleric.hp == cleric.max_hp  # nunca passa do máximo


def test_blood_rage_raises_only_physical_power_for_three_turns():
    from Game.domain.fighter import Barbarian
    barb = Barbarian()
    assert barb.max_hp == 110
    b = battle(barb, Knight(max_hp=1000))
    b.act(ActionType.SKILL)
    assert barb.power(ActionType.PHYSICAL) == 32 + barb.skill.self_effects[0].amount
    assert barb.power(ActionType.MAGIC) == 5
    for _ in range(6):  # 3 turnos do bárbaro (e 3 do oponente): o buff expira
        b.act(ActionType.PHYSICAL)
    assert not barb.has_effect(EffectKind.ATTACK_UP)
    assert barb.power(ActionType.PHYSICAL) == 32


def test_skill_should_use_heuristics():
    from Game.domain.fighter import Barbarian, Cleric
    cleric = Cleric()
    assert not cleric.skill.should_use(cleric)      # vida cheia: não cura
    cleric.take_damage(60)
    assert cleric.skill.should_use(cleric)
    barb = Barbarian()
    assert barb.skill.should_use(barb)
    barb.add_effect(barb.skill.self_effects[0])
    assert not barb.skill.should_use(barb)          # buff já ativo
