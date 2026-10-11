import pygame

from Game.config import GOLD, GREEN, GREY, RED, WHITE
from Game.data.arenas import ARENAS
from Game.data.characters import CHARACTERS
from Game.scenes.base import Scene
from Game.ui.button import Button


class ResultScene(Scene):
    """Fim de luta: mostra o resultado e oferece o próximo passo (próxima rodada,
    revanche, novo torneio ou menu)."""

    def __init__(self, game, won: bool, turns: int, opponent_id: str):
        super().__init__(game)
        self.won = won
        self.turns = turns
        self.opponent_id = opponent_id
        assets = game.assets
        self.font = assets.font(40)
        self.small = assets.font(30)
        self.background = assets.image("public/fundo.jpeg", game.screen.get_size(), alpha=False)
        tour = game.tournament if game.mode == "torneio" else None
        self.tour = tour

        if tour is None:
            self.title, color = ("Vitória!", GREEN) if won else ("Derrota", RED)
            primary = ("rematch", "Revanche")
        elif tour.is_champion:
            self.title, color, primary = "CAMPEÃO DO TORNEIO!", GOLD, ("new", "Novo torneio")
        elif tour.eliminated:
            self.title, color, primary = "Eliminado do torneio", RED, ("new", "Novo torneio")
        else:
            self.title, color, primary = "Rodada vencida!", GREEN, ("next", "Próxima luta")
        self.title_surface = self.font.render(self.title, True, color)

        lines = [f"Contra {CHARACTERS[opponent_id].name} em {turns} turnos"]
        if tour and not tour.is_over:
            nxt = CHARACTERS[tour.current_opponent].name
            lines.append(f"Próximo adversário: {nxt} — {ARENAS[tour.current_arena].name}")
        elif tour:
            lines.append(f"Rodadas vencidas: {sum(tour.results)}/{tour.total_rounds}")
        self.lines = [self.small.render(t, True, WHITE) for t in lines]

        self.actions = {primary[0]: Button(280, 360, 240, 55, primary[1], self.font, GREY, WHITE),
                        "menu": Button(280, 430, 240, 55, "Menu", self.font, GREY, WHITE)}

    def activate(self, key: str) -> None:
        game = self.game
        if key == "menu":
            game.go_to("menu")
        elif key == "new":
            game.go_to("character_select")
        elif key in ("next", "rematch"):
            game.go_to("gameplay")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.activate(next(iter(self.actions)))
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.activate("menu")
                return
            for key, button in self.actions.items():
                if button.was_clicked(event):
                    self.activate(key)
                    return

    def update(self, dt):
        mouse = pygame.mouse.get_pos()
        for button in self.actions.values():
            button.update_hover(mouse)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        veil = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 150))
        screen.blit(veil, (0, 0))
        cx = screen.get_width() // 2
        screen.blit(self.title_surface, self.title_surface.get_rect(center=(cx, 160)))
        for i, line in enumerate(self.lines):
            screen.blit(line, line.get_rect(center=(cx, 230 + i * 40)))
        for button in self.actions.values():
            button.draw(screen)
