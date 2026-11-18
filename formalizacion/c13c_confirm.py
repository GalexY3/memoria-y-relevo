"""C13c confirmation (PREREGISTERED in PREREG_C13C_FILO_DE_LA_DIVISORIA.md; seeds 8396xx). Dissolution with
different ratios T_old/T_new: 5->4 (0.8), 4->2 and 10->5 (0.5), 5->2 and 10->4 (0.4). Relief against fixed thresholds
(absolute 8; relative to the new target T/4, T/3, T/2+1), turnover tau = 80, s = 0.9. Usage: python c13c_confirm.py [M]"""
import json, sys, time, hashlib
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c13x_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 512
X = 16; t0 = time.time(); out = dict(status='PRIMARY' if M == 512 else 'SMOKE', M=M, rows=[])
for (k0, k1, sd) in [(5, 4, 839600), (4, 2, 839610), (10, 5, 839620), (5, 2, 839630), (10, 4, 839640)]:
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=6000, k=k0, seed=sd); col = col[dist_D(counts(col, X), k0) == 0]
    canon0 = counts(col, X) > 0; T1 = N / k1
    conds = [('relief', 'reflexive', {}), ('theta8_abs', 'constatative', dict(theta=8, U=1)),
             ('theta_T/4', 'constatative', dict(theta=max(2, round(T1 / 4)), U=1)),
             ('theta_T/3', 'constatative', dict(theta=max(2, round(T1 / 3)), U=1)),
             ('theta_T/2+1', 'constatative', dict(theta=int(T1 // 2) + 1, U=1))]
    for name, mode, kw in conds:
        (b1, b2), _ = run(col, mode, [(k0, 3000), (k1, 6000)], canon0=canon0, tau=80, s=0.9, seed=sd + 2, entry_seed=sd + 3, **kw)
        r = dict(change=f'{k0}->{k1}', ratio=(N / k0) / T1, k_new=k1, name=name, theta=kw.get('theta'), n=int(col.shape[0]),
                 stab_meanD=float(b1['meanD'].mean()), adapt_meanD=float(b2['meanD'].mean()), adapt_ever=float((b2['first'] >= 0).mean()),
                 adapt_canon_size=float(b2['canon_size'].mean()), share_canon_below_k=float((b2['canon_size'] < k1 - 0.5).mean()),
                 t_canon_k=float(np.median(b2['canon_k'][b2['canon_k'] >= 0])) if (b2['canon_k'] >= 0).any() else None, secs=round(time.time() - t0))
        out['rows'].append(r); print(json.dumps(r), flush=True)
out['seconds'] = round(time.time() - t0)
out['sha256'] = {f: hashlib.sha256((H / f).read_bytes()).hexdigest() for f in ['c13x_sim.py', 'c13c_confirm.py']}
(H / 'C13_RESULTS' / f"c13c_{out['status']}.json").write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print('done', out['status'], out['seconds'], 's')
