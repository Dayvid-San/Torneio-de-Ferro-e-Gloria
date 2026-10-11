from enum import Enum


class ActionType(str, Enum):
    PHYSICAL = "physical"
    MAGIC = "magic"
    SKILL = "skill"  # habilidade única da classe (ver Fighter.SKILL)

    @property
    def label(self) -> str:
        return {"physical": "Ataque Físico", "magic": "Magia", "skill": "Habilidade"}[self.value]


class Side(str, Enum):
    PLAYER = "player"
    OPPONENT = "opponent"

    @property
    def other(self) -> "Side":
        return Side.OPPONENT if self is Side.PLAYER else Side.PLAYER
