import random
from typing import Protocol

from Game.domain.actions import ActionType


class Policy(Protocol):
    def choose(self, battle, side) -> ActionType: ...


class RandomPolicy:
    """Comportamento original do oponente: escolhe ao acaso."""

    def __init__(self, rng: random.Random | None = None):
        self.rng = rng or random.Random()

    def choose(self, battle, side) -> ActionType:
        return self.rng.choice(list(ActionType))


class GreedyPolicy:
    """Sempre usa o ataque mais forte. Útil como baseline de balanceamento."""

    def choose(self, battle, side) -> ActionType:
        me = battle.fighter(side)
        return max(ActionType, key=me.power)
