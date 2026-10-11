"""Simulador de balanceamento: roda N lutas por confronto, sem UI.

    python -m tools.simulate --fights 5000 --seed 1
    python -m tools.simulate --check          # falha (exit 1) se houver desbalanceio

Mede taxa de vitória de cada personagem (contra todos os outros, ambos os
lados) e duração média. Use após mexer em atributos, dano ou IA.
"""
import argparse
import random
import sys
from itertools import product

from Game.data.arenas import ARENAS
from Game.data.characters import CHARACTERS
from Game.domain.actions import ActionType, Side
from Game.domain.ai import GreedyPolicy, HeuristicPolicy, RandomPolicy
from Game.domain.arena import NEUTRAL_ARENA
from Game.domain.battle import Battle

POLICIES = {"random": lambda rng: RandomPolicy(rng),
            "greedy": lambda rng: GreedyPolicy(),
            "heuristic": lambda rng: HeuristicPolicy(rng, randomness=0.0)}


def fight(a_id, b_id, rng, policy_name, first=Side.PLAYER, arena_id=None):
    battle = Battle(CHARACTERS[a_id].create(), CHARACTERS[b_id].create(), first=first,
                    policy=POLICIES[policy_name](rng), rng=rng,
                    arena=ARENAS[arena_id] if arena_id else NEUTRAL_ARENA)
    while not battle.is_over:
        battle.act()  # ambos usam a mesma policy: mede o poder do personagem
    return battle.winner, battle.turn_number - 1


def simulate(fights, seed, policy_name, arena_id=None):
    """arena_id=None sorteia uma arena por luta; 'all' é sinônimo."""
    rng = random.Random(seed)
    wins = {c: 0 for c in CHARACTERS}
    played = {c: 0 for c in CHARACTERS}
    matrix, turns = {}, []
    for a, b in product(CHARACTERS, CHARACTERS):
        if a == b:
            continue
        w = 0
        for i in range(fights):
            first = Side.PLAYER if i % 2 == 0 else Side.OPPONENT  # remove viés de iniciativa
            arena = arena_id if arena_id not in (None, "all") else rng.choice(list(ARENAS))
            winner, n = fight(a, b, rng, policy_name, first, arena)
            w += winner is Side.PLAYER
            turns.append(n)
        matrix[(a, b)] = w / fights
        wins[a] += w
        wins[b] += fights - w
        played[a] += fights
        played[b] += fights
    rates = {c: wins[c] / played[c] for c in CHARACTERS}
    return rates, matrix, sum(turns) / len(turns)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--fights", type=int, default=2000)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--policy", choices=POLICIES, default="heuristic")
    p.add_argument("--arena", choices=["all", *ARENAS], default="all")
    p.add_argument("--check", action="store_true")
    p.add_argument("--min", type=float, default=0.35, help="win rate mínima aceitável")
    p.add_argument("--max", type=float, default=0.65, help="win rate máxima aceitável")
    p.add_argument("--arena-min", type=float, default=0.30, help="mínima por arena (--check)")
    p.add_argument("--arena-max", type=float, default=0.70, help="máxima por arena (--check)")
    args = p.parse_args(argv)

    rates, matrix, avg_turns = simulate(args.fights, args.seed, args.policy, args.arena)
    print(f"policy={args.policy} arena={args.arena} fights/par={args.fights} seed={args.seed} "
          f"turnos médios={avg_turns:.1f}\n")
    ids = list(CHARACTERS)
    print(f"{'(linha vence coluna)':<22}" + "".join(f"{c:>11}" for c in ids))
    for a in ids:
        print(f"{a:<22}" + "".join(
            f"{'-':>11}" if a == b else f"{matrix[(a, b)]:>10.0%} " for b in ids))
    print("\nWin rate geral:")
    bad = []
    for c, r in sorted(rates.items(), key=lambda kv: -kv[1]):
        flag = "" if args.min <= r <= args.max else "  <-- DESBALANCEADO"
        print(f"  {c:<12}{r:>6.1%}{flag}")
        if flag:
            bad.append(c)
    if args.check and args.arena == "all":  # cada arena também precisa ser jogável
        for arena_id, arena in ARENAS.items():
            arena_rates, _, _ = simulate(args.fights, args.seed, args.policy, arena_id)
            line = " ".join(f"{c}={r:.0%}" for c, r in arena_rates.items())
            off = [c for c, r in arena_rates.items() if not args.arena_min <= r <= args.arena_max]
            print(f"  arena {arena_id:<10}{line}{'  <-- DESBALANCEADA' if off else ''}")
            bad += [f"{arena_id}:{c}" for c in off]
    return 1 if (args.check and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
