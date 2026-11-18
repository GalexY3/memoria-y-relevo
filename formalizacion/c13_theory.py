"""C13 exhaustive check of the relief landscape (Proposition 4 of TEOREMA_C13.md).
With the relief canon at its best response, the potential is F*(s) = sum_c min(s_c, |s_c - T|). For every partition of N
into at most X parts we classify the state under single-agent moves (one agent from colour a to colour b, b existing or
empty while fewer than X colours are used):
  global  F* = 0
  descent some move strictly lowers F*
  plateau no move lowers F*, some move keeps it (F* > 0)
  trap    every move raises F* (F* > 0)
and, for comparison, the same classification under the original collective signal C = sum_present |s_c - T| and under
the fixed-threshold canon with theta (canon = colours with s >= theta, re-evaluated after the move).
Usage: python c13_theory.py"""
import json, sys
from pathlib import Path

def partitions(n, maxpart, maxlen):
    if n == 0:
        yield (); return
    if maxlen == 0:
        return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - p, p, maxlen - 1):
            yield (p,) + rest

def F_relief(s, T):
    return sum(min(x, abs(x - T)) for x in s)

def F_C(s, T):
    return sum(abs(x - T) for x in s if x > 0)

def F_theta(theta):
    return lambda s, T: sum(abs(x - T) if x >= theta else x for x in s)

def classify(s, T, X, F):
    f0 = F(s, T)
    if abs(f0) < 1e-9:
        return 'global'
    s = list(s); best = None
    targets = list(range(len(s))) + ([None] if len(s) < X else [])
    for a in range(len(s)):
        for b in targets:
            if b == a:
                continue
            t = s[:]; t[a] -= 1
            if b is None:
                t.append(1)
            else:
                t[b] += 1
            t = [x for x in t if x > 0]
            d = F(t, T) - f0
            best = d if best is None else min(best, d)
            if best < -1e-9:
                return 'descent'
    return 'plateau' if abs(best) < 1e-9 else 'trap'

def main():
    out = {}
    for (N, k) in [(12, 3), (16, 4), (20, 4), (20, 5), (24, 4), (30, 5), (32, 4), (40, 4), (40, 5)]:
        T = N / k; X = 16; res = {}
        for name, F in [('relief', F_relief), ('C', F_C), ('theta_T/3', F_theta(round(T / 3))), ('theta_T/2+1', F_theta(int(T // 2) + 1))]:
            cnt = dict(global_=0, descent=0, plateau=0, trap=0); ex = {}
            for s in partitions(N, N, X):
                c = classify(s, T, X, F); key = 'global_' if c == 'global' else c
                cnt[key] += 1
                if c in ('plateau', 'trap') and c not in ex:
                    ex[c] = list(s)
            res[name] = dict(counts=cnt, example=ex)
        out[f'N{N}_k{k}'] = res
        print(N, k, {n: r['counts'] for n, r in res.items()}, flush=True)
    Path(__file__).resolve().parent.joinpath('C13_RESULTS', 'c13_theory.json').write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))

if __name__ == '__main__':
    main()
