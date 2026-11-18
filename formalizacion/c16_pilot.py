"""C16 pilot (EXPLORATORY; seeds 8600xx): requisite model fraction. Signal (1-lam) C + lam D. Creation k0 -> k1 with
institutions k0 x T0 and no turnover (tau = 0) or socialised turnover (tau = 80, s = 1); theory: creation needs
lam > 1 - 2/T1 (single-agent move); dissolution k 5 -> 4 needs any lam > 0. Usage: python c16_pilot.py [M]"""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c16_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 128
X = 16; t0 = time.time(); rows = []
for (k0, k1, sd) in [(4, 5, 860000), (5, 4, 860010), (5, 10, 860020)]:
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=6000, k=k0, seed=sd); col = col[dist_D(counts(col, X), k0) == 0]; n = col.shape[0]
    T1 = N / k1; lstar = 1 - 2 / T1
    for lam in [0.0, 0.05, 0.5, 0.7, 0.75, 0.8, 0.85, 0.88, 0.9, 0.92, 0.95, 1.0]:
        for tau in (0, 80):
            (b1, b2), _ = run(col, 'mix', [(k0, 1000), (k1, 6000)], lam=lam, tau=tau, s=1.0, seed=sd + 2, entry_seed=sd + 3)
            r = dict(change=f'{k0}->{k1}', lam=lam, lam_star=lstar, tau=tau, n=int(n), adapt_ever=float((b2['first'] >= 0).mean()),
                     adapt_meanD=float(b2['meanD'].mean()), t_med=float(np.median(b2['first'][b2['first'] >= 0])) if (b2['first'] >= 0).any() else None)
            rows.append(r); print(json.dumps(r), flush=True)
(H / 'C16_RESULTS' / 'pilot_c16.json').write_text(json.dumps(dict(status='PILOT', M=M, rows=rows), indent=1), encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
