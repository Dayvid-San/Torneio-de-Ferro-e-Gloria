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

`python -m tools.simulate` usa por padrão a policy `heuristic` (jogo razoável, sem erros aleatórios), que é a
medida de balanceamento que importa; `random` mostra o efeito de jogar sem critério e `greedy` o pior caso.
`--check` valida win rate geral (35–65%) **e por arena** (30–70%); `--arena <id>` isola uma arena.

Baseline atual (heuristic, 4000 lutas/par, seed 1): Assassino ≈55%, Mago ≈48%, Cavaleiro ≈46%.
Por arena: coliseu 52/48/50 · lâminas 68/43/40 · arcana 52/48/50 · cripta 51/47/53 (ass/cav/mag).

**Lição de balanceamento:** com dano fixo e 100 de vida, há degraus (ex.: 33 de dano mágico mata em 4 golpes, 34 em 3).
Um bônus de 5% já moveu o Mago de 50% a 71% contra o Cavaleiro. Ao mexer em números, rode `make sim` e
`--arena` para cada arena, não só o geral. Câmara Arcana está propositalmente sutil (+3% magia, +5 mana) por causa disso.
