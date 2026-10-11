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


class GreedyPolicy:
    """Sempre usa a ação de maior dano líquido (já descontada a defesa do alvo),
    ignorando custo de mana futuro. Baseline de pior caso para balanceamento."""

    def choose(self, battle, side) -> ActionType:
        me, foe = battle.fighter(side), battle.fighter(side.other)
        return max(battle.legal_actions(side),
                   key=lambda a: me.power(a) - foe.defense_against(a))
