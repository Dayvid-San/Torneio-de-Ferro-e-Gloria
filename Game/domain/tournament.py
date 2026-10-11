import random


class Tournament:
    """Chaveamento de eliminação simples: o jogador enfrenta todos os demais
    personagens, um por rodada, em ordem sorteada. Perdeu, está fora."""

    def __init__(self, player_id: str, character_ids: list[str],
                 rng: random.Random | None = None, arena_ids: list[str] | None = None,
                 max_rounds: int | None = None):
        self.player_id = player_id
        self.opponents = [c for c in character_ids if c != player_id]
        if not self.opponents:
            raise ValueError("Torneio precisa de ao menos um oponente")
        rng = rng or random.Random()
        rng.shuffle(self.opponents)
        if max_rounds:
            self.opponents = self.opponents[:max_rounds]
        # uma arena por rodada, sem repetir até esgotar as disponíveis
        pool = list(arena_ids or [])
        self.arenas: list[str | None] = []
        while len(self.arenas) < len(self.opponents):
            if not pool:
                pool = list(arena_ids or [None])
            self.arenas.append(pool.pop(rng.randrange(len(pool))))
        self.results: list[bool] = []

    @property
    def total_rounds(self) -> int:
        return len(self.opponents)

    @property
    def round_number(self) -> int:
        """Rodada em andamento (1-based); após o fim, a última disputada."""
        return min(len(self.results) + 1, self.total_rounds)

    @property
    def eliminated(self) -> bool:
        return bool(self.results) and not self.results[-1]

    @property
    def is_over(self) -> bool:
        return self.eliminated or len(self.results) == self.total_rounds

    @property
    def is_champion(self) -> bool:
        return len(self.results) == self.total_rounds and all(self.results)

    @property
    def current_opponent(self) -> str | None:
        return None if self.is_over else self.opponents[len(self.results)]

    @property
    def current_arena(self) -> str | None:
        return None if self.is_over else self.arenas[len(self.results)]

    def record(self, won: bool) -> None:
        if self.is_over:
            raise RuntimeError("Torneio já terminou")
        self.results.append(won)
