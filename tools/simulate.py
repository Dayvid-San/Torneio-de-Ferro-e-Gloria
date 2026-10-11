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

from Game.data.characters import CHARACTERS
from Game.domain.actions import ActionType, Side
from Game.domain.ai import GreedyPolicy, RandomPolicy
from Game.domain.battle import Battle

POLICIES = {"random": lambda rng: RandomPolicy(rng), "greedy": lambda rng: GreedyPolicy()}


def fight(a_id, b_id, rng, policy_name, first=Side.PLAYER):
    battle = Battle(CHARACTERS[a_id].create(), CHARACTERS[b_id].create(), first=first,
                    policy=POLICIES[policy_name](rng), rng=rng)
    while not battle.is_over:
        battle.act()  # ambos usam a mesma policy: mede o poder do personagem
    return battle.winner, battle.turn_number - 1


def simulate(fights, seed, policy_name):
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
            winner, n = fight(a, b, rng, policy_name, first)
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
    p.add_argument("--policy", choices=POLICIES, default="random")
    p.add_argument("--check", action="store_true")
    p.add_argument("--min", type=float, default=0.35, help="win rate mínima aceitável")
    p.add_argument("--max", type=float, default=0.65, help="win rate máxima aceitável")
    args = p.parse_args(argv)

    rates, matrix, avg_turns = simulate(args.fights, args.seed, args.policy)
    print(f"policy={args.policy} fights/par={args.fights} seed={args.seed} "
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
    return 1 if (args.check and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
