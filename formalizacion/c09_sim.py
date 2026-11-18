"""C09 simulator: trial-and-revert dynamics with scheduled replacement events and two acceptance rules.
Reuses the frozen C08 primitives (grid, counts, D, signals) without modifying them.
rule 'tr'     : keep a trial unless the own signal got WORSE (neutral moves accepted)  [= C08]
rule 'strict' : keep a trial only if the own signal got strictly BETTER (no neutral drift)"""
import numpy as np
from c08_sim import counts, dist_D, signal, NB, N

EPS = 1e-12

def enter(col, rep, entry, rng, X=16):
    """Newcomers at positions rep[i] take a colour; incumbents are the non-replaced agents."""
    col = col.copy()
    for i in np.nonzero(rep.any(1))[0]:
        r = np.nonzero(rep[i])[0]; inc = np.nonzero(~rep[i])[0]
        if entry == 'random': col[i, r] = rng.integers(0, X, len(r))
        elif entry == 'vocab': col[i, r] = rng.choice(np.unique(col[i, inc]), len(r))
        elif entry == 'new': col[i, r] = np.setdiff1d(np.arange(X), np.unique(col[i, inc]))[0]
        else: raise ValueError(entry)
    return col

def run(col0, mode, T, k=4, X=16, act=0.05, explore=0.1, seed=0, rule='tr', events=None, entry='random', entry_seed=0):
    """events: dict tick -> (M,N) bool mask of agents replaced at the start of that tick.
    Returns settled final colours, first tick (counted from the last event) with D=0 (-1 if never),
    and occupancy of D=0 over the last 25% of ticks."""
    rng = np.random.default_rng(seed); erng = np.random.default_rng(entry_seed)
    events = events or {}; last = max(events) if events else 0
    col = col0.copy(); M = col.shape[0]
    pending = np.zeros((M, N), bool); oldc = col.copy(); olds = np.zeros((M, N))
    sig = signal(col, counts(col, X), mode, k); first = np.full(M, -1); occ = np.zeros(M); t_occ = int(0.75 * T)
    ar = np.arange(M)[:, None]; an = np.arange(N)[None, :]
    for t in range(T):
        bad = (sig > olds + EPS) if rule == 'tr' else ~(sig < olds - EPS)
        col = np.where(pending & bad, oldc, col); pending[:] = False
        if t in events:
            col = enter(col, events[t], entry, erng, X)
        cnt = counts(col, X); sig = signal(col, cnt, mode, k); D = dist_D(cnt, k)
        if t >= last: first = np.where((first < 0) & (D == 0), t - last, first)
        if t >= t_occ: occ += (D == 0)
        tr = (rng.random((M, N)) < act) & (sig > EPS)
        nbcol = col[ar, NB[an, rng.integers(0, 6, (M, N))]]
        cand = np.where(rng.random((M, N)) < explore, rng.integers(0, X, (M, N)), nbcol)
        oldc = col.copy(); olds = sig.copy(); pending = tr & (cand != col); col = np.where(pending, cand, col)
        sig = signal(col, counts(col, X), mode, k)
    bad = (sig > olds + EPS) if rule == 'tr' else ~(sig < olds - EPS)
    col = np.where(pending & bad, oldc, col)
    return col, first, occ / max(1, T - t_occ)

def dispersed(M, m, rng):
    out = np.zeros((M, N), bool)
    for i in range(M): out[i, rng.choice(N, m, replace=False)] = True
    return out
