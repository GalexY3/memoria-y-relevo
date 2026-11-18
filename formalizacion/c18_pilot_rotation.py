"""C18 pilot (EXPLORATORY; seeds 8802xx) of Corollary 8.2: under C with turnover (tau = 20, c = 0.95, s = 0), total sanction
(q = 1) with v_min >= 2 removes the newcomers' new colours before anyone can imitate them, so creation stops; with v_min = 1 the
sanction is inert. Usage: python c18_pilot_rotation.py [M]"""
import json, sys, time
from pathlib import Path
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H.parent / 'claude_cycle17')); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D
from c17_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 128
t0 = time.time(); rows = []
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, seed=880200); col = col[dist_D(counts(col, 16), 4) == 0]
for q, v in [(0.0, 3), (1.0, 1), (1.0, 2), (1.0, 3)]:
    (b1, b2), _ = run(col, 'none', [(4, 4000), (5, 6000)], tau=20, s=0.0, cryst=0.95, q=q, v_min=v, seed=880202, entry_seed=880203)
    r = dict(q=q, v_min=v, n=int(col.shape[0]), stab_meanD=float(b1['meanD'].mean()), adapt_ever=float((b2['first'] >= 0).mean()), secs=round(time.time() - t0))
    rows.append(r); print(json.dumps(r), flush=True)
(H / 'C18_RESULTS' / 'pilot_c18_rotation.json').write_text(json.dumps(dict(status='PILOT', M=M, rows=rows), indent=1), encoding='utf-8', newline=chr(10))
