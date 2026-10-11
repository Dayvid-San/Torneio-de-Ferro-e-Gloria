from Game.domain.actions import ActionType
from Game.domain.effects import ActiveEffect, Effect, EffectKind
from Game.domain.skills import FURTIVE_STRIKE, SHIELD_STANCE, TOXIC_BOLT, Skill


class Fighter:
    """Lutador. Atributos encapsulados; subclasses definem os valores padrão
    e a frase de efeito (polimorfismo)."""

    DEFAULT_PHYSICAL = 10
    DEFAULT_MAGIC = 10
    DEFAULT_HP = 100
    DEFAULT_PHYSICAL_DEFENSE = 0
    DEFAULT_MAGIC_DEFENSE = 0
    DEFAULT_CRIT_CHANCE = 0.10
    DEFAULT_MAX_MANA = 30
    MAGIC_COST = 10
    MANA_REGEN = 5
    SKILL: Skill | None = None
    CATCHPHRASE = ""

    def __init__(self, physical: int | None = None, magic: int | None = None,
                 max_hp: int | None = None, *, physical_defense: int | None = None,
                 magic_defense: int | None = None, crit_chance: float | None = None,
                 max_mana: int | None = None):
        pick = lambda value, default: default if value is None else value  # noqa: E731
        self.__physical = pick(physical, self.DEFAULT_PHYSICAL)
        self.__magic = pick(magic, self.DEFAULT_MAGIC)
        self.__max_hp = pick(max_hp, self.DEFAULT_HP)
        self.__physical_defense = pick(physical_defense, self.DEFAULT_PHYSICAL_DEFENSE)
        self.__magic_defense = pick(magic_defense, self.DEFAULT_MAGIC_DEFENSE)
        self.__crit_chance = pick(crit_chance, self.DEFAULT_CRIT_CHANCE)
        self.__max_mana = pick(max_mana, self.DEFAULT_MAX_MANA)
        if min(self.__physical, self.__magic, self.__max_hp) <= 0:
            raise ValueError("Atributos devem ser positivos")
        if min(self.__physical_defense, self.__magic_defense, self.__max_mana) < 0:
            raise ValueError("Defesa e mana não podem ser negativas")
        if not 0 <= self.__crit_chance <= 1:
            raise ValueError("crit_chance deve estar entre 0 e 1")
        self.__hp = self.__max_hp
        self.__mana = self.__max_mana
        self.__cooldown = 0
        self.__effects: dict[EffectKind, ActiveEffect] = {}

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
    def physical_defense(self) -> int:
        return self.__physical_defense

    @property
    def magic_defense(self) -> int:
        return self.__magic_defense

    @property
    def crit_chance(self) -> float:
        return self.__crit_chance

    @property
    def max_hp(self) -> int:
        return self.__max_hp

    @property
    def hp(self) -> int:
        return self.__hp

    @property
    def max_mana(self) -> int:
        return self.__max_mana

    @property
    def mana(self) -> int:
        return self.__mana

    @property
    def is_alive(self) -> bool:
        return self.__hp > 0

    @property
    def skill(self) -> Skill | None:
        return self.SKILL

    @property
    def skill_cooldown(self) -> int:
        return self.__cooldown

    @property
    def effects(self) -> list[ActiveEffect]:
        return list(self.__effects.values())

    def has_effect(self, kind: EffectKind) -> bool:
        return kind in self.__effects

    def power(self, action: ActionType) -> int:
        if action is ActionType.SKILL:
            skill = self.SKILL
            return round(self.power(skill.damage_action) * skill.power_mult) \
                if skill and skill.damage_action else 0
        return self.__physical if action is ActionType.PHYSICAL else self.__magic

    def defense_against(self, action: ActionType) -> int:
        if action is ActionType.SKILL:
            action = self.SKILL.damage_action if self.SKILL else None
        base = self.__physical_defense if action is ActionType.PHYSICAL else self.__magic_defense
        bonus = self.__effects.get(EffectKind.DEFENSE_UP)
        return base + (bonus.effect.amount if bonus else 0)

    def cost(self, action: ActionType) -> int:
        if action is ActionType.MAGIC:
            return self.MAGIC_COST
        if action is ActionType.SKILL:
            return self.SKILL.mana_cost if self.SKILL else 0
        return 0

    def can_use(self, action: ActionType) -> bool:
        if action is ActionType.SKILL and (self.SKILL is None or self.__cooldown > 0):
            return False
        return self.__mana >= self.cost(action)

    def legal_actions(self) -> list[ActionType]:
        return [a for a in ActionType if self.can_use(a)]

    # --- mutação -------------------------------------------------------
    def take_damage(self, amount: int) -> int:
        """Aplica dano e devolve o dano efetivamente causado."""
        dealt = min(max(0, amount), self.__hp)
        self.__hp -= dealt
        return dealt

    def spend_mana(self, amount: int) -> None:
        if amount > self.__mana:
            raise ValueError("Mana insuficiente")
        self.__mana -= amount

    def regen_mana(self, bonus: int = 0) -> None:
        self.__mana = min(self.__max_mana, self.__mana + self.MANA_REGEN + bonus)

    def add_effect(self, effect: Effect) -> None:
        self.__effects[effect.kind] = ActiveEffect(effect)

    def start_cooldown(self) -> None:
        self.__cooldown = self.SKILL.cooldown if self.SKILL else 0

    def end_turn_upkeep(self) -> int:
        """Chamado ao fim de cada turno do próprio lutador: aplica veneno,
        reduz cooldown e duração dos efeitos. Devolve o dano de veneno sofrido."""
        poison = self.__effects.get(EffectKind.POISON)
        damage = self.take_damage(poison.effect.amount) if poison else 0
        self.__cooldown = max(0, self.__cooldown - 1)
        for kind in list(self.__effects):
            self.__effects[kind].remaining -= 1
            if self.__effects[kind].remaining <= 0:
                del self.__effects[kind]
        return damage

    def catchphrase(self) -> str:
        return self.CATCHPHRASE


class Assassin(Fighter):
    DEFAULT_PHYSICAL, DEFAULT_MAGIC = 25, 15
    DEFAULT_PHYSICAL_DEFENSE, DEFAULT_MAGIC_DEFENSE = 4, 4
    DEFAULT_CRIT_CHANCE = 0.30
    DEFAULT_MAX_MANA = 30
    SKILL = FURTIVE_STRIKE
    CATCHPHRASE = "Eu lhe caçarei até a morte"


class Knight(Fighter):
    DEFAULT_PHYSICAL, DEFAULT_MAGIC = 30, 10
    DEFAULT_PHYSICAL_DEFENSE, DEFAULT_MAGIC_DEFENSE = 8, 2
    DEFAULT_CRIT_CHANCE = 0.10
    DEFAULT_MAX_MANA = 20
    SKILL = SHIELD_STANCE
    CATCHPHRASE = "Pela honra do Rei, eu te anularei"


class Mage(Fighter):
    DEFAULT_PHYSICAL, DEFAULT_MAGIC = 10, 35
    DEFAULT_PHYSICAL_DEFENSE, DEFAULT_MAGIC_DEFENSE = 1, 6
    DEFAULT_CRIT_CHANCE = 0.10
    DEFAULT_MAX_MANA = 30
    MAGIC_COST = 15
    MANA_REGEN = 8
    SKILL = TOXIC_BOLT
    CATCHPHRASE = "Eu sou dos magos, o mais poderoso"
