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
    fighter.py       Fighter (HP, ataque, defesa, crítico, mana) + Assassin/Knight/Mage
    battle.py        Battle: máquina de estados de turnos, histórico de BattleEvent
    skills.py        Skill (declarativa): custo, cooldown, dano, efeitos; 1 por classe
    effects.py       Effect/ActiveEffect (DEFENSE_UP, POISON)
    arena.py         Arena: multiplicadores de dano, bônus de crítico e de mana
    damage.py        calculate_damage (poder x crítico -> modificadores -> defesa) + DamageModifier
    ai.py            Policy: RandomPolicy, GreedyPolicy
    tournament.py    Tournament: chaveamento de eliminação (jogador vs. todos os demais)
    actions.py       ActionType, Side
  data/              characters.py (lore, sprites) e arenas.py (catálogo de cenários)
  audio.py           música e efeitos (no-op se não houver dispositivo/arquivo)
  scenes/            menu, character_select, gameplay, result (registro por nome)
  ui/                Button, Animation (por dt), texto, barra de vida
tests/ tools/        harness (ver HARNESS.md)
```

## Fluxo de dependências
`scenes → ui, data, domain` · `data → domain` · `domain → nada`. Um teste garante que
`domain` não importa pygame/UI.

## Pontos de extensão do roadmap
| Item do README | Onde entra |
|---|---|
| Arenas com bônus/penalidades | ✅ `Arena` em `data/arenas.py` (novas arenas = nova entrada) |
| Eventos aleatórios por rodada | hook por turno em `Battle` + `rng` injetado |
| Habilidades | ✅ `Skill` declarativa; passivas ainda não |
| Torneio e ranking | novo pacote `domain/tournament.py` (chaveamento de `Battle`s) + cena `tournament` |
| Save/progressão | `domain` serializável + `utils/save.py` |

## Mudanças em relação à versão anterior
- Lógica de combate saiu de `GameplayScene` (209 linhas misturando regra, input, tempo e desenho).
- Imports quebrados (`from personagem import ...`) e circulares entre cenas removidos; navegação por nome.
- Tempo por `dt` em vez de `get_ticks`/`clock.tick` duplicado.
- Dados dos personagens deixaram de estar duplicados em 3 lugares (stats, caminhos de sprite, lore).
- Removidos pacotes `utills/`, `managers/` (código duplicado) e 3 PNGs idênticos (`* copy.png`).

## Regras de combate
- Dano = `poder` (x1,5 se crítico) → modificadores → menos defesa do alvo (física ou mágica), mínimo 1.
- Crítico: sorteado em `Battle` com o `rng` injetado, chance por classe (`crit_chance`).
- Mana: Magia custa `MAGIC_COST`; ataque físico é grátis; `MANA_REGEN` ao fim de cada turno próprio.
  Sem mana, `legal_actions()` exclui a magia (UI desabilita o botão; policies respeitam; `Battle.act` levanta `IllegalAction`).
- Atributos: Assassino 25/15, def 4/4, crit 30%, mana 30 · Cavaleiro 30/10, def 8/2, crit 10%, mana 20 · Mago 10/35, def 1/6, crit 10%, mana 30 (custo 15, regen 8).

## Fluxo de jogo
Menu → **Torneio** (rodadas contra cada outro lutador; derrota elimina) ou **Duelo Rápido**
→ seleção (hover mostra atributos) → luta → resultado (próxima luta / revanche / novo torneio / menu).
Controles: mouse ou `1`/`F` físico, `2` magia (na luta); `Enter`/`Espaço` confirma no resultado;
`Esc` volta; `M` liga/desliga o som.

## Habilidades, status e arenas
- **Habilidade** (`ActionType.SKILL`, tecla `3`): uma por classe, declarada em `domain/skills.py`. `Battle` aplica
  qualquer combinação de dano / crítico garantido / ignorar defesa / efeitos em si / efeitos no alvo, então uma
  skill nova não exige código de combate. Tem cooldown (turnos próprios) e pode custar mana.
  - Assassino — *Golpe Furtivo*: físico, crítico garantido, ignora defesa; cooldown 3.
  - Cavaleiro — *Postura de Escudo*: sem dano, +6 de defesa por 2 turnos do oponente; cooldown 3.
  - Mago — *Raio Tóxico*: magia a 60% do poder + veneno (5/turno, 3 turnos do portador); 10 mana; cooldown 3.
- **Efeitos de status**: ao fim do turno do portador aplica-se veneno (ignora defesa; pode matar), reduz-se cooldown
  e duração. Reaplicar o mesmo efeito renova.
- **Arenas** (`Arena`): multiplicador de dano físico/mágico, bônus de crítico, bônus de regeneração de mana e um tom
  de cor sobre o fundo (não há arte própria por arena ainda). No torneio cada rodada tem uma arena (sem repetir
  até esgotar); no duelo é sorteada. O banner de abertura mostra nome, descrição e efeitos.
- **IA do oponente** (`HeuristicPolicy`): usa skill de dano sempre que disponível, escudo com vida baixa, poupa
  mana e erra de propósito 25% das vezes (`randomness`).
