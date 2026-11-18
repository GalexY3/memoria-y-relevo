"""C13b confirmation (PREREGISTERED in PREREG_C13B_ORDEN_DESDE_EL_RUIDO.md; seeds 8490xx).
Usage: python c13b_confirm.py PART [M]      PART in {B, C, A}"""
import json, sys, time, hashlib
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c13x_sim import run
PART = sys.argv[1]; M = int(sys.argv[2]) if len(sys.argv) > 2 else 512
X = 16; t0 = time.time()
CONDS = [(f'sampled_n{n}_U1', 'sampled', dict(n_s=n, r_s=max(1, round(8 * n / N)), U=1)) for n in [12, 25, 50, 100]] + \
        [(f'sampled_n50_U{U}', 'sampled', dict(n_s=50, r_s=4, U=U)) for U in [5, 20]] + \
        [(f'const_t{th}_U1', 'constatative', dict(theta=th, U=1)) for th in [6, 7, 8, 9, 10, 13]] + \
        [('comm_W50', 'communicative', dict(W=50, r=4))]
out = dict(status='PRIMARY' if M == 512 else 'SMOKE', part=PART, M=M, rows=[])
if PART in ('B', 'C'):
    k0, k1, sd = (4, 5, 849000) if PART == 'B' else (5, 4, 849010)
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, k=k0, seed=sd); col = col[dist_D(counts(col, X), k0) == 0]
    canon0 = counts(col, X) > 0
    for name, mode, kw in CONDS:
        (b1, b2), _ = run(col, mode, [(k0, 3000), (k1, 6000)], canon0=canon0, tau=80, s=0.9, seed=sd + 2, entry_seed=sd + 3, **kw)
        out['rows'].append(dict(name=name, n=int(col.shape[0]), stab_meanD=float(b1['meanD'].mean()), stab_changes=float(b1['changes_per_1000'].mean()),
                                adapt_meanD=float(b2['meanD'].mean()), adapt_ever=float((b2['first'] >= 0).mean()), secs=round(time.time() - t0)))
        print(PART, json.dumps(out['rows'][-1]), flush=True)
elif PART == 'A':
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, seed=849020); col = col[dist_D(counts(col, X), 4) == 0]
    canon0 = counts(col, X) > 0; n = col.shape[0]; rng = np.random.default_rng(849021); cs = col.copy(); age0 = np.full((n, N), 10 ** 6, np.int64)
    for i in range(n):
        rr = rng.choice(N, 30, replace=False); cs[i, rr] = rng.integers(0, X, 30); age0[i, rr] = 0
    for name, mode, kw in CONDS:
        (a,), _ = run(cs, mode, [(4, 4000)], canon0=canon0, age0=age0, seed=849022, entry_seed=849023, **kw)
        out['rows'].append(dict(name=name, n=int(n), recovered=float((a['first'] >= 0).mean()), meanD=float(a['meanD'].mean()),
                                changes=float(a['changes_per_1000'].mean()), secs=round(time.time() - t0)))
        print('A', json.dumps(out['rows'][-1]), flush=True)
else:
    raise SystemExit('PART must be B, C or A')
out['seconds'] = round(time.time() - t0)
out['sha256'] = {f: hashlib.sha256((H / f).read_bytes()).hexdigest() for f in ['c13x_sim.py', 'c13b_confirm.py']}
(H / 'C13_RESULTS' / f"c13b_{out['status']}_{PART}.json").write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print('done', out['status'], PART, out['seconds'], 's')
