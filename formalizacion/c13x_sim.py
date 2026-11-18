"""C13x EXPLORATORY variant (idea I-021: noise or memory?). Copy of c13_sim.py plus mode 'sampled':
every U ticks the canon is rewritten from a fresh random sample of n_s agents: colours with >= r_s members in the sample.

Original docstring: C13 simulator: the canon (self-description) written by the agents themselves (idea I-017).

Builds on C12 (canon cost = sum over canonical colours |s - T| + sum over non-canonical colours s, / 2N)
and reuses the frozen C08 primitives unchanged. Canon regimes:
  'none'          plain collective signal C (no canon), reference
  'normative'     fixed founding canon, reference
  'constatative'  external observer: every U ticks canon = colours with count >= theta (C12), reference;
                  theta='half' means theta = floor(T/2) + 1 recomputed with the current T
  'reflexive'     uptake by relief: each tick one speaker proposes its own colour if it is not canonical,
                  and one random canonical colour is put under review; a change is accepted iff it
                  strictly lowers the shared canon cost (=> admit iff s > T/2, drop iff s < T/2)
  'communicative' uptake by repetition: each tick one speaker cites its own colour; the canon is the set
                  of colours cited at least r times in the last W citations (social memory, forgetting)
Voice (who speaks / proposes): 'uniform' | 'new' (with prob v the speaker is drawn among agents that
entered less than A_new ticks ago) | 'old' (with prob v among agents at least as old as the median).
Dynamics: trial-and-revert as in C08-C12; environment k may change by phase; optional continuous
turnover (tau, s) and replacement events."""
import numpy as np
from c08_sim import counts, dist_D, NB, N

EPS = 1e-12
BIG_AGE = 10 ** 6

def cost_canon(cnt, canon, T):
    return (np.where(canon, np.abs(cnt - T), cnt).sum(1)) / (2 * N)

def cost_C(cnt, T):
    return ((np.abs(cnt - T) * (cnt > 0)).sum(1)) / (2 * N)

def pick_speaker(rng, age, voice, v, A_new):
    M = age.shape[0]
    u = rng.random((M, N)); who = u.argmin(1)                    # uniform speaker
    if voice == 'uniform' or v <= 0:
        return who
    if voice == 'new':
        mask = age < A_new
    elif voice == 'old':
        mask = age >= np.median(age, 1, keepdims=True)
    else:
        raise ValueError(voice)
    key = u + 2.0 * (~mask); sel = key.argmin(1)                  # random member of the masked group
    use = (rng.random(M) < v) & mask.any(1)
    return np.where(use, sel, who)

def run(col0, mode, phases, canon0=None, theta=8, U=50, W=200, r=16, voice='uniform', v=0.5, A_new=160,
        tau=0, s=1.0, X=16, act=0.05, explore=0.1, seed=0, entry_seed=1, events=None, age0=None,
        state=None, n_s=50, r_s=4):
    """phases: list of (k_env, ticks). Returns dict with per-phase stats and the final state
    (col, canon, age, cite buffer) so that runs can be chained."""
    rng = np.random.default_rng(seed); er = np.random.default_rng(entry_seed)
    col = col0.copy(); M = col.shape[0]; ar = np.arange(M)[:, None]; an = np.arange(N)[None, :]
    canon = canon0.copy() if canon0 is not None else (counts(col, X) > 0)
    age = (age0.copy() if age0 is not None else np.full((M, N), BIG_AGE, np.int64))
    # communicative memory: ring buffer of the last W cited colours, prefilled from the current composition
    if mode == 'communicative':
        if state is not None and 'buf' in state:
            buf = state['buf'].copy(); bpos = state['bpos']
        else:
            buf = col[ar, rng.integers(0, N, (M, W))]; bpos = 0
        cites = np.zeros((M, X), np.int64); np.add.at(cites, (np.repeat(np.arange(M), W), buf.ravel()), 1)
        canon = cites >= r
    out = []
    for (k_env, ticks) in phases:
        T = N / k_env
        th = (int(np.floor(T / 2)) + 1) if theta == 'half' else theta
        def sig_of(c):
            cnt = counts(c, X)
            g = cost_C(cnt, T) if mode == 'none' else cost_canon(cnt, canon, T)
            return np.repeat(g[:, None], N, 1)
        pending = np.zeros((M, N), bool); oldc = col.copy(); olds = np.zeros((M, N)); sig = sig_of(col)
        first = np.full(M, -1); Dsum = np.zeros(M); csz = np.zeros(M); changes = np.zeros(M)
        canon_k = np.full(M, -1); canon_start = canon.copy()
        novel_size = np.full((M, X), -1); novel_t = np.full((M, X), -1)   # first admission of colours not canonical at phase start
        for t in range(ticks):
            col = np.where(pending & (sig > olds + EPS), oldc, col); pending[:] = False
            age += 1
            if events and t in events:
                rep = events[t]
                for i in np.nonzero(rep.any(1))[0]:
                    rr = np.nonzero(rep[i])[0]; col[i, rr] = er.integers(0, X, len(rr)); age[i, rr] = 0
            if tau and t % tau == 0:
                who = er.integers(0, N, M)
                for i in range(M):
                    if er.random() < s:
                        inc = np.delete(col[i], who[i]); col[i, who[i]] = er.choice(np.unique(inc))
                    else:
                        col[i, who[i]] = er.integers(0, X)
                    age[i, who[i]] = 0
            cnt = counts(col, X); old_canon = canon.copy()
            if mode == 'constatative' and t % U == 0:
                canon = cnt >= th
            elif mode == 'reflexive':
                spk = pick_speaker(rng, age, voice, v, A_new); c = col[np.arange(M), spk]
                sc = cnt[np.arange(M), c]
                add = (~canon[np.arange(M), c]) & (np.abs(sc - T) - sc < -EPS)
                canon[np.arange(M)[add], c[add]] = True
                # review one random canonical colour (uniform among canonical)
                key = rng.random((M, X)) + 2.0 * (~canon); rc = key.argmin(1); has = canon.any(1)
                src = cnt[np.arange(M), rc]
                drop = has & (src - np.abs(src - T) < -EPS)
                canon[np.arange(M)[drop], rc[drop]] = False
            elif mode == 'sampled' and t % U == 0:
                samp = np.argsort(rng.random((M, N)), 1)[:, :n_s]; sc = col[np.arange(M)[:, None], samp]
                cs = np.zeros((M, X), np.int64); np.add.at(cs, (np.repeat(np.arange(M), n_s), sc.ravel()), 1)
                canon = cs >= r_s
            elif mode == 'communicative':
                spk = pick_speaker(rng, age, voice, v, A_new); c = col[np.arange(M), spk]
                gone = buf[:, bpos]
                np.subtract.at(cites, (np.arange(M), gone), 1); np.add.at(cites, (np.arange(M), c), 1)
                buf[:, bpos] = c; bpos = (bpos + 1) % W
                canon = cites >= r
            ch = (canon != old_canon)
            changes += ch.sum(1)
            nov = canon & ~old_canon & ~canon_start & (novel_size < 0)
            novel_size = np.where(nov, cnt, novel_size); novel_t = np.where(nov, t, novel_t)
            sig = sig_of(col); D = dist_D(cnt, k_env)
            Dsum += D; csz += canon.sum(1); first = np.where((first < 0) & (D == 0), t, first)
            canon_k = np.where((canon_k < 0) & (canon.sum(1) == k_env), t, canon_k)   # first tick the canon names k_env categories
            tr = (rng.random((M, N)) < act) & (sig > EPS)
            nbcol = col[ar, NB[an, rng.integers(0, 6, (M, N))]]
            cand = np.where(rng.random((M, N)) < explore, rng.integers(0, X, (M, N)), nbcol)
            oldc = col.copy(); olds = sig.copy(); pending = tr & (cand != col); col = np.where(pending, cand, col)
            sig = sig_of(col)
        col = np.where(pending & (sig > olds + EPS), oldc, col)
        out.append(dict(k=k_env, ticks=ticks, first=first, meanD=Dsum / ticks, canon_size=csz / ticks,
                        changes_per_1000=changes * 1000.0 / ticks, final_D=dist_D(counts(col, X), k_env),
                        canon_k=canon_k, novel_size=novel_size, novel_t=novel_t))
    st = dict(col=col, canon=canon, age=age)
    if mode == 'communicative':
        st.update(buf=buf, bpos=bpos)
    return out, st
