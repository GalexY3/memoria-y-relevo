"""C12 EXPLORATORY pilot (seeds 8180xx, not reused): (A) recovery after 30% random entry, k=4;
(B) continuous turnover s=0.9 then the environment demands k=5."""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c12_sim import run
M = 128; X = 16; t0 = time.time(); out = {}
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, seed=818000); col = col[dist_D(counts(col, X), 4) == 0]; M = col.shape[0]
canon0 = counts(col, X) > 0
rng = np.random.default_rng(818001); rep = np.zeros((M, N), bool)
for i in range(M): rep[i, rng.choice(N, 30, replace=False)] = True
A = []
for mode, th in [('none', 0), ('normative', 0), ('constatative', 3), ('constatative', 8), ('constatative', 15)]:
    r = run(col, mode, 4, 4000, canon0=canon0, theta=th or 5, seed=818002, entry_seed=818003, events={0: rep})
    A.append(dict(mode=mode, theta=th, recovered=float((r['first'] >= 0).mean()), meanD=float(r['meanD'].mean()), canon_size=float(r['canon_size'].mean())))
    print('A', A[-1], flush=True)
B = []
for mode, th in [('none', 0), ('normative', 0), ('constatative', 3), ('constatative', 8), ('constatative', 15)]:
    r1 = run(col, mode, 4, 3000, canon0=canon0, theta=th or 5, tau=80, s=0.9, seed=818004, entry_seed=818005)
    r2 = run(r1['col'], mode, 5, 6000, canon0=r1['canon'], theta=th or 5, tau=80, s=0.9, seed=818006, entry_seed=818007)
    B.append(dict(mode=mode, theta=th, stab_meanD=float(r1['meanD'].mean()), adapt_meanD=float(r2['meanD'].mean()),
                  adapt_ever=float((r2['first'] >= 0).mean()), canon_size_adapt=float(r2['canon_size'].mean())))
    print('B', B[-1], flush=True)
(H / 'C12_RESULTS' / 'pilot_c12.json').write_text(json.dumps(dict(status='EXPLORATORY', M=M, A=A, B=B, seconds=time.time() - t0), indent=1), encoding='utf-8', newline=chr(10))
print('seconds', round(time.time() - t0))
