"""Blind re-implementation of the Memoria y relevo ABM (from SPEC_REPLICACION_CIEGA.md only)."""
import json, sys, time
from math import comb
import numpy as np

N = 100; X = 16; ACT = 0.05; EXPLORE = 0.10; TOL = 1e-12; ROWS = COLS = 10


def build_neighbours():
    nb = np.zeros((N, 6), dtype=np.int64)
    for r in range(ROWS):
        offs = ([(0, -1), (0, 1), (-1, -1), (-1, 0), (1, -1), (1, 0)] if r % 2 == 0
                else [(0, -1), (0, 1), (-1, 0), (-1, 1), (1, 0), (1, 1)])
        for c in range(COLS):
            for j, (dr, dc) in enumerate(offs):
                nb[r * COLS + c, j] = ((r + dr) % ROWS) * COLS + (c + dc) % COLS
    return nb


NB = build_neighbours()
AR = np.arange(N)[None, :]


def counts(col):
    M = col.shape[0]
    idx = (col + X * np.arange(M)[:, None]).ravel()
    return np.bincount(idx, minlength=M * X).reshape(M, X)


def sig_D(s, k):
    T = N / k
    ss = -np.sort(-s, axis=1)
    return np.abs(ss[:, :k] - T).sum(1) + ss[:, k:].sum(1)


def sig_C(s, k):
    T = N / k
    return np.where(s > 0, np.abs(s - T), 0).sum(1)


def sig_F(s, k, K):
    T = N / k
    return np.where(K, np.abs(s - T), s).sum(1)


def pick_present(present, rng):
    """uniform choice among True entries on last axis (rows must have >=1 True)."""
    u = rng.random(present.shape)
    u = np.where(present, u, -1.0)
    return u.argmax(-1)


def run(col, nticks, sig, k, rng, K=None, canon='none', theta=8, turnover=False,
        phases=(), win_start=0, tau=80, tc=50):
    """phases: list of (t_start, new_k). canon in none|const|relief."""
    col = col.copy(); M = col.shape[0]; am = np.arange(M)
    curk = k
    pend = False; trial = None; prev = None; sbefore = None
    reach = np.zeros(M, bool); first = np.full(M, -1)
    Dsum = np.zeros(M); nwin = 0
    ksz_first = np.full(M, -1)
    adm_min = np.full(M, 10 ** 9); adm_n = np.zeros(M, int)
    ph = dict(phases)

    def signal(s):
        if sig == 'D': return sig_D(s, curk)
        if sig == 'C': return sig_C(s, curk)
        return sig_F(s, curk, K)

    for t in range(nticks):
        # 1 revert
        if pend:
            s = counts(col); now = signal(s)
            rev = trial.any(1) & (now > sbefore + TOL)
            m = rev[:, None] & trial
            col = np.where(m, prev, col)
        # 2 events (env change, turnover, canon)
        if t in ph: curk = ph[t]
        T = N / curk
        if turnover and t % tau == 0:
            s = counts(col)
            pos = rng.integers(0, N, M)
            old = col[am, pos]
            s2 = s.copy(); s2[am, old] -= 1
            drawn = pick_present(s2 > 0, rng)
            rnd = rng.integers(0, X, M)
            new = np.where(rng.random(M) < 0.9, drawn, rnd)
            col[am, pos] = new
        if canon == 'const':
            if t % tc == 0:
                s = counts(col); K = s >= theta
        elif canon == 'relief':
            s = counts(col)
            p = rng.integers(0, N, M); c = col[am, p]
            sc = s[am, c]
            acc = (~K[am, c]) & ((np.abs(sc - T) - sc) < 0)
            if t >= win_start:
                adm_n += acc
                adm_min = np.where(acc, np.minimum(adm_min, sc), adm_min)
            K[am, c] |= acc
            nonempty = K.any(1)
            cr = pick_present(K, rng)
            scr = s[am, cr]
            rem = nonempty & ((scr - np.abs(scr - T)) < 0)
            K[am[rem], cr[rem]] = False
        # 3 signal and measures
        s = counts(col); sg = signal(s)
        D = sig_D(s, curk)
        if t >= win_start:
            z = D == 0
            first[z & ~reach] = t; reach |= z
            Dsum += D; nwin += 1
            if K is not None:
                hit = (K.sum(1) == curk) & (ksz_first < 0)
                ksz_first[hit] = t - win_start
        # 4 trial
        hungry = sg > TOL
        active = (rng.random((M, N)) < ACT) & hungry[:, None]
        expl = rng.random((M, N)) < EXPLORE
        randc = rng.integers(0, X, (M, N))
        nbi = NB[AR, rng.integers(0, 6, (M, N))]
        ncol = np.take_along_axis(col, nbi, axis=1)
        cand = np.where(expl, randc, ncol)
        trial = active & (cand != col)
        prev = col; col = np.where(trial, cand, col)
        sbefore = sg; pend = True
    # final revert
    s = counts(col); now = signal(s)
    rev = trial.any(1) & (now > sbefore + TOL)
    col = np.where(rev[:, None] & trial, prev, col)
    s = counts(col); Dend = sig_D(s, curk)
    return dict(col=col, reach=reach, first=first, Dmean=Dsum / max(nwin, 1), Dend=Dend,
                K=K, ksz_first=ksz_first, adm_min=adm_min, adm_n=adm_n)


def founding_K(col):
    return counts(col) > 0


def p_all_colours(k=4, T=25, keep=10):
    return sum((-1) ** j * comb(k, j) * comb(N - T * j, keep) for j in range(k + 1)) / comb(N, keep)


def r2(inst, rng, ticks=4000):
    M = inst.shape[0]; col = inst.copy()
    for m in range(M):
        perm = rng.permutation(N); keep = perm[:10]; rep = perm[10:]
        cols = np.unique(col[m, keep])
        col[m, rep] = rng.choice(cols, size=90)
    return run(col, ticks, 'C', 4, rng)


def canon_exp(inst, rng, k1, k2, canon, theta, p1=3000, p2=6000):
    K = founding_K(inst)
    return run(inst, p1 + p2, 'F', k1, rng, K=K.copy(), canon=canon, theta=theta, turnover=True,
               phases=[(p1, k2)], win_start=p1)


def summ(r):
    n = len(r['reach'])
    f = r['ksz_first']; ok = f >= 0
    out = dict(n=int(n), frac_D0=float(r['reach'].mean()), meanD=float(r['Dmean'].mean()),
               n_K_reaches_newk=int(ok.sum()),
               median_first_K_eq_k_among_reaching=float(np.median(f[ok])) if ok.any() else None,
               median_first_K_eq_k_censored_inf=float(np.median(np.where(ok, f, np.inf))))
    if r['adm_n'].sum() > 0:
        out['min_s_at_admission_phase2'] = int(r['adm_min'][r['adm_n'] > 0].min())
        out['n_admissions_phase2'] = int(r['adm_n'].sum())
        out['n_comm_with_admission'] = int((r['adm_n'] > 0).sum())
    return out


def main(M=256, ticks1=8000, p1=3000, p2=6000, out='RESULTS.json', seed=2024, r2t=4000):
    rng = np.random.default_rng(seed); res = {'M': M, 'seed': seed}; t0 = time.time()

    def log(m): print(f'[{time.time() - t0:7.1f}s] {m}', flush=True)

    col0 = rng.integers(0, X, (M, N))
    ra = run(col0, ticks1, 'D', 4, rng)
    ok = ra['reach'] & (ra['Dend'] == 0); inst4 = ra['col'][ok]
    rc = run(rng.integers(0, X, (M, N)), ticks1, 'C', 4, rng)
    res['R1'] = dict(n=M, ticks=ticks1, frac_D0_signal_D=float(ra['reach'].mean()),
                     frac_D0_signal_C=float(rc['reach'].mean()),
                     n_inst_k4=int(ok.sum()), frac_end_D0_signal_D=float((ra['Dend'] == 0).mean()),
                     frac_end_D0_signal_C=float((rc['Dend'] == 0).mean()))
    log(f"R1 {res['R1']}")
    r = r2(inst4, rng, r2t)
    res['R2'] = dict(n=int(len(inst4)), frac_D0_after_replacement=float(r['reach'].mean()),
                     analytic_P_all4_in_10_incumbents=p_all_colours(), ticks=r2t)
    log(f"R2 {res['R2']}")
    res['R3'] = {}
    for th in (3, 8, 15):
        r = canon_exp(inst4, rng, 4, 5, 'const', th, p1, p2)
        res['R3'][f'theta{th}'] = summ(r); log(f"R3 th{th} {res['R3'][f'theta{th}']}")
    res['R4a'] = {'constatative_theta8_same_run_as_R3': res['R3']['theta8']}
    r = canon_exp(inst4, rng, 4, 5, 'relief', 8, p1, p2)
    res['R4a']['relief'] = summ(r); log(f"R4a relief {res['R4a']['relief']}")
    r5 = run(rng.integers(0, X, (M, N)), ticks1, 'D', 5, rng)
    ok5 = r5['reach'] & (r5['Dend'] == 0); inst5 = r5['col'][ok5]
    res['R1_k5'] = dict(n=M, frac_D0=float(r5['reach'].mean()), n_inst_k5=int(ok5.sum()))
    log(f"R1k5 {res['R1_k5']}")
    res['R4b'] = {}
    for name, canon in (('relief', 'relief'), ('constatative_theta8', 'const')):
        r = canon_exp(inst5, rng, 5, 4, canon, 8, p1, p2)
        res['R4b'][name] = summ(r); log(f"R4b {name} {res['R4b'][name]}")
    json.dump(res, open(out, 'w'), indent=2)
    return res


if __name__ == '__main__':
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 256
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 2024
    ticks = int(sys.argv[3]) if len(sys.argv) > 3 else 8000
    out = sys.argv[4] if len(sys.argv) > 4 else 'RESULTS.json'
    if len(sys.argv) > 5 and sys.argv[5] == 'small':
        main(M, ticks, 300, 600, out=out, seed=seed, r2t=300)
    else:
        main(M, ticks, out=out, seed=seed)
