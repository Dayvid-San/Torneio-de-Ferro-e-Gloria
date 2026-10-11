from dataclasses import dataclass

from Game.domain.actions import ActionType
from Game.domain.effects import Effect, EffectKind


@dataclass(frozen=True)
class Skill:
    """Habilidade única de uma classe. Totalmente declarativa: `Battle` sabe
    aplicar qualquer combinação destes campos, então novas habilidades não
    exigem código novo de combate."""
    name: str
    description: str
    mana_cost: int = 0
    cooldown: int = 0                       # turnos próprios de espera após usar
    damage_action: ActionType | None = None  # None = não causa dano
    power_mult: float = 1.0
    guaranteed_crit: bool = False
    ignore_defense: bool = False
    self_heal: int = 0                      # PV recuperados pelo usuário
    self_effects: tuple[Effect, ...] = ()
    target_effects: tuple[Effect, ...] = ()

    def estimate_damage(self, attacker, defender) -> int:
        """Estimativa para IAs: dano direto + dano total de veneno aplicado."""
        total = sum(e.amount * e.duration for e in self.target_effects
                    if e.kind is EffectKind.POISON)
        if self.damage_action is None:
            return total
        power = attacker.power(self.damage_action) * self.power_mult
        if self.guaranteed_crit:
            power *= 1.5
        defense = 0 if self.ignore_defense else defender.defense_against(self.damage_action)
        return max(1, round(power) - defense) + total


    def should_use(self, me) -> bool:
        """Heurística para IAs: vale gastar a habilidade agora?"""
        if self.damage_action is not None:
            return True
        if any(me.has_effect(e.kind) for e in self.self_effects):
            return False  # buff já ativo
        if self.self_heal:
            return me.max_hp - me.hp >= self.self_heal and me.hp <= 0.6 * me.max_hp
        if any(e.kind is EffectKind.DEFENSE_UP for e in self.self_effects):
            return me.hp <= 0.6 * me.max_hp
        return True


FURTIVE_STRIKE = Skill(
    "Golpe Furtivo", "Ataque físico crítico garantido que ignora a defesa do alvo.",
    cooldown=3, damage_action=ActionType.PHYSICAL, guaranteed_crit=True, ignore_defense=True)

SHIELD_STANCE = Skill(
    "Postura de Escudo", "Sem atacar, ganha +9 de defesa por 2 turnos do oponente.",
    cooldown=3, self_effects=(Effect(EffectKind.DEFENSE_UP, 9, 2, "Escudo"),))

TOXIC_BOLT = Skill(
    "Raio Tóxico", "Magia que envenena o alvo: 5 de dano por turno durante 3 turnos.",
    mana_cost=10, cooldown=3, damage_action=ActionType.MAGIC, power_mult=0.6,
    target_effects=(Effect(EffectKind.POISON, 5, 3, "Veneno"),))

PIERCING_ARROW = Skill(
    "Flecha Perfurante", "Disparo físico a 130% do poder que atravessa a defesa do alvo.",
    cooldown=2, damage_action=ActionType.PHYSICAL, power_mult=1.3, ignore_defense=True)

HEALING_LIGHT = Skill(
    "Luz Curativa", "Recupera 30 pontos de vida.",
    mana_cost=12, cooldown=3, self_heal=30)

BLOOD_RAGE = Skill(
    "Fúria", "Sem atacar, ganha +10 de poder físico por 3 turnos.",
    cooldown=4, self_effects=(Effect(EffectKind.ATTACK_UP, 10, 3, "Fúria"),))
