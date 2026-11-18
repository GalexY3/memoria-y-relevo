"""C10 simulator: continuous turnover with partial socialization and an environmental shift of the
required structure (k=4 -> k=5). Reuses the frozen C08 primitives (grid, counts, D, signals).
Each tau ticks one random agent is replaced; the newcomer is socialized with probability s (takes a
colour used by incumbents, uniformly over those colours) or else brings any of the X colours.
Dynamics: trial-and-revert (neutral moves accepted), as in C08-C09."""
import numpy as np
from c08_sim import counts, dist_D, signal, NB, N

EPS = 1e-12

def run_phases(col0, phases, s, tau, X=16, act=0.05, explore=0.1, seed=0, entry_seed=1):
    """phases: list of (mode, k, T). Returns dict with per-phase mean structural error D_k (k of that
    phase), occupancy of D_k = 0, first tick with D_k = 0 (-1 if never), and final colours."""
    rng = np.random.default_rng(seed); er = np.random.default_rng(entry_seed)
    col = col0.copy(); M = col.shape[0]; ar = np.arange(M)[:, None]; an = np.arange(N)[None, :]
    out = []; t_global = 0
    for (mode, k, T) in phases:
        pending = np.zeros((M, N), bool); oldc = col.copy(); olds = np.zeros((M, N))
        sig = signal(col, counts(col, X), mode, k)
        Dsum = np.zeros(M); occ = np.zeros(M); first = np.full(M, -1); ncol_sum = np.zeros(M)
        for t in range(T):
            col = np.where(pending & (sig > olds + EPS), oldc, col); pending[:] = False
            if t_global % tau == 0:
                who = er.integers(0, N, M)
                for i in range(M):
                    if er.random() < s:
                        inc = np.delete(col[i], who[i]); col[i, who[i]] = er.choice(np.unique(inc))
                    else:
                        col[i, who[i]] = er.integers(0, X)
            cnt = counts(col, X); sig = signal(col, cnt, mode, k); D = dist_D(cnt, k)
            Dsum += D; occ += (D == 0); ncol_sum += (cnt > 0).sum(1)
            first = np.where((first < 0) & (D == 0), t, first)
            tr = (rng.random((M, N)) < act) & (sig > EPS)
            nbcol = col[ar, NB[an, rng.integers(0, 6, (M, N))]]
            cand = np.where(rng.random((M, N)) < explore, rng.integers(0, X, (M, N)), nbcol)
            oldc = col.copy(); olds = sig.copy(); pending = tr & (cand != col); col = np.where(pending, cand, col)
            sig = signal(col, counts(col, X), mode, k); t_global += 1
        col = np.where(pending & (sig > olds + EPS), oldc, col)
        out.append(dict(mode=mode, k=k, T=T, meanD=Dsum / T, occupancy=occ / T, first=first, mean_colours=ncol_sum / T))
    return out, col
