"""C12 confirmation (PREREGISTERED in PREREG_C12_AUTODESCRIPCION.md; seeds 8190xx).
Usage: python c12_confirm.py [M] [scale]"""
import json, sys, time, hashlib
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c12_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 512
SC = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
X = 16; t0 = time.time()
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=int(4000 * SC), seed=819000); col = col[dist_D(counts(col, X), 4) == 0]; n = int(col.shape[0])
canon0 = counts(col, X) > 0
rng = np.random.default_rng(819001); rep = np.zeros((n, N), bool)
for i in range(n): rep[i, rng.choice(N, 30, replace=False)] = True
CONDS = [('none', None), ('normative', None)] + [('constatative', th) for th in [2, 3, 5, 8, 12, 15, 20]]
A, B = [], []
for mode, th in CONDS:
    r = run(col, mode, 4, int(4000 * SC), canon0=canon0, theta=th or 5, seed=819002, entry_seed=819003, events={0: rep})
    A.append(dict(mode=mode, theta=th, n=n, recovered=float((r['first'] >= 0).mean()), meanD=float(r['meanD'].mean()), canon_size=float(r['canon_size'].mean())))
    print('A', A[-1], flush=True)
for mode, th in CONDS:
    r1 = run(col, mode, 4, int(3000 * SC), canon0=canon0, theta=th or 5, tau=80, s=0.9, seed=819004, entry_seed=819005)
    r2 = run(r1['col'], mode, 5, int(6000 * SC), canon0=r1['canon'], theta=th or 5, tau=80, s=0.9, seed=819006, entry_seed=819007)
    B.append(dict(mode=mode, theta=th, n=n, stab_meanD=float(r1['meanD'].mean()), adapt_meanD=float(r2['meanD'].mean()),
                  adapt_ever=float((r2['first'] >= 0).mean()), canon_size_adapt=float(r2['canon_size'].mean())))
    print('B', B[-1], flush=True)
status = 'PRIMARY' if (M == 512 and SC == 1.0) else 'SMOKE'
(H / 'C12_RESULTS' / f'c12_{status}.json').write_text(json.dumps(dict(status=status, n=n, A=A, B=B, seconds=time.time() - t0,
    sha256={f: hashlib.sha256((H / f).read_bytes()).hexdigest() for f in ['c12_sim.py', 'c12_confirm.py']}), indent=1), encoding='utf-8', newline=chr(10))
print('done', status, round(time.time() - t0), 's')
