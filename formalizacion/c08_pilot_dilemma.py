"""C08 EXPLORATORY dilemma pilot (seeds 8083xx). Private bonus for a preferred colour among 0..k-1 with
skewed preferences: balance (4x25) requires some agents to give up their preferred colour."""
import json, sys
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H))
from c08_sim import trial_and_revert, counts, dist_D, N
def prefs(M, k, skew, rng):
    p = np.full(k, 1 / k); p[0] += skew; p[1:] -= skew / (k - 1)
    return rng.choice(k, (M, N), p=p)
rows = []
for skew in [0.0, 0.2]:
    for bonus in [0.002, 0.005, 0.02]:
        rng = np.random.default_rng(808300 + len(rows)); pref = prefs(128, 4, skew, rng)
        col, first, _, occ = trial_and_revert(128, 'dilemma', 0.05, 0.1, T=8000, seed=808350 + len(rows), pref=pref, bonus=bonus)
        D = dist_D(counts(col, 16), 4)
        rows.append(dict(skew=skew, bonus=bonus, solved=float((D == 0).mean()), ever=float((first >= 0).mean()), occupancy=float(occ.mean()),
                         mean_D=float(D.mean()), at_pref=float((col == pref).mean())))
        print(rows[-1], flush=True)
(H / 'C08_RESULTS' / 'pilot_dilemma.json').write_text(json.dumps(dict(status='EXPLORATORY', rows=rows), indent=1), encoding='utf-8', newline=chr(10))
