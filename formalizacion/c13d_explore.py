"""C13d EXPLORATORY (idea I-020; seeds 8387xx): semantic lag or lead. In B (k 4->5) with turnover, for the novel colour
that first becomes canonical in each community: lag = (tick it is admitted) - (tick it first reached 7 members, ~T/3).
Positive lag: semantics follows structure; negative: semantics anticipates it; 'no structure': admitted but never
reached 7. Usage: python c13d_explore.py [M]"""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c13d_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 256
X = 16; t0 = time.time(); rows = []
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, k=4, seed=838700); col = col[dist_D(counts(col, X), 4) == 0]; canon0 = counts(col, X) > 0
for name, mode, kw in [('relief', 'reflexive', {}), ('theta8_U1', 'constatative', dict(theta=8, U=1)), ('theta5_U1', 'constatative', dict(theta=5, U=1)),
                       ('sampled_n50', 'sampled', dict(n_s=50, r_s=4, U=1)), ('comm_W50', 'communicative', dict(W=50, r=4)), ('comm_W200', 'communicative', dict(W=200, r=16))]:
    (b1, b2), _ = run(col, mode, [(4, 3000), (5, 6000)], canon0=canon0, tau=80, s=0.9, seed=838702, entry_seed=838703, **kw)
    nt = np.where(b2['novel_t'] >= 0, b2['novel_t'], 10 ** 9); c1 = nt.argmin(1); has = (b2['novel_t'] >= 0).any(1); n = col.shape[0]
    adm = b2['novel_t'][np.arange(n), c1]; st = b2['struct_t'][np.arange(n), c1]
    lag = np.where(has & (st >= 0), adm - st, np.nan); no_struct = has & (st < 0)
    # did that first-admitted colour end up as one of the five groups? (final size >= 15)
    rows.append(dict(name=name, n=int(n), admitted=float(has.mean()), lag_median=float(np.nanmedian(lag)) if np.isfinite(lag).any() else None,
                     lag_q25=float(np.nanpercentile(lag, 25)) if np.isfinite(lag).any() else None, lag_q75=float(np.nanpercentile(lag, 75)) if np.isfinite(lag).any() else None,
                     share_semantics_first=float(((lag < 0) | no_struct)[has].mean()) if has.any() else None, share_no_structure=float(no_struct[has].mean()) if has.any() else None,
                     adapt_meanD=float(b2['meanD'].mean()), adapt_ever=float((b2['first'] >= 0).mean())))
    print(json.dumps(rows[-1]), flush=True)
(H / 'C13_RESULTS' / 'explore_c13d_semantic_lag.json').write_text(json.dumps(dict(status='EXPLORATORY', M=M, rows=rows), indent=1), encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
