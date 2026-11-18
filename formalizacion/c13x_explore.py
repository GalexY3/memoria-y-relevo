"""C13x EXPLORATORY (idea I-021; seeds 8380xx; not preregistered). Is the advantage of the short-memory communicative
canon due to sampling noise or to temporal memory? Compares, in B (k 4->5) and C (k 5->4) with turnover:
  comm W=50 r=4 (rolling memory) | sampled n=50 r=4 every tick (fresh noise, no memory) | sampled every 50 ticks |
  constatative theta=8 every tick and every 50 ticks (no noise).
Usage: python c13x_explore.py [M]"""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c13x_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 256
X = 16; t0 = time.time(); out = {}
CONDS = [('comm_W50', 'communicative', dict(W=50, r=4)), ('sampled_U1', 'sampled', dict(U=1, n_s=50, r_s=4)),
         ('sampled_U10', 'sampled', dict(U=10, n_s=50, r_s=4)), ('sampled_U50', 'sampled', dict(U=50, n_s=50, r_s=4)),
         ('const_t8_U1', 'constatative', dict(theta=8, U=1)), ('const_t8_U50', 'constatative', dict(theta=8, U=50)),
         ('sampled_U1_n100', 'sampled', dict(U=1, n_s=100, r_s=8))]
for tag, k0, k1, sd in [('B', 4, 5, 838000), ('C', 5, 4, 838010)]:
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, k=k0, seed=sd); col = col[dist_D(counts(col, X), k0) == 0]
    canon0 = counts(col, X) > 0; rows = []
    for name, mode, kw in CONDS:
        (b1, b2), _ = run(col, mode, [(k0, 3000), (k1, 6000)], canon0=canon0, tau=80, s=0.9, seed=sd + 2, entry_seed=sd + 3, **kw)
        nv = b2['novel_size'][b2['novel_size'] >= 0]
        rows.append(dict(name=name, n=int(col.shape[0]), stab_meanD=float(b1['meanD'].mean()), stab_changes=float(b1['changes_per_1000'].mean()),
                         adapt_meanD=float(b2['meanD'].mean()), adapt_ever=float((b2['first'] >= 0).mean()),
                         t_canon_k_med=float(np.median(b2['canon_k'][b2['canon_k'] >= 0])) if (b2['canon_k'] >= 0).any() else None,
                         novel_size_med=float(np.median(nv)) if nv.size else None))
        print(tag, json.dumps(rows[-1]), flush=True)
    out[tag] = rows
(H / 'C13_RESULTS' / 'explore_c13x_noise_vs_memory.json').write_text(json.dumps(dict(status='EXPLORATORY', M=M, **out), indent=1), encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
