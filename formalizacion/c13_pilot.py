"""C13 pilot (EXPLORATORY; seeds 8280xx; not reused in the confirmation).
Usage: python c13_pilot.py [M] [scale]"""
import json, sys, time
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c13_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 128
SC = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
X = 16; t0 = time.time()
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=int(4000 * SC), seed=828000); col = col[dist_D(counts(col, X), 4) == 0]; n = int(col.shape[0])
canon0 = counts(col, X) > 0
rng = np.random.default_rng(828001); rep = np.zeros((n, N), bool)
for i in range(n): rep[i, rng.choice(N, 30, replace=False)] = True
CONDS = [dict(name='none', mode='none'), dict(name='normative', mode='normative'),
         dict(name='const_t8', mode='constatative', theta=8), dict(name='const_half', mode='constatative', theta='half'),
         dict(name='reflexive', mode='reflexive'), dict(name='reflexive_new', mode='reflexive', voice='new'),
         dict(name='comm_W200_r16', mode='communicative', W=200, r=16),
         dict(name='comm_W50_r4', mode='communicative', W=50, r=4),
         dict(name='comm_W800_r64', mode='communicative', W=800, r=64),
         dict(name='comm_W200_r10', mode='communicative', W=200, r=10),
         dict(name='comm_W200_r24', mode='communicative', W=200, r=24),
         dict(name='comm_W200_r16_new', mode='communicative', W=200, r=16, voice='new'),
         dict(name='comm_W200_r16_old', mode='communicative', W=200, r=16, voice='old'),
         dict(name='comm_W25_r2', mode='communicative', W=25, r=2), dict(name='comm_W100_r8', mode='communicative', W=100, r=8),
         dict(name='comm_W400_r32', mode='communicative', W=400, r=32),
         dict(name='comm_W50_r4_new', mode='communicative', W=50, r=4, voice='new'),
         dict(name='reflexive_old', mode='reflexive', voice='old'),
         dict(name='comm_W50_r6', mode='communicative', W=50, r=6), dict(name='comm_W50_r2', mode='communicative', W=50, r=2)]
only = sys.argv[3].split(',') if len(sys.argv) > 3 else None
res = []
def med(a):
    a = a[a >= 0]; return float(np.median(a)) if a.size else None
for c in CONDS:
    if only and c['name'] not in only:
        continue
    kw = {k: v for k, v in c.items() if k not in ('name', 'mode')}
    oa, _ = run(col, c['mode'], [(4, int(4000 * SC))], canon0=canon0, seed=828002, entry_seed=828003, events={0: rep}, **kw)
    a = oa[0]
    ob, _ = run(col, c['mode'], [(4, int(3000 * SC)), (5, int(6000 * SC))], canon0=canon0, tau=80, s=0.9,
                seed=828004, entry_seed=828005, **kw)
    b1, b2 = ob
    adm = b2['novel_size'][b2['novel_size'] >= 0]
    # size of the eventual 5th category at its first admission: novel colour admitted first in each community
    nt = np.where(b2['novel_t'] >= 0, b2['novel_t'], 10 ** 9); f1 = nt.argmin(1); has = (b2['novel_t'] >= 0).any(1)
    first_sz = b2['novel_size'][np.arange(n), f1][has]
    row = dict(name=c['name'], n=n, A_recovered=float((a['first'] >= 0).mean()), A_meanD=float(a['meanD'].mean()),
               A_canon=float(a['canon_size'].mean()), A_changes=float(a['changes_per_1000'].mean()),
               B_stab_meanD=float(b1['meanD'].mean()), B_stab_canon=float(b1['canon_size'].mean()),
               B_stab_changes=float(b1['changes_per_1000'].mean()),
               B_adapt_meanD=float(b2['meanD'].mean()), B_adapt_ever=float((b2['first'] >= 0).mean()),
               B_t_D0_med=med(b2['first']), B_t_canon5_med=med(b2['canon_k']), B_adapt_canon=float(b2['canon_size'].mean()),
               B_adapt_changes=float(b2['changes_per_1000'].mean()),
               B_novel_size_med=float(np.median(adm)) if adm.size else None, B_novel_n=int(adm.size),
               B_first_novel_size_med=float(np.median(first_sz)) if first_sz.size else None,
               B_novel_lt_half=float((adm < 11).mean()) if adm.size else None,
               secs=round(time.time() - t0))
    res.append(row); print(json.dumps(row), flush=True)
tag = '' if not only else '_' + '_'.join(only)
(H / 'C13_RESULTS' / f'pilot_c13{tag}.json').write_text(json.dumps(dict(status='PILOT', M=M, scale=SC, n=n, rows=res), indent=1), encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
