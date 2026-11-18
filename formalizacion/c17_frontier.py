"""C17 frontier exploration (EXPLORATORY; seeds 8703xx): stability-adaptation trade-off of each compensator under C
(socialisation s, sanction q, crystallisation c alone), and sanction under D. Usage: python c17_frontier.py [M]"""
import json, sys, time
from pathlib import Path
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D
from c17_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 64
t0 = time.time(); rows = []
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, seed=870300); col = col[dist_D(counts(col, 16), 4) == 0]
cases = ([('C', 's', dict(s=v)) for v in (0.9, 0.97, 0.98, 0.99)] + [('C', 'q', dict(s=0.0, q=v)) for v in (0.1, 0.3, 0.4, 0.7)]
         + [('C', 'c', dict(s=0.0, cryst=v)) for v in (0.9, 0.98, 0.99)] + [('D', 'q', dict(s=0.0, q=v, lam=1.0)) for v in (0.5, 1.0)])
for sig, kind, kw in cases:
    (b1, b2), _ = run(col, 'none' if sig == 'C' else 'mix', [(4, 4000), (5, 6000)], tau=20, seed=870302, entry_seed=870303, **kw)
    r = dict(signal=sig, kind=kind, **kw, n=int(col.shape[0]), stab_meanD=round(float(b1['meanD'].mean()), 2),
             adapt_meanD=round(float(b2['meanD'].mean()), 2), adapt_ever=round(float((b2['first'] >= 0).mean()), 3), secs=round(time.time() - t0))
    rows.append(r); print(json.dumps(r), flush=True)
(H / 'C17_RESULTS' / 'frontier_c17.json').write_text(json.dumps(dict(status='EXPLORATORY', rows=rows), indent=1), encoding='utf-8', newline=chr(10))
