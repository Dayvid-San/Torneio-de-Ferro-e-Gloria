# Arquitetura

**Gênero:** RPG de combate por turnos, duelo 1v1 em arena (estilo JRPG clássico), com
seleção de personagem e, no roadmap, torneio/ranking, arenas, eventos aleatórios e habilidades.
Esse gênero é *dirigido por regras e dados*, não por física/tempo real, então a arquitetura
separa a simulação da apresentação.

```
main.py              entrada
Game/
  core.py            Game: janela, loop, cena atual, rng; step(events, dt)
  config.py          constantes e tempos
  assets.py          cache de imagens/fontes + placeholder se faltar arquivo
  domain/            REGRAS (puro Python, sem pygame)
    fighter.py       Fighter + Assassin/Knight/Mage (herança, encapsulamento, polimorfismo)
    battle.py        Battle: máquina de estados de turnos, histórico de BattleEvent
    damage.py        calculate_damage + ganchos DamageModifier
    ai.py            Policy: RandomPolicy, GreedyPolicy
    actions.py       ActionType, Side
  data/characters.py CharacterDef: conteúdo (nome, lore, sprites) separado da lógica
  scenes/            apresentação: menu, character_select, gameplay (registro por nome)
  ui/                Button, Animation (por dt), texto, barra de vida
tests/ tools/        harness (ver HARNESS.md)
```

## Fluxo de dependências
`scenes → ui, data, domain` · `data → domain` · `domain → nada`. Um teste garante que
`domain` não importa pygame/UI.

## Pontos de extensão do roadmap
| Item do README | Onde entra |
|---|---|
| Arenas com bônus/penalidades | `DamageModifier` passados a `Battle` + dados de arena em `data/` |
| Eventos aleatórios por rodada | hook por turno em `Battle` + `rng` injetado |
| Habilidades/passivas | novos `ActionType` / métodos em `Fighter` |
| Torneio e ranking | novo pacote `domain/tournament.py` (chaveamento de `Battle`s) + cena `tournament` |
| Save/progressão | `domain` serializável + `utils/save.py` |

## Mudanças em relação à versão anterior
- Lógica de combate saiu de `GameplayScene` (209 linhas misturando regra, input, tempo e desenho).
- Imports quebrados (`from personagem import ...`) e circulares entre cenas removidos; navegação por nome.
- Tempo por `dt` em vez de `get_ticks`/`clock.tick` duplicado.
- Dados dos personagens deixaram de estar duplicados em 3 lugares (stats, caminhos de sprite, lore).
- Removidos pacotes `utills/`, `managers/` (código duplicado) e 3 PNGs idênticos (`* copy.png`).
