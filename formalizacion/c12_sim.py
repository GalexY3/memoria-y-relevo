"""C12 simulator: self-description (canon of categories) as the regulator's model (idea I-005).
Signal 'canon': cost = sum over canonical colours |s - T| + sum over non-canonical colours s, divided by 2N.
Canon modes:
  'normative'      fixed list (the institution's founding colours), never updated
  'constatative'   every U ticks the canon is rewritten as the colours with count >= theta
  'none'           plain collective signal C (sizes of present colours only), for comparison
Trial-and-revert dynamics as in C08-C10; optional continuous turnover (tau, s) and environment k."""
import numpy as np
from c08_sim import counts, dist_D, NB, N

EPS = 1e-12

def cost_canon(cnt, canon, T):
    """cnt: (M,X) counts; canon: (M,X) bool."""
    return (np.where(canon, np.abs(cnt - T), cnt).sum(1)) / (2 * N)

def cost_C(cnt, T):
    return ((np.abs(cnt - T) * (cnt > 0)).sum(1)) / (2 * N)

def run(col0, mode, k_env, T_ticks, canon0=None, theta=5, U=50, tau=0, s=1.0, X=16, act=0.05, explore=0.1,
        seed=0, entry_seed=1, events=None):
    rng = np.random.default_rng(seed); er = np.random.default_rng(entry_seed)
    col = col0.copy(); M = col.shape[0]; ar = np.arange(M)[:, None]; an = np.arange(N)[None, :]
    T = N / k_env
    canon = canon0.copy() if canon0 is not None else (counts(col, X) > 0)
    def sig_of(c):
        cnt = counts(c, X)
        g = cost_C(cnt, T) if mode == 'none' else cost_canon(cnt, canon, T)
        return np.repeat(g[:, None], N, 1)
    pending = np.zeros((M, N), bool); oldc = col.copy(); olds = np.zeros((M, N)); sig = sig_of(col)
    first = np.full(M, -1); Dsum = np.zeros(M); canon_size_sum = np.zeros(M)
    for t in range(T_ticks):
        col = np.where(pending & (sig > olds + EPS), oldc, col); pending[:] = False
        if events and t in events:
            rep = events[t]
            for i in np.nonzero(rep.any(1))[0]:
                r = np.nonzero(rep[i])[0]; col[i, r] = er.integers(0, X, len(r))
        if tau and t % tau == 0:
            who = er.integers(0, N, M)
            for i in range(M):
                if er.random() < s:
                    inc = np.delete(col[i], who[i]); col[i, who[i]] = er.choice(np.unique(inc))
                else:
                    col[i, who[i]] = er.integers(0, X)
        cnt = counts(col, X)
        if mode == 'constatative' and t % U == 0:
            canon = cnt >= theta
        sig = sig_of(col); D = dist_D(cnt, k_env)
        Dsum += D; canon_size_sum += canon.sum(1); first = np.where((first < 0) & (D == 0), t, first)
        tr = (rng.random((M, N)) < act) & (sig > EPS)
        nbcol = col[ar, NB[an, rng.integers(0, 6, (M, N))]]
        cand = np.where(rng.random((M, N)) < explore, rng.integers(0, X, (M, N)), nbcol)
        oldc = col.copy(); olds = sig.copy(); pending = tr & (cand != col); col = np.where(pending, cand, col)
        sig = sig_of(col)
    col = np.where(pending & (sig > olds + EPS), oldc, col)
    return dict(first=first, meanD=Dsum / T_ticks, canon_size=canon_size_sum / T_ticks, final_D=dist_D(counts(col, X), k_env), col=col, canon=canon)
