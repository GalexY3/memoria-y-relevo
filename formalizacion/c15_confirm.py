"""C15 confirmation (PREREGISTERED in PREREG_C15_ULTRAESTABILIDAD.md; seeds 8510xx): Ashby ultrastability of the
self-description. Usage: python c15_confirm.py [M]"""
import json, sys, time, hashlib
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c15_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 512
X = 16; t0 = time.time(); rows = []
for tag, k0, k1, sd in [('B', 4, 5, 851000), ('C', 5, 4, 851010)]:
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, k=k0, seed=sd); col = col[dist_D(counts(col, X), k0) == 0]
    canon0 = counts(col, X) > 0; n = col.shape[0]
    conds = [(f'ultra_L{L}', 'ultrastable', dict(L=L, b=0.05)) for L in [100, 200, 400, 800]] + [('no_loop', 'normative', {})]
    for name, mode, kw in conds:
        (b1, b2), _ = run(col, mode, [(k0, 3000), (k1, 12000)], canon0=canon0, tau=80, s=0.9, seed=sd + 2, entry_seed=sd + 3, **kw)
        st = b2['us_steps']
        r = dict(exp=tag, name=name, n=int(n), stab_meanD=float(b1['meanD'].mean()), stab_any_step=float((b1['us_steps'] > 0).mean()),
                 adapt_meanD=float(b2['meanD'].mean()), adapt_ever=float((b2['first'] >= 0).mean()),
                 steps_mean=float(st.mean()), steps_med=float(np.median(st)), share_one_step=float((st == 1).mean()),
                 steps_hist=[int((st == j).sum()) for j in range(0, 11)], secs=round(time.time() - t0))
        rows.append(r); print(json.dumps(r), flush=True)
out = dict(status='PRIMARY' if M == 512 else 'SMOKE', M=M, rows=rows, seconds=round(time.time() - t0),
           sha256={f: hashlib.sha256((H / f).read_bytes()).hexdigest() for f in ['c15_sim.py', 'c15_confirm.py']})
(H / 'C15_RESULTS' / f"c15_{out['status']}.json").write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print('done', out['status'], out['seconds'], 's')
