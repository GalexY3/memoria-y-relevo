"""C13b pilot (EXPLORATORY; seeds 8480xx; not reused): noisy self-description ('order from noise').
Canon rewritten every U ticks from a random sample of n agents (colours with >= r members in the sample, r = 8n/N),
against the exact constatative canon (theta sweep, rewritten every tick). Experiments A (30% shock), B (k 4->5) and
C (k 5->4) as in C13. Usage: python c13b_pilot.py [M]"""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c13x_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 256
X = 16; t0 = time.time(); out = dict(status='PILOT', M=M)
CONDS = [(f'sampled_n{n}_U{U}', 'sampled', dict(n_s=n, r_s=max(1, round(8 * n / N)), U=U)) for n in [12, 25, 50, 100] for U in [1]] + \
        [(f'sampled_n50_U{U}', 'sampled', dict(n_s=50, r_s=4, U=U)) for U in [5, 20]] + \
        [(f'const_t{th}_U1', 'constatative', dict(theta=th, U=1)) for th in [6, 7, 8, 10, 13]] + \
        [('comm_W50', 'communicative', dict(W=50, r=4))]
for tag, k0, k1, sd in [('B', 4, 5, 848000), ('C', 5, 4, 848010)]:
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, k=k0, seed=sd); col = col[dist_D(counts(col, X), k0) == 0]
    canon0 = counts(col, X) > 0; rows = []
    for name, mode, kw in CONDS:
        (b1, b2), _ = run(col, mode, [(k0, 3000), (k1, 6000)], canon0=canon0, tau=80, s=0.9, seed=sd + 2, entry_seed=sd + 3, **kw)
        rows.append(dict(name=name, stab_meanD=float(b1['meanD'].mean()), stab_changes=float(b1['changes_per_1000'].mean()),
                         adapt_meanD=float(b2['meanD'].mean()), adapt_ever=float((b2['first'] >= 0).mean())))
        print(tag, json.dumps(rows[-1]), flush=True)
    out[tag] = rows
# A: homeostasis after a 30% shock
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, seed=848020); col = col[dist_D(counts(col, X), 4) == 0]
canon0 = counts(col, X) > 0; n = col.shape[0]; rng = np.random.default_rng(848021); cs = col.copy(); age0 = np.full((n, N), 10 ** 6, np.int64)
for i in range(n):
    rr = rng.choice(N, 30, replace=False); cs[i, rr] = rng.integers(0, X, 30); age0[i, rr] = 0
rows = []
for name, mode, kw in CONDS:
    (a,), _ = run(cs, mode, [(4, 4000)], canon0=canon0, age0=age0, seed=848022, entry_seed=848023, **kw)
    rows.append(dict(name=name, recovered=float((a['first'] >= 0).mean()), meanD=float(a['meanD'].mean()), changes=float(a['changes_per_1000'].mean())))
    print('A', json.dumps(rows[-1]), flush=True)
out['A'] = rows
(H / 'C13_RESULTS' / 'pilot_c13b.json').write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
