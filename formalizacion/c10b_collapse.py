"""C10b (PREREGISTERED in PREREG_C10B_TASA_DE_DESVIACION.md; seeds 8170xx). Same design as C10,
but tau and s chosen so that the inflow rate of unsocialized newcomers r = (1-s)/tau takes the same
values at three different turnover rates. Usage: python c10b_collapse.py [M] [scale]"""
import json, sys, time, hashlib
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D
from c10_sim import run_phases
M = int(sys.argv[1]) if len(sys.argv) > 1 else 512
SC = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
X = 16; t0 = time.time(); R_GRID = [0.0005, 0.001, 0.002, 0.004]; TAUS = [10, 40, 160]
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=int(4000 * SC), seed=817000)
col = col[dist_D(counts(col, X), 4) == 0]; n = int(col.shape[0]); rows = []
for ti, tau in enumerate(TAUS):
    for gi, sig in enumerate(['coll', 'D']):
        for ri, r in enumerate(R_GRID):
            s = 1 - r * tau
            (a, b), _ = run_phases(col, [(sig, 4, int(4000 * SC)), (sig, 5, int(6000 * SC))], s, tau,
                                   seed=817100 + 10 * ti + gi, entry_seed=817200 + 10 * ti + gi)
            rows.append(dict(tau=tau, signal=sig, r=r, s=s, n=n, stab_meanD=float(a['meanD'].mean()),
                             adapt_meanD=float(b['meanD'].mean()), adapt_ever=float((b['first'] >= 0).mean())))
            print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in rows[-1].items()}, flush=True)
status = 'PRIMARY' if (M == 512 and SC == 1.0) else 'SMOKE'
(H / 'C10_RESULTS' / f'c10b_{status}.json').write_text(json.dumps(dict(status=status, M=M, n_established=n, scale=SC, rows=rows,
    sha256={f: hashlib.sha256((H / f).read_bytes()).hexdigest() for f in ['c10_sim.py', 'c10b_collapse.py']}, seconds=time.time() - t0), indent=1),
    encoding='utf-8', newline=chr(10))
print('done', status, round(time.time() - t0), 's')
