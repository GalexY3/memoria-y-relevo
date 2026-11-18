"""C13 confirmation (PREREGISTERED in PREREG_C13_CANON_VIVO.md; seeds 8290xx).
Usage: python c13_confirm.py PART [M] [scale]     PART in {AC, B}  (run as two processes)"""
import json, sys, time, hashlib
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c13_sim import run
PART = sys.argv[1]
M = int(sys.argv[2]) if len(sys.argv) > 2 else 512
SC = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
X = 16; t0 = time.time()

def institutions(k, seed):
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=int(4000 * SC), k=k, seed=seed)
    return col[dist_D(counts(col, X), k) == 0]

def med(a):
    a = a[a >= 0]; return float(np.median(a)) if a.size else None

THETAS = [3, 5, 6, 8, 10, 11, 12, 13, 15]
WS = [25, 50, 100, 200, 400, 800]                       # communicative memory, r = 0.08 W (theta* = 8)
REF = [dict(name='none', mode='none'), dict(name='normative', mode='normative'),
       dict(name='const_half', mode='constatative', theta='half')]
SWEEP = [dict(name=f'const_t{th}', mode='constatative', theta=th) for th in THETAS]
REFL = [dict(name='reflexive', mode='reflexive'), dict(name='reflexive_new', mode='reflexive', voice='new'),
        dict(name='reflexive_old', mode='reflexive', voice='old')]
COMM = [dict(name=f'comm_W{w}', mode='communicative', W=w, r=int(round(0.08 * w))) for w in WS]
VOICE = [dict(name='comm_W200_new', mode='communicative', W=200, r=16, voice='new'),
         dict(name='comm_W200_old', mode='communicative', W=200, r=16, voice='old'),
         dict(name='comm_W50_new', mode='communicative', W=50, r=4, voice='new')]
kwof = lambda c: {k: v for k, v in c.items() if k not in ('name', 'mode')}
out = dict(status='PRIMARY' if (M == 512 and SC == 1.0) else 'SMOKE', part=PART, M=M, scale=SC)

def change_exp(tag, k0, k1, inst_seed, run_seed, conds):
    col = institutions(k0, inst_seed); n = int(col.shape[0]); canon0 = counts(col, X) > 0; rows = []
    for c in conds:
        (b1, b2), _ = run(col, c['mode'], [(k0, int(3000 * SC)), (k1, int(6000 * SC))], canon0=canon0, tau=80, s=0.9,
                          seed=run_seed, entry_seed=run_seed + 1, **kwof(c))
        nov2 = b2['novel_size'][b2['novel_size'] >= 0]; nov1 = b1['novel_size'][b1['novel_size'] >= 0]
        rows.append(dict(name=c['name'], n=n, stab_meanD=float(b1['meanD'].mean()), stab_changes=float(b1['changes_per_1000'].mean()),
                         stab_novel_n=int(nov1.size), stab_novel_size_med=float(np.median(nov1)) if nov1.size else None,
                         adapt_meanD=float(b2['meanD'].mean()), adapt_ever=float((b2['first'] >= 0).mean()),
                         t_D0_med=med(b2['first']), t_canon_k_med=med(b2['canon_k']), adapt_canon=float(b2['canon_size'].mean()),
                         adapt_changes=float(b2['changes_per_1000'].mean()), novel_n=int(nov2.size),
                         novel_size_min=int(nov2.min()) if nov2.size else None,
                         novel_size_med=float(np.median(nov2)) if nov2.size else None, secs=round(time.time() - t0)))
        print(tag, json.dumps(rows[-1]), flush=True)
    return rows

def shock_exp(tag, f, conds, inst_seed=829000, shock_seed=829001, run_seed=829002):
    col = institutions(4, inst_seed); n = int(col.shape[0]); canon0 = counts(col, X) > 0
    rng = np.random.default_rng(shock_seed); cs = col.copy(); age0 = np.full((n, N), 10 ** 6, np.int64)
    for i in range(n):
        rr = rng.choice(N, int(round(f * N)), replace=False); cs[i, rr] = rng.integers(0, X, rr.size); age0[i, rr] = 0
    minfound = np.where(canon0, counts(cs, X), 999).min(1); wound = minfound <= 12; rows = []
    for c in conds:
        (a,), _ = run(cs, c['mode'], [(4, int(4000 * SC))], canon0=canon0, age0=age0, seed=run_seed, entry_seed=run_seed + 1, **kwof(c))
        rec = a['first'] >= 0
        rows.append(dict(name=c['name'], f=f, n=n, recovered=float(rec.mean()), meanD=float(a['meanD'].mean()),
                         canon=float(a['canon_size'].mean()), changes=float(a['changes_per_1000'].mean()),
                         p_wounded=float(wound.mean()), rec_if_wounded=float(rec[wound].mean()) if wound.any() else None,
                         rec_if_not=float(rec[~wound].mean()), secs=round(time.time() - t0)))
        print(tag, json.dumps(rows[-1]), flush=True)
    return rows

if PART == 'AC':
    A_CONDS = REF + [dict(name='const_t8', mode='constatative', theta=8)] + REFL + \
              [c for c in COMM if c['name'] in ('comm_W50', 'comm_W100', 'comm_W200')] + VOICE
    out['A'] = shock_exp('A', 0.30, A_CONDS)
    A2_CONDS = [c for c in A_CONDS if c['name'] in ('normative', 'const_t8', 'const_half', 'reflexive', 'comm_W50', 'comm_W200')]
    out['A2'] = shock_exp('A2', 0.45, A2_CONDS)
    out['C'] = change_exp('C', 5, 4, 829010, 829012, REF + SWEEP + REFL + COMM + VOICE)
elif PART == 'B':
    out['B'] = change_exp('B', 4, 5, 829020, 829022, REF + SWEEP + REFL + COMM + VOICE)
    # descriptive: dose of newcomer voice during the stable phase only (k = 4, turnover)
    col = institutions(4, 829020); canon0 = counts(col, X) > 0; dose = []
    for (W, r) in [(200, 16), (50, 4)]:
        for v in [0.0, 0.05, 0.1, 0.2, 0.3, 0.5]:
            (b,), _ = run(col, 'communicative', [(4, int(3000 * SC))], canon0=canon0, W=W, r=r, voice='new', v=v, tau=80, s=0.9,
                          seed=829030, entry_seed=829031)
            nv = b['novel_size'][b['novel_size'] >= 0]
            dose.append(dict(W=W, r=r, v=v, stab_meanD=float(b['meanD'].mean()), changes=float(b['changes_per_1000'].mean()),
                             novel_n=int(nv.size), novel_le2=int((nv <= 2).sum())))
            print('dose', json.dumps(dose[-1]), flush=True)
    out['dose'] = dose
else:
    raise SystemExit('PART must be AC or B')
out['seconds'] = round(time.time() - t0)
out['sha256'] = {f: hashlib.sha256((H / f).read_bytes()).hexdigest() for f in ['c13_sim.py', 'c13_confirm.py']}
(H / 'C13_RESULTS' / f"c13_{out['status']}_{PART}.json").write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print('done', out['status'], PART, out['seconds'], 's')
