"""C15 pilot (EXPLORATORY; seeds 8500xx): Ashby ultrastability of the self-description. Normative canon + a random
second-order loop (patience L, bound b on the malaise F) versus no loop, informed decree (d = 0) and the bottom-up
noisy canon. B: k 4->5, C: k 5->4, turnover tau = 80, s = 0.9; 3000 ticks before the change, 12000 after.
Usage: python c15_pilot.py [M]"""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c15_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 256
X = 16; t0 = time.time(); rows = []
for tag, k0, k1, sd in [('B', 4, 5, 850000), ('C', 5, 4, 850010)]:
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, k=k0, seed=sd); col = col[dist_D(counts(col, X), k0) == 0]
    canon0 = counts(col, X) > 0; n = col.shape[0]
    conds = [(f'ultra_L{L}', 'ultrastable', dict(L=L, b=0.05)) for L in [25, 50, 100, 200, 400]] + \
            [('no_loop', 'normative', {}), ('sampled_n50', 'sampled', dict(n_s=50, r_s=4, U=1))]
    for name, mode, kw in conds:
        (b1, b2), _ = run(col, mode, [(k0, 3000), (k1, 12000)], canon0=canon0, tau=80, s=0.9, seed=sd + 2, entry_seed=sd + 3, **kw)
        r = dict(exp=tag, name=name, n=int(n), stab_meanD=float(b1['meanD'].mean()), stab_steps=float(b1['us_steps'].mean()),
                 adapt_meanD=float(b2['meanD'].mean()), adapt_ever=float((b2['first'] >= 0).mean()),
                 t_D0_med=float(np.median(b2['first'][b2['first'] >= 0])) if (b2['first'] >= 0).any() else None,
                 steps_mean=float(b2['us_steps'].mean()), steps_med=float(np.median(b2['us_steps'])),
                 final_canon=float(b2['canon_size'].mean()))
        rows.append(r); print(json.dumps(r), flush=True)
(H / 'C15_RESULTS' / 'pilot_c15.json').write_text(json.dumps(dict(status='PILOT', M=M, rows=rows), indent=1), encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
