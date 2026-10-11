from dataclasses import dataclass

from Game.domain.actions import ActionType
from Game.domain.damage import DamageModifier


@dataclass(frozen=True)
class Arena:
    """Cenário de luta com efeitos ambientais, aplicados via `Battle`."""
    id: str
    name: str
    description: str
    physical_mult: float = 1.0
    magic_mult: float = 1.0
    crit_bonus: float = 0.0
    mana_regen_bonus: int = 0
    tint: tuple[int, int, int, int] = (0, 0, 0, 0)  # RGBA sobreposto ao fundo

    @property
    def modifiers(self) -> tuple[DamageModifier, ...]:
        if self.physical_mult == 1.0 and self.magic_mult == 1.0:
            return ()

        def scale(attacker, defender, action, power):
            mult = self.physical_mult if action is ActionType.PHYSICAL else self.magic_mult
            return round(power * mult)
        return (scale,)

    @property
    def effects_summary(self) -> str:
        parts = []
        if self.physical_mult != 1.0:
            parts.append(f"Físico {self.physical_mult - 1:+.0%}")
        if self.magic_mult != 1.0:
            parts.append(f"Magia {self.magic_mult - 1:+.0%}")
        if self.crit_bonus:
            parts.append(f"Crítico {self.crit_bonus:+.0%}")
        if self.mana_regen_bonus:
            parts.append(f"Mana {self.mana_regen_bonus:+d}/turno")
        return ", ".join(parts) or "Sem efeitos"


NEUTRAL_ARENA = Arena("coliseu", "Coliseu de Ferro", "Terreno neutro, sem surpresas.")
