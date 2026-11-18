"""C13 pilot, experiment C (EXPLORATORY; seeds 8281xx): de-differentiation. Institutions 5x20 with turnover
(tau=80, s=0.9) for 3000 ticks, then the environment requires k=4 for 6000 ticks: one category must be forgotten.
Usage: python c13_pilot_c.py [M] [scale]"""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c13_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 128
SC = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
X = 16; t0 = time.time()
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=int(4000 * SC), k=5, seed=828100); col = col[dist_D(counts(col, X), 5) == 0]; n = int(col.shape[0])
canon0 = counts(col, X) > 0
CONDS = [dict(name='none', mode='none'), dict(name='normative', mode='normative'),
         dict(name='const_t8', mode='constatative', theta=8), dict(name='const_half', mode='constatative', theta='half'),
         dict(name='reflexive', mode='reflexive'),
         dict(name='comm_W50_r4', mode='communicative', W=50, r=4), dict(name='comm_W200_r16', mode='communicative', W=200, r=16),
         dict(name='comm_W800_r64', mode='communicative', W=800, r=64)]
def med(a):
    a = a[a >= 0]; return float(np.median(a)) if a.size else None
res = []
for c in CONDS:
    kw = {k: v for k, v in c.items() if k not in ('name', 'mode')}
    (b1, b2), _ = run(col, c['mode'], [(5, int(3000 * SC)), (4, int(6000 * SC))], canon0=canon0, tau=80, s=0.9,
                      seed=828104, entry_seed=828105, **kw)
    row = dict(name=c['name'], n=n, C_stab_meanD=float(b1['meanD'].mean()), C_adapt_meanD=float(b2['meanD'].mean()),
               C_adapt_ever=float((b2['first'] >= 0).mean()), C_t_D0_med=med(b2['first']), C_t_canon4_med=med(b2['canon_k']),
               C_canon=float(b2['canon_size'].mean()), C_changes=float(b2['changes_per_1000'].mean()), secs=round(time.time() - t0))
    res.append(row); print(json.dumps(row), flush=True)
(H / 'C13_RESULTS' / 'pilot_c13_C.json').write_text(json.dumps(dict(status='PILOT', M=M, scale=SC, n=n, rows=res), indent=1), encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
