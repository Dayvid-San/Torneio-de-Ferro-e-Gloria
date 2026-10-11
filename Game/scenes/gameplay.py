import pygame

from Game import config
from Game.config import GREEN, GREY, RED, WHITE
from Game.data.characters import CHARACTERS, SPRITE_KIND, CharacterDef
from Game.domain.actions import ActionType, Side
from Game.domain.ai import RandomPolicy
from Game.domain.battle import Battle, BattleEvent
from Game.scenes.base import Scene
from Game.ui.animation import Animation
from Game.ui.button import Button
from Game.ui.widgets import draw_health_bar, draw_mana_bar

INPUT, ACTING, ENDED = "input", "acting", "ended"


class GameplayScene(Scene):
    """Apresentação de uma `Battle`. A scene só decide *quando* agir e como
    mostrar; todas as regras vivem em Game.domain."""

    def __init__(self, game, player_id: str | None = None, opponent_id: str | None = None,
                 battle: Battle | None = None):
        super().__init__(game)
        assets = game.assets
        player_id = player_id or game.selected_character_id or "assassino"
        tournament = game.tournament if game.mode == "torneio" else None
        if opponent_id is None and tournament and tournament.current_opponent:
            opponent_id = tournament.current_opponent
        if opponent_id is None:
            opponent_id = game.rng.choice([c for c in CHARACTERS if c != player_id])
        self.defs: dict[Side, CharacterDef] = {
            Side.PLAYER: CHARACTERS[player_id], Side.OPPONENT: CHARACTERS[opponent_id]}
        self.battle = battle or Battle(
            self.defs[Side.PLAYER].create(), self.defs[Side.OPPONENT].create(),
            policy=RandomPolicy(game.rng))

        self.font = assets.font(40)
        self.background = assets.image("public/fundo.jpeg", game.screen.get_size(), alpha=False)
        w, h = game.screen.get_size()
        self.width, self.height = w, h
        cost = self.battle.fighter(Side.PLAYER).cost(ActionType.MAGIC)
        self.buttons = {
            ActionType.PHYSICAL: Button(w // 3 - 90, h - 100, 180, 50, "Físico [1]", self.font),
            ActionType.MAGIC: Button(2 * w // 3 - 90, h - 100, 180, 50,
                                     f"Magia [2] -{cost}", self.font),
        }
        self.hotkeys = {pygame.K_1: ActionType.PHYSICAL, pygame.K_f: ActionType.PHYSICAL,
                        pygame.K_2: ActionType.MAGIC}
        self.floaters: list[dict] = []  # números de dano flutuantes
        self.small_font = assets.font(30)
        self.round_label = (f"Rodada {tournament.round_number}/{tournament.total_rounds}"
                            if tournament else "Duelo Rápido")
        self.animations = {side: self._animation(side, "idle") for side in Side}
        self.phase = INPUT
        self.timer = 0.0
        self.last_event: BattleEvent | None = None

    # --- apresentação ---------------------------------------------------
    def _animation(self, side: Side, kind: str) -> Animation:
        paths = self.defs[side].sprite_paths(SPRITE_KIND[kind])
        frames = [self.game.assets.image(p, config.SPRITE_SIZE, flip_x=side is Side.OPPONENT)
                  for p in paths]
        return Animation(frames, config.FRAME_DURATION)

    def _name(self, side: Side) -> str:
        return self.defs[side].name

    def _status_text(self) -> str:
        if self.battle.is_over:
            return "Você Venceu!" if self.battle.winner is Side.PLAYER else "Você Perdeu!"
        return "Seu Turno" if self.battle.turn_side is Side.PLAYER else "Turno do Oponente"

    # --- fluxo ----------------------------------------------------------
    def perform(self, action: ActionType | None = None) -> None:
        event = self.battle.act(action)
        self.last_event = event
        kind = "physical" if event.action is ActionType.PHYSICAL else "magic"
        self.animations[event.actor] = self._animation(event.actor, kind)
        self.game.audio.play("attack")
        self.game.audio.play("hit")
        x = self._x(event.target) + 100
        text = f"{event.damage}!" if event.crit else str(event.damage)
        self.floaters.append({"text": text, "x": x, "y": self.height // 2 - 90, "age": 0.0,
                              "color": (255, 215, 0) if event.crit else WHITE})
        self.phase, self.timer = ACTING, config.ACTION_DELAY

    def _x(self, side: Side) -> int:
        return self.width // 4 - 100 if side is Side.PLAYER else 3 * self.width // 4 - 100

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.go_to("menu")
                return
            if self.phase != INPUT:
                continue
            if event.type == pygame.KEYDOWN and event.key in self.hotkeys:
                action = self.hotkeys[event.key]
                if action in self.battle.legal_actions(Side.PLAYER):
                    self.perform(action)
                    return
            for action, button in self.buttons.items():
                if button.was_clicked(event):
                    self.perform(action)
                    return

    def update(self, dt):
        for anim in self.animations.values():
            anim.update(dt)
        for f in self.floaters:
            f["age"] += dt
        self.floaters = [f for f in self.floaters if f["age"] < 1.0]
        mouse = pygame.mouse.get_pos()
        legal = self.battle.legal_actions(Side.PLAYER)
        for action, button in self.buttons.items():
            button.enabled = action in legal
            button.update_hover(mouse)

        if self.phase == INPUT:
            return
        self.timer -= dt
        if self.timer > 0:
            return
        if self.phase == ENDED:
            self._finish()
        elif self.battle.is_over:
            self.animations[self.last_event.actor] = self._animation(self.last_event.actor, "idle")
            self.phase, self.timer = ENDED, config.END_DELAY
        else:
            self.animations[self.last_event.actor] = self._animation(self.last_event.actor, "idle")
            if self.battle.turn_side is Side.OPPONENT:
                self.perform()  # policy do oponente
            else:
                self.phase = INPUT

    def _finish(self) -> None:
        won = self.battle.winner is Side.PLAYER
        tournament = self.game.tournament if self.game.mode == "torneio" else None
        if tournament and not tournament.is_over:
            tournament.record(won)
        self.game.go_to("result", won=won, turns=len(self.battle.history),
                        opponent_id=self.defs[Side.OPPONENT].id)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        y = self.height // 2
        xs = {Side.PLAYER: self.width // 4 - 100, Side.OPPONENT: 3 * self.width // 4 - 100}
        for side in Side:
            fighter = self.battle.fighter(side)
            screen.blit(self.animations[side].frame, (xs[side], y))
            screen.blit(self.font.render(self._name(side), True, WHITE), (xs[side], y - 85))
            draw_health_bar(screen, xs[side], y - 50, fighter.hp, fighter.max_hp)
            draw_mana_bar(screen, xs[side], y - 26, fighter.mana, fighter.max_mana)

        if self.phase == INPUT:
            for button in self.buttons.values():
                button.draw(screen)
        for f in self.floaters:
            label = self.font.render(f["text"], True, f["color"])
            screen.blit(label, label.get_rect(center=(f["x"], f["y"] - int(60 * f["age"]))))
        screen.blit(self.small_font.render(self.round_label, True, WHITE), (10, 10))

        color = WHITE
        if self.battle.is_over:
            color = GREEN if self.battle.winner is Side.PLAYER else RED
        status = self.font.render(self._status_text(), True, color)
        screen.blit(status, status.get_rect(center=(self.width // 2, 60)))
        if self.last_event:
            e = self.last_event
            crit = " CRÍTICO!" if e.crit else ""
            log = self.font.render(
                f"{self._name(e.actor)}: {e.action.label}, {e.damage} de dano{crit}",
                True, (255, 215, 0) if e.crit else GREY)
            screen.blit(log, log.get_rect(center=(self.width // 2, 100)))
