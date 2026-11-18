"""C13x EXPLORATORY (seeds 8380xx, same institutions as c13x_explore.py): fixed-threshold sweep with the canon
rewritten EVERY tick (U = 1) in B (k 4->5) and C (k 5->4), to separate update cadence from noise and memory."""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c13x_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 256
X = 16; out = {}; t0 = time.time()
for tag, k0, k1, sd in [('B', 4, 5, 838000), ('C', 5, 4, 838010)]:
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, k=k0, seed=sd); col = col[dist_D(counts(col, X), k0) == 0]
    canon0 = counts(col, X) > 0; rows = []
    for th in [5, 6, 7, 8, 10, 12, 13]:
        (b1, b2), _ = run(col, 'constatative', [(k0, 3000), (k1, 6000)], canon0=canon0, theta=th, U=1, tau=80, s=0.9, seed=sd + 2, entry_seed=sd + 3)
        rows.append(dict(theta=th, adapt_meanD=float(b2['meanD'].mean()), adapt_ever=float((b2['first'] >= 0).mean())))
        print(tag, json.dumps(rows[-1]), flush=True)
    out[tag] = rows
(H / 'C13_RESULTS' / 'explore_c13x_theta_U1.json').write_text(json.dumps(dict(status='EXPLORATORY', M=M, **out), indent=1), encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
