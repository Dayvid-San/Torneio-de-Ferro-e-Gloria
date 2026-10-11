from typing import Callable

from Game.domain.actions import ActionType
from Game.domain.fighter import Fighter

# Gancho de extensão: arenas, eventos aleatórios, buffs e passivas entram aqui
# como funções (attacker, defender, action, damage) -> damage.
DamageModifier = Callable[[Fighter, Fighter, ActionType, int], int]


def calculate_damage(attacker: Fighter, defender: Fighter, action: ActionType,
                     modifiers: tuple[DamageModifier, ...] = ()) -> int:
    damage = attacker.power(action)
    for modifier in modifiers:
        damage = modifier(attacker, defender, action, damage)
    return max(0, damage)
