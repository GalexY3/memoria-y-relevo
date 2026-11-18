"""C18 confirmation (PREREG_C18_UMBRAL_DE_SANCION.md; new seeds 8811xx and 8812xx, M = 512) on the frozen C17 simulator.
  stair  C16 setting, no turnover: k = 4 (1000 ticks) then k = 5 (T = 20, 6000 ticks); q = 1 x v_min in {1..4} x lam in {1, .9, .8, .7};
         references without sanction (lam in {1, .9, .8, .75, .7, .65}); moderate sanction q in {0.2, 0.5} at lam = 1, v_min in {2, 3}
  rot    Corollary 8.2: signal C with turnover (tau = 20, c = 0.95, s = 0), q = 0 and q = 1 with v_min in {1, 2, 3}
The exact check of Proposition 8 is c18_theory.py 8000 881000. Usage: python c18_confirm.py stair|rot [M]"""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H.parent / 'claude_cycle17')); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D
from c17_sim import run
part = sys.argv[1]; M = int(sys.argv[2]) if len(sys.argv) > 2 else 512; tag = 'PRIMARY' if M == 512 else 'SMOKE'
X = 16; t0 = time.time(); rows = []
if part == 'stair':
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=6000, k=4, seed=881100); col = col[dist_D(counts(col, X), 4) == 0]
    grid = [(lam, 1.0, v) for v in (1, 2, 3, 4) for lam in (1.0, 0.9, 0.8, 0.7)]
    grid += [(lam, 0.0, 3) for lam in (1.0, 0.9, 0.8, 0.75, 0.7, 0.65)] + [(1.0, q, v) for q in (0.2, 0.5) for v in (2, 3)]
    for lam, q, v in grid:
        (b1, b2), _ = run(col, 'mix', [(4, 1000), (5, 6000)], lam=lam, tau=0, q=q, v_min=v, seed=881102, entry_seed=881103)
        f = b2['first']
        r = dict(lam=lam, q=q, v_min=v, n=int(col.shape[0]), adapt_ever=float((f >= 0).mean()),
                 t_med=float(np.median(f[f >= 0])) if (f >= 0).any() else None, adapt_meanD=float(b2['meanD'].mean()), secs=round(time.time() - t0))
        rows.append(r); print(json.dumps(r), flush=True)
else:
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, seed=881200); col = col[dist_D(counts(col, X), 4) == 0]
    for q, v in [(0.0, 3), (1.0, 1), (1.0, 2), (1.0, 3)]:
        (b1, b2), _ = run(col, 'none', [(4, 4000), (5, 6000)], tau=20, s=0.0, cryst=0.95, q=q, v_min=v, seed=881202, entry_seed=881203)
        r = dict(q=q, v_min=v, n=int(col.shape[0]), stab_meanD=float(b1['meanD'].mean()), adapt_ever=float((b2['first'] >= 0).mean()), secs=round(time.time() - t0))
        rows.append(r); print(json.dumps(r), flush=True)
(H / 'C18_RESULTS' / f'c18_{tag}_{part}.json').write_text(json.dumps(dict(status=tag, part=part, M=M, rows=rows), indent=1), encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
