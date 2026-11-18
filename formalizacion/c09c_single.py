"""C09c (PREREGISTERED in PREREG_C09C_UN_RECIEN_LLEGADO.md; seeds 8140xx): fate of ONE newcomer who
enters a solved 4x25 community with a colour absent from it."""
import json, sys, hashlib
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D
from c09_sim import run, dispersed
M = int(sys.argv[1]) if len(sys.argv) > 1 else 1024; T = int(sys.argv[2]) if len(sys.argv) > 2 else 6400; X = 16
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, seed=814000); col = col[dist_D(counts(col, X), 4) == 0]; M = col.shape[0]
rep = dispersed(M, 1, np.random.default_rng(814001))
newc = np.array([np.setdiff1d(np.arange(X), np.unique(col[i]))[0] for i in range(M)])
c1 = col.copy(); c1[rep] = newc; rows = []
for sig in ['coll', 'D']:
    cT, _, _ = run(c1, sig, T, seed=814002)
    alive = np.array([(cT[i] == newc[i]).sum() for i in range(M)])
    cnt = counts(cT, X); ncol = (cnt > 0).sum(1)
    rows.append(dict(signal=sig, n=M, T=T, foreign_alive=float((alive > 0).mean()), solved=float((dist_D(cnt, 4) == 0).mean()),
                     mean_size_if_alive=(float(alive[alive > 0].mean()) if (alive > 0).any() else None),
                     share_unsolved_with_5plus_colours=(float((ncol[dist_D(cnt, 4) > 0] >= 5).mean()) if (dist_D(cnt, 4) > 0).any() else None)))
    print(rows[-1], flush=True)
st = 'PRIMARY' if (len(sys.argv) == 1) else 'SMOKE'
(H / 'C09_RESULTS' / f'c09c_{st}.json').write_text(json.dumps(dict(status=st, rows=rows, sha256=hashlib.sha256((H / 'c09c_single.py').read_bytes()).hexdigest()), indent=1), encoding='utf-8', newline=chr(10))
