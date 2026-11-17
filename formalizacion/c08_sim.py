"""C08: «Memoria y relevo» simulator (vectorised over M independent communities).

10x10 hexagonal toroidal grid (6 neighbours), X colours, target k groups of N/k.
Each tick: observe (own colour, 6 neighbour colours, last signal) -> optionally propose own colour
to a random neighbour -> decide. Independent tabular Q-learners (contextual bandit) per agent;
memory is per agent, so replacement wipes it.

Signals (cost, normalised to [0,1]):
  'ind'   individual hunger |n_own - T| / (N - T)
  'coll'  collective hunger of the original design: sum over PRESENT colours |n_c - T| / (2N)
  'D'     corrected collective: L1 distance to the nearest balanced k-partition / (2N)
Dilemma variant: reward = -D + bonus * [colour == preferred colour], with unbalanced preferences.

State (96): own-signal bin (4) x signal change (3) x same-colour neighbours bin (4) x proposal received (2)
Actions (5): stay | adopt most common neighbour colour | adopt least common neighbour colour |
             accept a received proposal | random colour
"""
import numpy as np

def hex_neighbours(R=10, C=10):
    nb = np.zeros((R * C, 6), int)
    for r in range(R):
        for c in range(C):
            if r % 2 == 0: d = [(0, -1), (0, 1), (-1, -1), (-1, 0), (1, -1), (1, 0)]
            else:          d = [(0, -1), (0, 1), (-1, 0), (-1, 1), (1, 0), (1, 1)]
            nb[r * C + c] = [((r + dr) % R) * C + (c + dc) % C for dr, dc in d]
    return nb

NB = hex_neighbours()
N = 100

def counts(col, X):
    M = col.shape[0]; cnt = np.zeros((M, X), int)
    np.add.at(cnt, (np.repeat(np.arange(M), col.shape[1]), col.ravel()), 1)
    return cnt

def dist_D(cnt, k):
    T = N / k; s = -np.sort(-cnt, 1)
    return np.abs(s[:, :k] - T).sum(1) + s[:, k:].sum(1)

def signal(col, cnt, mode, k, pref=None, bonus=0.0):
    M = col.shape[0]; T = N / k
    if mode == 'ind':
        own = np.take_along_axis(cnt, col, 1)
        return np.abs(own - T) / (N - T)
    if mode == 'coll':
        v = (np.abs(cnt - T) * (cnt > 0)).sum(1) / (2 * N)
        return np.repeat(v[:, None], N, 1)
    D = dist_D(cnt, k) / (2 * N)
    c = np.repeat(D[:, None], N, 1)
    if mode == 'dilemma':
        c = c - bonus * (col == pref)
    return c

class Sim:
    def __init__(self, M, mode, k=4, X=16, messages=True, seed=0, alpha=0.1, bonus=0.0, pref_skew=0.0):
        self.rng = np.random.default_rng(seed); self.M, self.mode, self.k, self.X = M, mode, k, X
        self.messages, self.alpha, self.bonus = messages, alpha, bonus
        self.col = self.rng.integers(0, X, (M, N))
        self.Q = np.zeros((M, N, 96, 5))
        # preferences (dilemma): colours 0..k-1, skewed so balance requires sacrifice
        p = np.full(k, 1 / k); p[0] += pref_skew; p[1:] -= pref_skew / (k - 1)
        self.pref = self.rng.choice(k, (M, N), p=p)
        self.prev_sig = self.cost(); self.prev_bin = self.bin(self.prev_sig); self.dsig = np.ones((M, N), int)

    def cost(self):
        return signal(self.col, counts(self.col, self.X), self.mode, self.k, self.pref, self.bonus)

    def bin(self, s):
        return np.digitize(s, [0.02, 0.1, 0.3])

    def state(self, got):
        nbc = self.col[:, NB]                                   # M,N,6
        same = (nbc == self.col[:, :, None]).sum(2)
        sb = np.digitize(same, [1, 3, 5])
        return ((self.prev_bin * 3 + self.dsig) * 4 + sb) * 2 + got

    def step(self, eps, learn=True):
        M, rng = self.M, self.rng
        # proposals: each agent proposes its colour to one random neighbour with prob .5
        got = np.zeros((M, N), int); prop_col = np.full((M, N), -1)
        if self.messages:
            who = rng.random((M, N)) < 0.5
            tgt = NB[np.arange(N)[None, :], rng.integers(0, 6, (M, N))]
            mi, ai = np.nonzero(who)
            prop_col[mi, tgt[mi, ai]] = self.col[mi, ai]            # last writer wins: one received proposal kept
            got = (prop_col >= 0).astype(int)
        s = self.state(got)
        q = np.take_along_axis(self.Q, s[:, :, None, None].repeat(5, 3), 2)[:, :, 0, :]
        greedy = q.argmax(2)
        a = np.where(rng.random((M, N)) < eps, rng.integers(0, 5, (M, N)), greedy)
        nbc = self.col[:, NB]
        # most / least common neighbour colour
        onehot = (nbc[..., None] == np.arange(self.X)).sum(2)            # M,N,X
        most = np.where(onehot.max(2) > 0, onehot.argmax(2), self.col)
        oh2 = np.where(onehot > 0, onehot, 99); least = oh2.argmin(2)
        new = self.col.copy()
        new = np.where(a == 1, most, new); new = np.where(a == 2, least, new)
        new = np.where((a == 3) & (prop_col >= 0), prop_col, new)
        new = np.where(a == 4, rng.integers(0, self.X, (M, N)), new)
        self.col = new
        sig = self.cost()
        if learn:
            r = -sig
            idx = (np.arange(M)[:, None], np.arange(N)[None, :], s, a)
            self.Q[idx] += self.alpha * (r - self.Q[idx])
        self.dsig = np.where(sig < self.prev_sig - 1e-9, 0, np.where(sig > self.prev_sig + 1e-9, 2, 1))
        self.prev_sig = sig; self.prev_bin = self.bin(sig)

    def metrics(self):
        cnt = counts(self.col, self.X); D = dist_D(cnt, self.k)
        return dict(D=D, solved=(D == 0), ncol=(cnt > 0).sum(1))

    def replace(self, frac=0.3, contiguous=False, entry='random'):
        """Replace a fraction of agents: wipe their Q (memory); entry colour fixed in advance."""
        M, rng = self.M, self.rng; m = int(frac * N)
        for i in range(M):
            if contiguous:
                start = rng.integers(0, N); order = [start]; seen = {start}; j = 0
                while len(order) < m:
                    for v in NB[order[j]]:
                        if v not in seen and len(order) < m: seen.add(v); order.append(v)
                    j += 1
                idx = np.array(order)
            else:
                idx = rng.choice(N, m, replace=False)
            self.Q[i, idx] = 0
            if entry == 'random': self.col[i, idx] = rng.integers(0, self.X, m)
            elif entry == 'new':  self.col[i, idx] = self.X - 1   # all newcomers enter on one (possibly new) colour
        self.prev_sig = self.cost(); self.prev_bin = self.bin(self.prev_sig)


def trial_and_revert(M, mode, act=0.05, explore=0.1, T=8000, k=4, X=16, seed=0, col0=None,
                     pref=None, bonus=0.0, record_every=0):
    """Competent local rule with ONE-STEP memory (Young-style trial and error): a hungry agent, when
    active, tries a neighbour's colour (or a random one with prob `explore`); next tick it reverts if
    its own signal got worse. Memory = (previous colour, previous signal). Returns settled final colours,
    the first tick each community reached D = 0, the optional D trace, and the share of the last 25%
    of ticks with settled D = 0 (occupancy; trials are measured after reverts)."""
    rng = np.random.default_rng(seed)
    col = rng.integers(0, X, (M, N)) if col0 is None else col0.copy()
    pending = np.zeros((M, N), bool); oldc = col.copy(); olds = np.zeros((M, N)); first = np.full(M, -1)
    sig = signal(col, counts(col, X), mode, k, pref, bonus); trace = []; occ = np.zeros(M); t_occ = int(0.75 * T)
    for t in range(T):
        worse = pending & (sig > olds + 1e-12); col = np.where(worse, oldc, col); pending[:] = False
        cnt = counts(col, X); sig = signal(col, cnt, mode, k, pref, bonus); D = dist_D(cnt, k)
        first = np.where((first < 0) & (D == 0), t, first)
        if t >= t_occ: occ += (D == 0)
        if record_every and t % record_every == 0: trace.append(D.copy())
        hungry = sig > (-bonus + 1e-12) if mode == 'dilemma' else sig > 1e-12
        tr = (rng.random((M, N)) < act) & hungry
        nbcol = col[np.arange(M)[:, None], NB[np.arange(N)[None, :], rng.integers(0, 6, (M, N))]]
        cand = np.where(rng.random((M, N)) < explore, rng.integers(0, X, (M, N)), nbcol)
        oldc = col.copy(); olds = sig.copy(); pending = tr & (cand != col); col = np.where(pending, cand, col)
        sig = signal(col, counts(col, X), mode, k, pref, bonus)
    worse = pending & (sig > olds + 1e-12); col = np.where(worse, oldc, col)   # settle last trials
    return col, first, np.array(trace), occ / (T - t_occ)
