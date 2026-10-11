import random
from typing import Protocol

from Game.domain.actions import ActionType


class Policy(Protocol):
    def choose(self, battle, side) -> ActionType: ...


class RandomPolicy:
    """Escolhe ao acaso entre as ações que a mana permite."""

    def __init__(self, rng: random.Random | None = None):
        self.rng = rng or random.Random()

    def choose(self, battle, side) -> ActionType:
        return self.rng.choice(battle.legal_actions(side))


def _estimate(me, foe, action) -> int:
    if action is ActionType.SKILL:
        return me.skill.estimate_damage(me, foe)
    return me.power(action) - foe.defense_against(action)


class GreedyPolicy:
    """Sempre usa a ação de maior dano líquido (já descontada a defesa do alvo),
    ignorando custo de mana futuro. Baseline de pior caso para balanceamento."""

    def choose(self, battle, side) -> ActionType:
        me, foe = battle.fighter(side), battle.fighter(side.other)
        return max(battle.legal_actions(side), key=lambda a: _estimate(me, foe, a))


class HeuristicPolicy:
    """IA do oponente no jogo: usa a habilidade quando faz sentido (escudo com
    vida baixa), poupa mana da magia e erra de propósito com chance `randomness`."""

    def __init__(self, rng: random.Random | None = None, randomness: float = 0.25):
        self.rng = rng or random.Random()
        self.randomness = randomness

    def choose(self, battle, side) -> ActionType:
        legal = battle.legal_actions(side)
        if self.rng.random() < self.randomness:
            return self.rng.choice(legal)
        me, foe = battle.fighter(side), battle.fighter(side.other)
        skill = me.skill
        if ActionType.SKILL in legal and skill:
            if skill.damage_action is None:  # habilidade defensiva
                if me.hp <= 0.6 * me.max_hp and not me.effects:
                    return ActionType.SKILL
            else:
                return ActionType.SKILL
        pool = [a for a in legal if a is not ActionType.SKILL]
        return max(pool, key=lambda a: _estimate(me, foe, a))
