"""C13x EXPLORATORY (idea I-027; seeds 8385xx; not preregistered): scale. Relief (threshold T/2, scale-invariant)
against fixed thresholds that are absolute (theta = 8) or relative to the new target size (T/4, T/3, T/2 + 1), for
four environmental changes on N = 100: create 2->4 and 5->10, dissolve 4->2 and 10->5. Turnover tau = 80, s = 0.9.
Usage: python c13x_scale.py [M]"""
import json, sys, time, math
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c13x_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 256
X = 16; t0 = time.time(); out = dict(status='EXPLORATORY', M=M, rows=[])
for (k0, k1, sd) in [(2, 4, 838500), (5, 10, 838510), (4, 2, 838520), (10, 5, 838530)]:
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=6000, k=k0, seed=sd); col = col[dist_D(counts(col, X), k0) == 0]
    if col.shape[0] < 20:
        print('few institutions', k0, col.shape[0], flush=True); continue
    canon0 = counts(col, X) > 0; T1 = N / k1
    conds = [('relief', 'reflexive', {}), ('theta8_abs', 'constatative', dict(theta=8, U=1)),
             ('theta_T/4', 'constatative', dict(theta=max(2, round(T1 / 4)), U=1)),
             ('theta_T/3', 'constatative', dict(theta=max(2, round(T1 / 3)), U=1)),
             ('theta_T/2+1', 'constatative', dict(theta=int(T1 // 2) + 1, U=1))]
    for name, mode, kw in conds:
        (b1, b2), _ = run(col, mode, [(k0, 3000), (k1, 6000)], canon0=canon0, tau=80, s=0.9, seed=sd + 2, entry_seed=sd + 3, **kw)
        r = dict(change=f'{k0}->{k1}', T_new=T1, name=name, theta=kw.get('theta'), n=int(col.shape[0]), stab_meanD=float(b1['meanD'].mean()),
                 adapt_meanD=float(b2['meanD'].mean()), adapt_ever=float((b2['first'] >= 0).mean()),
                 t_canon_k=float(np.median(b2['canon_k'][b2['canon_k'] >= 0])) if (b2['canon_k'] >= 0).any() else None)
        out['rows'].append(r); print(json.dumps(r), flush=True)
(H / 'C13_RESULTS' / 'explore_c13x_scale.json').write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
