"""C15 analytic prediction: expected number of random canon steps until the canon has exactly k_new categories, for
the ultrastable loop (symmetric +/-1 random walk on the canon size 0..X, forced add at 0 and forced remove at X),
starting from k_old. Exact absorbing-chain solution. Usage: python c15_markov.py"""
import numpy as np, json, sys
def expected_steps(k_old, k_new, X=16):
    states = [c for c in range(X + 1) if c != k_new]; idx = {c: i for i, c in enumerate(states)}
    A = np.eye(len(states)); bvec = np.ones(len(states))
    for c in states:
        nxt = [(c + 1, 1.0)] if c == 0 else ([(c - 1, 1.0)] if c == X else [(c + 1, 0.5), (c - 1, 0.5)])
        for d, p in nxt:
            if d != k_new:
                A[idx[c], idx[d]] -= p
    E = np.linalg.solve(A, bvec)
    return float(E[idx[k_old]])
out = {f'{a}->{b}': expected_steps(a, b) for a, b in [(4, 5), (5, 4), (2, 4), (4, 2)]}
print(json.dumps(out, indent=1))
