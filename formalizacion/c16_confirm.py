"""C16 confirmation (PREREGISTERED in PREREG_C16_FRACCION_DE_MODELO.md; seeds 8610xx). No turnover (tau = 0).
Usage: python c16_confirm.py [M]"""
import json, sys, time, hashlib
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c16_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 512
X = 16; t0 = time.time(); rows = []
GRID = {(4, 5): [0.0, 0.3, 0.55, 0.65, 0.7, 0.75, 0.79, 0.8, 0.85, 0.89, 0.9, 1.0],
        (5, 10): [0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 1.0],
        (5, 4): [0.0, 0.05, 0.1, 0.5, 1.0]}
for (k0, k1), sd in [((4, 5), 861000), ((5, 10), 861020), ((5, 4), 861010)]:
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=6000, k=k0, seed=sd); col = col[dist_D(counts(col, X), k0) == 0]; n = col.shape[0]
    for lam in GRID[(k0, k1)]:
        (b1, b2), _ = run(col, 'mix', [(k0, 1000), (k1, 6000)], lam=lam, tau=0, seed=sd + 2, entry_seed=sd + 3)
        f = b2['first']
        r = dict(change=f'{k0}->{k1}', lam=lam, n=int(n), adapt_ever=float((f >= 0).mean()), adapt_meanD=float(b2['meanD'].mean()),
                 t_med=float(np.median(f[f >= 0])) if (f >= 0).any() else None, secs=round(time.time() - t0))
        rows.append(r); print(json.dumps(r), flush=True)
out = dict(status='PRIMARY' if M == 512 else 'SMOKE', M=M, rows=rows, seconds=round(time.time() - t0),
           sha256={f: hashlib.sha256((H / f).read_bytes()).hexdigest() for f in ['c16_sim.py', 'c16_confirm.py']})
(H / 'C16_RESULTS' / f"c16_{out['status']}.json").write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print('done', out['status'], out['seconds'], 's')
