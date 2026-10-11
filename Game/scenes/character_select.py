import pygame

from Game.config import GREY, WHITE
from Game.data.arenas import ARENAS
from Game.data.characters import CHARACTERS
from Game.scenes.base import Scene
from Game.ui.button import Button
from Game.domain.actions import ActionType
from Game.domain.tournament import Tournament
from Game.ui.text import wrap_text


class CharacterSelectScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        assets = game.assets
        self.font = assets.font(40)
        self.small_font = assets.font(30)
        self.title = self.font.render("Selecione o Lutador", True, WHITE)
        self.background = assets.image("public/fundo.jpeg", game.screen.get_size(), alpha=False)
        self.icons = {cid: assets.image(c.icon, (80, 80)) for cid, c in CHARACTERS.items()}
        self.buttons = {
            cid: Button(150, 200 + i * 100, 150, 50, c.name, self.font, GREY, WHITE)
            for i, (cid, c) in enumerate(CHARACTERS.items())
        }
        self.hovered_id: str | None = None
        self._description: list[pygame.Surface] = []

    def select(self, char_id: str) -> None:
        game = self.game
        game.selected_character_id = char_id
        game.tournament = (Tournament(char_id, list(CHARACTERS), game.rng, list(ARENAS))
                           if game.mode == "torneio" else None)
        game.go_to("gameplay")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.go_to("menu")
                return
            for cid, button in self.buttons.items():
                if button.was_clicked(event):
                    self.select(cid)
                    return

    def update(self, dt):
        mouse = pygame.mouse.get_pos()
        hovered = None
        for cid, button in self.buttons.items():
            button.update_hover(mouse)
            if button.hovered:
                hovered = cid
        if hovered != self.hovered_id:
            self.hovered_id = hovered
            self._description = self._describe(hovered) if hovered else []

    def _describe(self, char_id: str) -> list[pygame.Surface]:
        c = CHARACTERS[char_id]
        f = c.create()
        stats = (f"PV {f.max_hp}  Fís {f.physical}  Mag {f.magic}  "
                 f"Def {f.physical_defense}/{f.magic_defense}  "
                 f"Crít {f.crit_chance:.0%}  Mana {f.max_mana} (Magia {f.cost(ActionType.MAGIC)})")
        gold = (255, 215, 0)
        skill = f.skill
        skill_txt = f"Habilidade - {skill.name}: {skill.description}" if skill else ""
        return (wrap_text(stats, self.small_font, gold, 420)
                + wrap_text(skill_txt, self.small_font, (140, 220, 255), 420)
                + wrap_text(c.lore, self.small_font, WHITE, 420))

    def _draw_text_box(self, screen, lines, x, y, padding=10):
        line_h = self.small_font.get_linesize()
        box = pygame.Surface((max(l.get_width() for l in lines) + 2 * padding,
                              len(lines) * line_h + 2 * padding), pygame.SRCALPHA)
        box.fill((0, 0, 0, 150))
        screen.blit(box, (x, y))
        for i, line in enumerate(lines):
            screen.blit(line, (x + padding, y + padding + i * line_h))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.title, (200, 100))
        for cid, button in self.buttons.items():
            screen.blit(self.icons[cid], (button.rect.x - 100, button.rect.y))
            button.draw(screen)
            if button.hovered and self._description:
                self._draw_text_box(screen, self._description, button.rect.right + 20, button.rect.y)
