from dataclasses import dataclass
from enum import Enum


class EffectKind(str, Enum):
    DEFENSE_UP = "defense_up"  # soma ao valor das duas defesas
    POISON = "poison"          # dano por turno do portador, ignora defesa
    ATTACK_UP = "attack_up"    # soma ao poder do ataque físico


@dataclass(frozen=True)
class Effect:
    """Modelo imutável de um efeito de status (parte da definição de uma Skill)."""
    kind: EffectKind
    amount: int
    duration: int  # quantos turnos do portador o efeito dura
    name: str


class ActiveEffect:
    """Efeito em andamento sobre um lutador. Reaplicar o mesmo tipo renova."""

    def __init__(self, effect: Effect):
        self.effect = effect
        self.remaining = effect.duration

    @property
    def kind(self) -> EffectKind:
        return self.effect.kind

    @property
    def label(self) -> str:
        return f"{self.effect.name}({self.remaining})"
