from enum import Enum


class ActionType(str, Enum):
    PHYSICAL = "physical"
    MAGIC = "magic"

    @property
    def label(self) -> str:
        return {"physical": "Ataque Físico", "magic": "Magia"}[self.value]


class Side(str, Enum):
    PLAYER = "player"
    OPPONENT = "opponent"

    @property
    def other(self) -> "Side":
        return Side.OPPONENT if self is Side.PLAYER else Side.PLAYER
