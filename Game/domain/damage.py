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
                     modifiers: tuple[DamageModifier, ...] = (), crit: bool = False,
                     skill=None) -> int:
    """poder (x crítico) -> modificadores -> menos defesa do alvo (mínimo 1).

    Com `skill`, o tipo de dano, o multiplicador de poder e o `ignore_defense`
    vêm dela; `action` é ignorado.
    """
    if skill is not None:
        action = skill.damage_action
        power = round(attacker.power(action) * skill.power_mult)
    else:
        power = attacker.power(action)
    if crit:
        power = round(power * CRIT_MULTIPLIER)
    for modifier in modifiers:
        power = modifier(attacker, defender, action, power)
    defense = 0 if skill is not None and skill.ignore_defense else defender.defense_against(action)
    return max(MIN_DAMAGE, power - defense)
