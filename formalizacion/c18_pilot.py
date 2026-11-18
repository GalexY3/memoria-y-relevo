"""C18 pilot (EXPLORATORY; seeds 8801xx): founding-size staircase j* = max(v_min, j_lam) of Corollary 8.1.
C16 setting on the frozen C17 simulator: no turnover, k = 4 (1000 ticks) then k = 5 (T = 20, 6000 ticks).
Usage: python c18_pilot.py [M]"""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H.parent / 'claude_cycle17')); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D
from c17_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 128
X = 16; t0 = time.time(); rows = []
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=6000, k=4, seed=880100); col = col[dist_D(counts(col, X), 4) == 0]
grid = [(lam, 1.0, v) for v in (1, 2, 3, 4) for lam in (1.0, 0.9, 0.8, 0.7)]
grid += [(lam, 0.0, 3) for lam in (1.0, 0.9, 0.8, 0.75, 0.7, 0.65)] + [(1.0, q, v) for q in (0.2, 0.5) for v in (2, 3)]
for lam, q, v in grid:
    (b1, b2), _ = run(col, 'mix', [(4, 1000), (5, 6000)], lam=lam, tau=0, q=q, v_min=v, seed=880102, entry_seed=880103)
    f = b2['first']
    r = dict(lam=lam, q=q, v_min=v, n=int(col.shape[0]), adapt_ever=float((f >= 0).mean()),
             t_med=float(np.median(f[f >= 0])) if (f >= 0).any() else None, adapt_meanD=float(b2['meanD'].mean()), secs=round(time.time() - t0))
    rows.append(r); print(json.dumps(r), flush=True)
(H / 'C18_RESULTS' / 'pilot_c18.json').write_text(json.dumps(dict(status='PILOT', M=M, rows=rows), indent=1), encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
