from dataclasses import dataclass

from Game.domain.fighter import Assassin, Fighter, Knight, Mage


@dataclass(frozen=True)
class CharacterDef:
    """Definição estática de um personagem jogável. Adicionar um novo
    personagem = criar a subclasse de Fighter + uma entrada em CHARACTERS."""
    id: str
    name: str
    fighter_cls: type[Fighter]
    lore: str
    icon: str
    sprite_slug: str

    def create(self) -> Fighter:
        return self.fighter_cls()

    def sprite_paths(self, kind: str) -> list[str]:
        """kind: idle | ataque_fisico | magico (convenção em public/moveChar)."""
        return [f"public/moveChar/right_{self.sprite_slug}_{kind}_{i}.png" for i in (1, 2)]


CHARACTERS: dict[str, CharacterDef] = {c.id: c for c in (
    CharacterDef(
        "assassino", "Assassino", Assassin,
        "Henrique, naufrago nas praias do condado e capturado roubando uma lorde, "
        "esse estrangeiro foi tomado como prisioneiro e agora luta por sua liberdade, na arena.",
        "public/IconesJogo/assassino.jpeg", "assassino"),
    CharacterDef(
        "cavaleiro", "Cavaleiro", Knight,
        "Sula, o fracassado e desertor na batalha dos sete exércitos. "
        "Sula busca o perdão prometido em vitória na arena.",
        "public/IconesJogo/cavaleiro.jpeg", "cavaleiro"),
    CharacterDef(
        "mago", "Mago", Mage,
        "Arnabin, um velho sábio (ou louco) do novo continente. "
        "Ele se diverte com seus experimentos em humanos e procura se entreter na arena.",
        "public/IconesJogo/mago.jpeg", "mago"),
)}

SPRITE_KIND = {"idle": "idle", "physical": "ataque_fisico", "magic": "magico"}


def get_character(char_id: str) -> CharacterDef:
    return CHARACTERS[char_id]
