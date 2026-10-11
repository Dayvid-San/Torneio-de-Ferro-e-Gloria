import random
from dataclasses import dataclass

from Game.domain.actions import ActionType, Side
from Game.domain.ai import Policy, RandomPolicy
from Game.domain.arena import NEUTRAL_ARENA, Arena
from Game.domain.damage import DamageModifier, calculate_damage
from Game.domain.fighter import Fighter


@dataclass(frozen=True)
class BattleEvent:
    """Fato ocorrido na luta. A UI usa para animar; testes, para asserir."""
    turn: int
    actor: Side
    target: Side
    action: ActionType
    damage: int
    target_hp: int
    defeated: bool
    crit: bool = False
    mana_spent: int = 0
    actor_mana: int = 0
    skill: str | None = None        # nome da habilidade, se a ação foi SKILL
    self_damage: int = 0            # veneno sofrido pelo ator ao fim do turno
    effects: tuple[str, ...] = ()   # efeitos aplicados neste turno


class BattleOver(RuntimeError):
    pass


class IllegalAction(ValueError):
    pass


class Battle:
    """Máquina de estados de uma luta por turnos 1v1. Sem I/O nem relógio."""

    def __init__(self, player: Fighter, opponent: Fighter, *,
                 first: Side = Side.PLAYER,
                 policy: Policy | None = None,
                 rng: random.Random | None = None,
                 modifiers: tuple[DamageModifier, ...] = (),
                 arena: Arena = NEUTRAL_ARENA):
        self._fighters = {Side.PLAYER: player, Side.OPPONENT: opponent}
        self.turn_side = first
        self.turn_number = 1
        self.rng = rng or random.Random()
        self.policy = policy or RandomPolicy(self.rng)
        self.arena = arena
        self.modifiers = arena.modifiers + modifiers
        self.history: list[BattleEvent] = []

    def fighter(self, side: Side) -> Fighter:
        return self._fighters[side]

    @property
    def winner(self) -> Side | None:
        for side, fighter in self._fighters.items():
            if not fighter.is_alive:
                return side.other
        return None

    @property
    def is_over(self) -> bool:
        return self.winner is not None

    def legal_actions(self, side: Side | None = None) -> list[ActionType]:
        return self.fighter(side or self.turn_side).legal_actions()

    def act(self, action: ActionType | None = None) -> BattleEvent:
        """Executa o turno de quem está na vez. Sem `action`, a policy decide."""
        if self.is_over:
            raise BattleOver("A luta já terminou")
        actor_side = self.turn_side
        if action is None:
            action = self.policy.choose(self, actor_side)
        attacker = self.fighter(actor_side)
        defender = self.fighter(actor_side.other)
        if not attacker.can_use(action):
            raise IllegalAction(f"Ação indisponível: {action.value}")

        cost = attacker.cost(action)
        attacker.spend_mana(cost)
        skill = attacker.skill if action is ActionType.SKILL else None

        dealt, crit = 0, False
        if skill is None or skill.damage_action is not None:
            crit = (skill.guaranteed_crit if skill
                    else self.rng.random() < attacker.crit_chance + self.arena.crit_bonus)
            dealt = defender.take_damage(calculate_damage(
                attacker, defender, action, self.modifiers, crit, skill))

        self_damage = 0
        if defender.is_alive:  # fim do turno do ator: veneno, cooldown e duração
            self_damage = attacker.end_turn_upkeep()
            attacker.regen_mana(self.arena.mana_regen_bonus)
        applied = ()
        if skill is not None:
            attacker.start_cooldown()
            for effect in skill.self_effects:
                attacker.add_effect(effect)
            for effect in skill.target_effects:
                defender.add_effect(effect)
            applied = tuple(e.name for e in skill.self_effects + skill.target_effects)

        event = BattleEvent(self.turn_number, actor_side, actor_side.other, action,
                            dealt, defender.hp, not defender.is_alive,
                            crit, cost, attacker.mana, skill.name if skill else None,
                            self_damage, applied)
        self.history.append(event)
        self.turn_side = actor_side.other
        self.turn_number += 1
        return event
