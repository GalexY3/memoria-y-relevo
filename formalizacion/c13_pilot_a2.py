"""C13 pilot, experiment A2 (EXPLORATORY; seeds 8282xx): the wounded category. A shock replaces a fraction f of
agents with random colours (applied before the run, so the post-shock sizes are known); prediction for the
relief canon: a founding category left with s <= floor(T/2) members is dropped and not recovered.
Usage: python c13_pilot_a2.py [M] [scale]"""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c13_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 128
SC = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
X = 16; t0 = time.time()
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=int(4000 * SC), seed=828200); col = col[dist_D(counts(col, X), 4) == 0]; n = int(col.shape[0])
canon0 = counts(col, X) > 0
res = []
for f in [0.30, 0.45]:
    rng = np.random.default_rng(828201); cs = col.copy(); age0 = np.full((n, N), 10 ** 6, np.int64)
    for i in range(n):
        rr = rng.choice(N, int(round(f * N)), replace=False); cs[i, rr] = rng.integers(0, X, rr.size); age0[i, rr] = 0
    cnt = counts(cs, X); minfound = np.where(canon0, cnt, 999).min(1)
    for name, mode, kw in [('const_t8', 'constatative', dict(theta=8)), ('const_half', 'constatative', dict(theta='half')),
                           ('reflexive', 'reflexive', {}), ('comm_W50_r4', 'communicative', dict(W=50, r=4)),
                           ('comm_W200_r16', 'communicative', dict(W=200, r=16)), ('normative', 'normative', {})]:
        (a,), _ = run(cs, mode, [(4, int(4000 * SC))], canon0=canon0, age0=age0, seed=828202, entry_seed=828203, **kw)
        rec = a['first'] >= 0; wound = minfound <= 12
        row = dict(f=f, name=name, n=n, recovered=float(rec.mean()), p_wounded=float(wound.mean()),
                   rec_if_wounded=float(rec[wound].mean()) if wound.any() else None, rec_if_not=float(rec[~wound].mean()),
                   agree=float((rec == ~wound).mean()), canon=float(a['canon_size'].mean()), meanD=float(a['meanD'].mean()))
        res.append(row); print(json.dumps(row), flush=True)
(H / 'C13_RESULTS' / 'pilot_c13_A2.json').write_text(json.dumps(dict(status='PILOT', M=M, scale=SC, n=n, rows=res), indent=1), encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
