"""C10 EXPLORATORY pilot (seeds 8150xx, never reused): stability (k=4) then adaptation (k=5)."""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D
from c10_sim import run_phases
M = 128; X = 16; t0 = time.time()
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, seed=815000); col = col[dist_D(counts(col, X), 4) == 0]
rows = []
for tau in [20, 80]:
    for sig in ['coll', 'D']:
        for s in [0.0, 0.5, 0.9, 1.0]:
            res, _ = run_phases(col, [(sig, 4, 4000), (sig, 5, 6000)], s, tau, seed=815100, entry_seed=815200)
            a, b = res
            rows.append(dict(tau=tau, signal=sig, s=s, stab_meanD=float(a['meanD'].mean()), stab_occ=float(a['occupancy'].mean()),
                             stab_colours=float(a['mean_colours'].mean()), adapt_meanD=float(b['meanD'].mean()),
                             adapt_ever=float((b['first'] >= 0).mean()), adapt_occ=float(b['occupancy'].mean()), adapt_colours=float(b['mean_colours'].mean())))
            print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in rows[-1].items()}, flush=True)
(H / 'C10_RESULTS' / 'pilot_c10.json').write_text(json.dumps(dict(status='EXPLORATORY', M=int(col.shape[0]), rows=rows, seconds=time.time() - t0), indent=1), encoding='utf-8', newline=chr(10))
