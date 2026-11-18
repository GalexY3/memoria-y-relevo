"""C17 pilot (EXPLORATORY; seeds 8700xx): compensatory robustness inside the model (TFG Annex I, entries 2 and 27).
Institutions 4x25; continuous re-entry every tau = 20 ticks; crystallisation c = prob. a re-entering member returns as
itself; collective compensation by socialisation s (at entry) or symbolic sanction q (per tick). Signal C ('none') or
D ('mix', lam = 1). Stable phase k = 4 (4000 ticks), then the environment asks k = 5 (6000 ticks).
Usage: python c17_pilot.py [M]"""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c17_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 128
X = 16; t0 = time.time(); rows = []
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, seed=870000); col = col[dist_D(counts(col, X), 4) == 0]; n = col.shape[0]
for sig, mode, kw0 in [('C', 'none', {}), ('D', 'mix', dict(lam=1.0))]:
    for c in [0.0, 0.5, 0.8, 0.95]:
        grid = [('s', s_, 0.0) for s_ in [0.0, 0.5, 0.8, 0.95, 1.0]] + [('q', 0.0, q_) for q_ in [0.01, 0.05, 0.2]]
        for kind, s_, q_ in grid:
            (b1, b2), _ = run(col, mode, [(4, 4000), (5, 6000)], tau=20, s=s_, cryst=c, q=q_, seed=870002, entry_seed=870003, **kw0)
            r = dict(signal=sig, c=c, kind=kind, s=s_, q=q_, n=int(n), stab_meanD=float(b1['meanD'].mean()),
                     adapt_meanD=float(b2['meanD'].mean()), adapt_ever=float((b2['first'] >= 0).mean()), secs=round(time.time() - t0))
            rows.append(r); print(json.dumps(r), flush=True)
(H / 'C17_RESULTS' / 'pilot_c17.json').write_text(json.dumps(dict(status='PILOT', M=M, rows=rows), indent=1), encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
