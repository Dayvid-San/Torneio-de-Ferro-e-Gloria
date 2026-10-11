from Game.domain.arena import NEUTRAL_ARENA, Arena

ARENAS: dict[str, Arena] = {a.id: a for a in (
    NEUTRAL_ARENA,
    Arena("lamina", "Campo de Lâminas",
          "Armas cravadas no chão: golpes físicos mais letais.",
          physical_mult=1.10, tint=(120, 30, 30, 70)),
    Arena("arcana", "Câmara Arcana",
          "Runas pulsam no ar: a magia ganha um pouco de força e a mana flui bem mais rápido.",
          magic_mult=1.03, mana_regen_bonus=5, tint=(40, 60, 170, 80)),
    Arena("cripta", "Cripta Sombria",
          "Sombras guiam os golpes: todos acertam críticos com mais frequência.",
          crit_bonus=0.15, tint=(20, 0, 40, 110)),
)}
