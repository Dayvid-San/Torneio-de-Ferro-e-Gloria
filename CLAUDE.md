# Torneio de Ferro e Glória — guia para agentes

RPG de **combate por turnos 1v1 (arena)** em pygame. Fluxo: menu → seleção → luta → menu.
Roadmap (README): arenas com efeitos, eventos aleatórios, ranking/torneio, habilidades.

## Regra de ouro
Regras do jogo vivem em `Game/domain` (puro, sem pygame). Cenas só apresentam.
Se uma mudança de regra exige abrir janela para ser testada, ela está no lugar errado.

## Antes de dar por pronto
`make check` (pytest + simulação de balanceamento + snapshots headless). Roda sem display.
Mudou número/regra de combate? Rode `make sim` e reporte o win rate. Mudou UI? `make snapshot`
e olhe `snapshots/*.png`.

## Onde mexer
- Novo personagem: subclasse de `Fighter` + entrada em `Game/data/characters.py` (+ sprites em `public/moveChar`, convenção `right_<slug>_<idle|ataque_fisico|magico>_<1|2>.png`). Testes de assets cobrem.
- Nova habilidade: `Skill` em `domain/skills.py` + `SKILL = ...` na subclasse de `Fighter` (nenhum código de combate novo se couber nos campos de `Skill`; efeito inédito = novo `EffectKind` em `effects.py` e tratá-lo em `Fighter`).
- Nova arena: entrada em `Game/data/arenas.py`; rode `python -m tools.simulate --arena <id> --check`.
- Modificador de dano (evento/passiva): função em `Battle(modifiers=...)`.
- Nova IA: classe com `choose(battle, side)` em `domain/ai.py`.
- Nova cena: arquivo em `Game/scenes/`, registrar em `Game/scenes/__init__.py`, navegar com `game.go_to("nome")`.
- Constantes/tempos: `Game/config.py`. Imagens/fontes: sempre via `game.assets` (cache + fallback).

## Convenções
Cenas recebem `dt` em segundos (nada de `pygame.time.get_ticks` / `clock.tick` dentro de cena).
Aleatoriedade sempre por `random.Random` injetado (`game.rng`) para ser reproduzível.
Textos ao jogador em português; código em inglês.
