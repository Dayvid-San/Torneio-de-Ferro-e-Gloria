# Harness de desenvolvimento

Para um jogo por turnos, o que mais quebra é **regra/balanceamento** e **fluxo entre telas**,
não frames. O harness cobre isso sem precisar de janela (`SDL_VIDEODRIVER=dummy`).

| Camada | Ferramenta | O que pega |
|---|---|---|
| Regras | `tests/test_fighter.py`, `test_battle.py` | dano, turnos, término, determinismo por seed |
| Fluxo/UI | `tests/test_scenes_headless.py` | menu→seleção→luta→menu via eventos sintéticos e `Game.step(events, dt)` |
| Conteúdo/arquitetura | `tests/test_content_and_architecture.py` | assets ausentes, `domain` importando pygame |
| Balanceamento | `python -m tools.simulate` | win rate por personagem/confronto, turnos médios; `--check` falha fora de 35–65% |
| Visual | `python -m tools.snapshot` | PNG de cada cena em `snapshots/` (artefato no CI) |
| Gate | `make check` / `.github/workflows/ci.yml` | tudo acima |

## Fluxo recomendado
1. Regra nova → teste em `tests/` primeiro (domínio, sem pygame).
2. `make sim` para ver o efeito no balanceamento (use `--policy greedy` para o pior caso).
3. UI → `make snapshot` e inspecionar as imagens.
4. `make check` antes do commit.

Baseline atual (random, 5000 lutas/par, seed 1): Assassino ≈53%, Mago ≈53%, Cavaleiro ≈45%.
Com `--policy greedy` (IA que só maximiza dano líquido, ignorando mana) o Cavaleiro sobe a ≈73%:
é um piso de pior caso, não o jogo real; observe-o ao mexer em defesa/mana, mas o gate usa `random`.
