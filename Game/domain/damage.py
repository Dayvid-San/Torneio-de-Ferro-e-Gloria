from typing import Callable

from Game.domain.actions import ActionType
from Game.domain.fighter import Fighter

# Gancho de extensão: arenas, eventos aleatórios, buffs e passivas entram aqui
# como funções (attacker, defender, action, power) -> power, aplicadas antes
# da defesa.
DamageModifier = Callable[[Fighter, Fighter, ActionType, int], int]

CRIT_MULTIPLIER = 1.5
MIN_DAMAGE = 1


def calculate_damage(attacker: Fighter, defender: Fighter, action: ActionType,
                     modifiers: tuple[DamageModifier, ...] = (), crit: bool = False) -> int:
    """poder (x crítico) -> modificadores -> menos defesa do alvo (mínimo 1)."""
    power = attacker.power(action)
    if crit:
        power = round(power * CRIT_MULTIPLIER)
    for modifier in modifiers:
        power = modifier(attacker, defender, action, power)
    return max(MIN_DAMAGE, power - defender.defense_against(action))
