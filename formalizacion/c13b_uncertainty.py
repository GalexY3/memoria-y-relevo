"""C13b uncertainty (post hoc, for the preprint): re-runs the key preregistered conditions of c13b_confirm.py with the
same seeds (identical results by construction) but keeps per-community errors, and reports paired bootstrap CIs
(communities resampled, 2000 draws, seed 13) for the creating + dissolving sums and their differences.
Usage: python c13b_uncertainty.py"""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c13x_sim import run
M = 512; X = 16; t0 = time.time()
CONDS = [('sampled_n50_U1', 'sampled', dict(n_s=50, r_s=4, U=1)), ('sampled_n100_U1', 'sampled', dict(n_s=100, r_s=8, U=1)),
         ('const_t8_U1', 'constatative', dict(theta=8, U=1)), ('const_t9_U1', 'constatative', dict(theta=9, U=1)),
         ('comm_W50', 'communicative', dict(W=50, r=4))]
per = {}
for PART, k0, k1, sd in [('B', 4, 5, 849000), ('C', 5, 4, 849010)]:
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, k=k0, seed=sd); col = col[dist_D(counts(col, X), k0) == 0]
    canon0 = counts(col, X) > 0
    for name, mode, kw in CONDS:
        (b1, b2), _ = run(col, mode, [(k0, 3000), (k1, 6000)], canon0=canon0, tau=80, s=0.9, seed=sd + 2, entry_seed=sd + 3, **kw)
        per[(PART, name)] = b2['meanD']
        print(PART, name, round(float(b2['meanD'].mean()), 3), round(time.time() - t0), 's', flush=True)
rng = np.random.default_rng(13); out = dict(status='POST_HOC_UNCERTAINTY', B_n=int(len(per[('B', 'const_t8_U1')])), C_n=int(len(per[('C', 'const_t8_U1')])))
def boot(fun, nB, nC):
    v = []
    for _ in range(2000):
        ib = rng.integers(0, nB, nB); ic = rng.integers(0, nC, nC); v.append(fun(ib, ic))
    v = np.sort(v); return [float(v[int(0.025 * 1999)]), float(v[int(0.975 * 1999)])]
nB, nC = out['B_n'], out['C_n']
for name, _, _ in CONDS:
    s = lambda ib, ic, n=name: per[('B', n)][ib].mean() + per[('C', n)][ic].mean()
    out[name] = dict(sum=float(per[('B', name)].mean() + per[('C', name)].mean()), ci95=boot(s, nB, nC))
for a, b in [('sampled_n50_U1', 'const_t8_U1'), ('sampled_n50_U1', 'const_t9_U1'), ('sampled_n50_U1', 'comm_W50'), ('sampled_n50_U1', 'sampled_n100_U1')]:
    d = lambda ib, ic: (per[('B', a)][ib].mean() + per[('C', a)][ic].mean()) - (per[('B', b)][ib].mean() + per[('C', b)][ic].mean())
    out[f'{a}_minus_{b}'] = dict(diff=float(d(np.arange(nB), np.arange(nC))), ci95_paired=boot(d, nB, nC))
(H / 'C13_RESULTS' / 'c13b_uncertainty.json').write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print(json.dumps({k: v for k, v in out.items() if isinstance(v, dict)}, indent=1))
