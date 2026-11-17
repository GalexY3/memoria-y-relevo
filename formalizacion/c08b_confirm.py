"""C08b confirmation (PREREGISTERED in PREREG_C08B_SOCIALIZACION.md; seeds 8100xx-8106xx).
Question: under the user's original collective signal ('coll'), does socialised entry preserve the
institution after turnover, and through which channel? Entry rules separate the channels:
  social         copy a random incumbent NEIGHBOUR's colour (local transmission)
  social_global  copy a random incumbent ANYWHERE (preserves proportions, no locality)
  incumbent_set  uniform over colours present among incumbents (preserves the colour set only)
  random         uniform over all 16 colours
  new            one colour absent from the community
Plus succession: replace founders in rounds of 30 (30,30,30,10) with social entry until none remain."""
import json, sys, time, hashlib
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H))
from c08_sim import trial_and_revert, counts, dist_D, NB, N

K, X, ACT, EXPL, FRAC = 4, 16, 0.05, 0.1, 0.3
SIGNALS = {'coll': int(sys.argv[1]) if len(sys.argv) > 1 else 4096, 'D': int(sys.argv[2]) if len(sys.argv) > 2 else 1024}
T0 = int(sys.argv[3]) if len(sys.argv) > 3 else 8000
T1 = int(sys.argv[4]) if len(sys.argv) > 4 else 4000
TS = T1 // 2
ENTRIES = ['social', 'social_global', 'incumbent_set', 'random', 'new']

def pick(M, rng, contiguous, pool=None, m=int(FRAC * N)):
    out = np.zeros((M, N), bool)
    for i in range(M):
        if pool is not None:
            cand = np.nonzero(pool[i])[0]; out[i, rng.choice(cand, min(m, len(cand)), replace=False)] = True
        elif contiguous:
            start = int(rng.integers(0, N)); order = [start]; seen = {start}; j = 0
            while len(order) < m:
                for v in NB[order[j]]:
                    if v not in seen and len(order) < m: seen.add(v); order.append(v)
                j += 1
            out[i, order] = True
        else:
            out[i, rng.choice(N, m, replace=False)] = True
    return out

def enter(col, rep, entry, rng):
    col = col.copy(); M = col.shape[0]
    for i in range(M):
        r = np.nonzero(rep[i])[0]; inc = np.nonzero(~rep[i])[0]
        if entry == 'random': col[i, r] = rng.integers(0, X, len(r))
        elif entry == 'new': col[i, r] = np.setdiff1d(np.arange(X), np.unique(col[i, inc]))[0]
        elif entry == 'incumbent_set': col[i, r] = rng.choice(np.unique(col[i, inc]), len(r))
        elif entry == 'social_global': col[i, r] = col[i, rng.choice(inc, len(r))]
        elif entry == 'social':
            todo = list(r); done = ~rep[i].copy()
            while todo:
                nxt = []
                for a in todo:
                    src = [v for v in NB[a] if done[v]]
                    if src: col[i, a] = col[i, src[rng.integers(0, len(src))]]; done[a] = True
                    else: nxt.append(a)
                todo = nxt
    return col

def wilson(k, n, z=1.96):
    if n == 0: return None
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [float(c - h), float(c + h)]

rows, succ = [], []; t0 = time.time()
for gi, (sig, M) in enumerate(SIGNALS.items()):
    col0, _, _, _ = trial_and_revert(M, sig, ACT, EXPL, T=T0, seed=810000 + gi)
    S = dist_D(counts(col0, X), K) == 0; nS = int(S.sum()); print(sig, 'presolved', nS, 'of', M, flush=True)
    for si, contiguous in enumerate([False, True]):
        rep = pick(M, np.random.default_rng(810100 + 10 * gi + si), contiguous)
        for ei, entry in enumerate(ENTRIES):
            col1 = enter(col0, rep, entry, np.random.default_rng(810200 + 100 * gi + 10 * si + ei))
            Dsh = dist_D(counts(col1, X), K)
            col, first, _, occ = trial_and_revert(M, sig, ACT, EXPL, T=T1, seed=810300 + 10 * gi + si, col0=col1)
            k = int((first[S] >= 0).sum())
            rows.append(dict(signal=sig, contiguous=contiguous, entry=entry, M=M, presolved=nS, recovered=k,
                             recovery=(k / nS if nS else None), wilson95=wilson(k, nS),
                             occupancy_presolved=(float(occ[S].mean()) if nS else None),
                             D_shock_presolved=(float(Dsh[S].mean()) if nS else None),
                             median_recovery=(float(np.median(first[S & (first >= 0)])) if k else None)))
            print({a: b for a, b in rows[-1].items()}, flush=True)
    # succession: founders replaced in rounds 30,30,30,10, dispersed, social entry; TS ticks per round
    col = col0.copy(); founder = np.ones((M, N), bool); rng = np.random.default_rng(810500 + gi)
    for rnd, m in enumerate([30, 30, 30, 10]):
        rep = pick(M, rng, False, pool=founder, m=m); founder &= ~rep
        col = enter(col, rep, 'social', rng)
        col, first, _, occ = trial_and_revert(M, sig, ACT, EXPL, T=TS, seed=810600 + 10 * gi + rnd, col0=col)
        alive = dist_D(counts(col, X), K) == 0
        succ.append(dict(signal=sig, round=rnd + 1, founders_left=int(founder[0].sum()), presolved=nS,
                         solved_end_presolved=int((alive & S).sum()), share=(float((alive & S).sum() / nS) if nS else None),
                         wilson95=wilson(int((alive & S).sum()), nS), occupancy_presolved=(float(occ[S].mean()) if nS else None)))
        print(succ[-1], flush=True)
primary = SIGNALS == {'coll': 4096, 'D': 1024} and T0 == 8000 and T1 == 4000
out = H / 'C08_RESULTS' / ('c08b_confirm_PRIMARY.json' if primary else 'c08b_smoke.json')
out.write_text(json.dumps(dict(status='PRIMARY' if primary else 'SMOKE', T0=T0, T1=T1, TS=TS,
    sha256={f: hashlib.sha256((H / f).read_bytes()).hexdigest() for f in ['c08_sim.py', 'c08b_confirm.py']},
    seconds=time.time() - t0, rows=rows, succession=succ), indent=1), encoding='utf-8', newline=chr(10))
print('wrote', out.name, round(time.time() - t0), 's')
