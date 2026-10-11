from Game.domain.actions import ActionType


class Fighter:
    """Lutador. Atributos encapsulados; subclasses definem os valores padrão
    e a frase de efeito (polimorfismo)."""

    DEFAULT_PHYSICAL = 10
    DEFAULT_MAGIC = 10
    DEFAULT_HP = 100
    CATCHPHRASE = ""

    def __init__(self, physical: int | None = None, magic: int | None = None,
                 max_hp: int | None = None):
        self.__physical = self.DEFAULT_PHYSICAL if physical is None else physical
        self.__magic = self.DEFAULT_MAGIC if magic is None else magic
        self.__max_hp = self.DEFAULT_HP if max_hp is None else max_hp
        if self.__physical <= 0 or self.__magic <= 0 or self.__max_hp <= 0:
            raise ValueError("Atributos devem ser positivos")
        self.__hp = self.__max_hp

    # --- atributos -----------------------------------------------------
    @property
    def physical(self) -> int:
        return self.__physical

    @physical.setter
    def physical(self, value: int) -> None:
        self.__physical = max(1, value)

    @property
    def magic(self) -> int:
        return self.__magic

    @magic.setter
    def magic(self, value: int) -> None:
        self.__magic = max(1, value)

    @property
    def max_hp(self) -> int:
        return self.__max_hp

    @property
    def hp(self) -> int:
        return self.__hp

    @property
    def is_alive(self) -> bool:
        return self.__hp > 0

    def power(self, action: ActionType) -> int:
        return self.__physical if action is ActionType.PHYSICAL else self.__magic

    # --- mutação -------------------------------------------------------
    def take_damage(self, amount: int) -> int:
        """Aplica dano e devolve o dano efetivamente causado."""
        dealt = min(max(0, amount), self.__hp)
        self.__hp -= dealt
        return dealt

    def catchphrase(self) -> str:
        return self.CATCHPHRASE


class Assassin(Fighter):
    DEFAULT_PHYSICAL, DEFAULT_MAGIC = 25, 15
    CATCHPHRASE = "Eu lhe caçarei até a morte"


class Knight(Fighter):
    DEFAULT_PHYSICAL, DEFAULT_MAGIC = 30, 10
    CATCHPHRASE = "Pela honra do Rei, eu te anularei"


class Mage(Fighter):
    DEFAULT_PHYSICAL, DEFAULT_MAGIC = 10, 35
    CATCHPHRASE = "Eu sou dos magos, o mais poderoso"
