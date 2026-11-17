"""C08 EXPLORATORY pilot (seeds 8082xx; never reused for confirmation). Reproduces the solvability table."""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H))
from c08_sim import trial_and_revert, counts, dist_D
rows = []; t0 = time.time()
for mode in ['ind', 'coll', 'D']:
    for act in [0.05, 0.2]:
        for ex in [0.1, 0.5]:
            col, first, _, occ = trial_and_revert(128, mode, act, ex, T=8000, seed=808200 + len(rows))
            D = dist_D(counts(col, 16), 4)
            rows.append(dict(mode=mode, act=act, explore=ex, solved_final=float((D == 0).mean()), ever=float((first >= 0).mean()), occupancy=float(occ.mean()),
                             median_first=(float(np.median(first[first >= 0])) if (first >= 0).any() else None),
                             mean_D=float(D.mean()), mean_colours=float((counts(col, 16) > 0).sum(1).mean())))
            print(rows[-1], flush=True)
(H / 'C08_RESULTS').mkdir(exist_ok=True)
(H / 'C08_RESULTS' / 'pilot_trial_and_revert.json').write_text(json.dumps(dict(status='EXPLORATORY', M=128, T=8000, rows=rows, seconds=time.time() - t0), indent=1), encoding='utf-8', newline=chr(10))
