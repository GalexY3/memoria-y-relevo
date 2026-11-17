"""C08 turnover experiment (PREREGISTERED in PREREG_C08_RELEVO.md; seeds 809xxx).
Warm-up with trial-and-revert, replace 30% of agents (dispersed | contiguous) with newcomers whose
entry colour is random | socialised (copied from a random incumbent neighbour = a 'message') | new
(one colour absent from the community), then keep running. Common random numbers across entry rules."""
import json, sys, time, hashlib
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H))
from c08_sim import trial_and_revert, counts, dist_D, NB, N

M = int(sys.argv[1]) if len(sys.argv) > 1 else 256
T0 = T1 = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
K, X, ACT, EXPL, FRAC = 4, 16, 0.05, 0.1, 0.3
MODES = {'D': dict(mode='D'), 'ind': dict(mode='ind'), 'coll': dict(mode='coll'),
         'dilemma_sub': dict(mode='dilemma', bonus=0.005, skew=0.2)}

def prefs(skew, rng):
    p = np.full(K, 1 / K); p[0] += skew; p[1:] -= skew / (K - 1)
    return rng.choice(K, (M, N), p=p)

def pick(rng, contiguous):
    m = int(FRAC * N); out = np.zeros((M, N), bool)
    for i in range(M):
        if contiguous:
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
    col = col.copy()
    if entry == 'random':
        col[rep] = rng.integers(0, X, rep.sum())
    elif entry == 'new':
        for i in range(M):
            absent = np.setdiff1d(np.arange(X), np.unique(col[i, ~rep[i]]))
            col[i, rep[i]] = absent[0]
    elif entry == 'social':          # copy a random incumbent neighbour; newcomers with none wait for socialised ones
        for i in range(M):
            todo = list(np.nonzero(rep[i])[0]); done = ~rep[i].copy()
            while todo:
                nxt = []
                for a in todo:
                    src = [v for v in NB[a] if done[v]]
                    if src: col[i, a] = col[i, src[rng.integers(0, len(src))]]; done[a] = True
                    else: nxt.append(a)
                todo = nxt
    return col

rows = []; t0 = time.time()
for mi, (name, spec) in enumerate(MODES.items()):
    pref = prefs(spec.get('skew', 0.0), np.random.default_rng(809000 + mi)) if spec['mode'] == 'dilemma' else None
    bonus = spec.get('bonus', 0.0)
    col0, _, _, _ = trial_and_revert(M, spec['mode'], ACT, EXPL, T=T0, seed=809010 + mi, pref=pref, bonus=bonus)
    D0 = dist_D(counts(col0, X), K); pre_solved = D0 == 0
    for si, contiguous in enumerate([False, True]):
        rep = pick(np.random.default_rng(809100 + 10 * mi + si), contiguous)
        for ei, entry in enumerate(['random', 'social', 'new']):
            col1 = enter(col0, rep, entry, np.random.default_rng(809200 + 10 * mi + si))
            Dshock = dist_D(counts(col1, X), K)
            col, first, _, occ = trial_and_revert(M, spec['mode'], ACT, EXPL, T=T1, seed=809300 + 10 * mi + si, col0=col1, pref=pref, bonus=bonus)
            D = dist_D(counts(col, X), K); S = pre_solved
            def med(x): return float(np.median(x)) if len(x) else None
            rows.append(dict(signal=name, contiguous=contiguous, entry=entry, M=M, pre_solved=int(S.sum()),
                             D_pre_mean=float(D0.mean()), D_shock_mean=float(Dshock.mean()), D_shock_mean_presolved=(float(Dshock[S].mean()) if S.any() else None),
                             occupancy_all=float(occ.mean()), occupancy_presolved=(float(occ[S].mean()) if S.any() else None),
                             recovered_presolved=(float((first[S] >= 0).mean()) if S.any() else None),
                             median_recovery_presolved=med(first[S & (first >= 0)]), D_final_mean=float(D.mean()),
                             first_presolved=[int(v) for v in first[S]]))
            r = {k: v for k, v in rows[-1].items() if k != 'first_presolved'}; print(r, flush=True)
out = H / 'C08_RESULTS' / f'turnover_M{M}_T{T1}.json'
out.write_text(json.dumps(dict(status='PRIMARY' if (M == 256 and T1 == 4000) else 'SMOKE', script_sha256=hashlib.sha256((H / 'c08_turnover.py').read_bytes()).hexdigest(),
                               sim_sha256=hashlib.sha256((H / 'c08_sim.py').read_bytes()).hexdigest(), seconds=time.time() - t0, rows=rows), indent=1), encoding='utf-8', newline=chr(10))
print('wrote', out.name, round(time.time() - t0), 's')
