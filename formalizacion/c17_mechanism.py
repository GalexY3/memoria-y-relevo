"""C17 mechanism probe (EXPLORATORY; seeds 8702xx). Where does the variety for creating the 5th category come from
under signal C with sanction? Knock-outs: no turnover (tau = 0), socialised newcomers only (s = 1), and sanction
with v_min = 1 (inactive) vs 3. Usage: python c17_mechanism.py [M]"""
import json, sys, time
from pathlib import Path
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D
from c17_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 48
t0 = time.time(); rows = []
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, seed=870200); col = col[dist_D(counts(col, 16), 4) == 0]
cases = [('baseline q=0.2', dict(tau=20, s=0.0, q=0.2)),
         ('no turnover, q=0.2', dict(tau=0, s=0.0, q=0.2)),
         ('socialised newcomers, q=0.2', dict(tau=20, s=1.0, q=0.2)),
         ('q=0.2, v_min=2', dict(tau=20, s=0.0, q=0.2, v_min=2)),
         ('q=0.2, v_min=5', dict(tau=20, s=0.0, q=0.2, v_min=5)),
         ('q=0.5', dict(tau=20, s=0.0, q=0.5)),
         ('q=1.0', dict(tau=20, s=0.0, q=1.0))]
for name, kw in cases:
    (b1, b2), _ = run(col, 'none', [(4, 4000), (5, 6000)], seed=870202, entry_seed=870203, **kw)
    r = dict(case=name, n=int(col.shape[0]), stab_meanD=round(float(b1['meanD'].mean()), 2), adapt_meanD=round(float(b2['meanD'].mean()), 2),
             adapt_ever=round(float((b2['first'] >= 0).mean()), 3), secs=round(time.time() - t0))
    rows.append(r); print(json.dumps(r), flush=True)
(H / 'C17_RESULTS' / 'mechanism_c17.json').write_text(json.dumps(dict(status='EXPLORATORY', rows=rows), indent=1), encoding='utf-8', newline=chr(10))
