"""C09 exact landscape analysis of the two collective signals on group-size profiles.

State = multiset of positive group sizes summing to N (colours are exchangeable). A single move takes
one agent from group i to an existing group j or to a new group. Costs:
  C (original collective): sum over present groups |s - T|
  D (corrected):           L1 distance to the nearest balanced k-partition
For each non-solved state we compute: does a strictly improving move exist? Can the solved state be
reached by a path of non-worsening moves (dynamics that accept neutral moves)? Classified by m, the
number of present groups, relative to k."""
import sys, json
from functools import lru_cache
from collections import Counter, defaultdict

def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield (); return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - p, p): yield (p,) + rest

def C(s, T): return sum(abs(x - T) for x in s)
def D(s, k, T):
    s = sorted(s, reverse=True); top = s[:k] + [0] * max(0, k - len(s))
    return sum(abs(x - T) for x in top) + sum(s[k:])

def moves(s):
    s = list(s); out = set()
    for i in range(len(s)):
        for j in range(len(s) + 1):
            if i == j: continue
            t = s.copy(); t[i] -= 1
            if j == len(s): t.append(1)
            else: t[j] += 1
            out.add(tuple(sorted([x for x in t if x > 0], reverse=True)))
    return out

def analyse(N, k):
    T = N // k; solved = tuple([T] * k); states = list(partitions(N))
    res = {}
    for name, f in [('C', lambda s: C(s, T)), ('D', lambda s: D(s, k, T))]:
        cost = {s: f(s) for s in states}; nb = {s: moves(s) for s in states}
        # reverse search from solved over non-worsening moves: s -> t allowed if cost[t] <= cost[s]
        rev = defaultdict(list)
        for s in states:
            for t in nb[s]:
                if cost[t] <= cost[s]: rev[t].append(s)
        reach = {solved}; stack = [solved]
        while stack:
            t = stack.pop()
            for s in rev[t]:
                if s not in reach: reach.add(s); stack.append(s)
        tab = Counter()
        for s in states:
            if s == solved: continue
            m = len(s); rel = 'm<k' if m < k else ('m=k' if m == k else 'm>k')
            strict = any(cost[t] < cost[s] for t in nb[s])
            tab[(rel, 'has_strict_improvement' if strict else 'NO_strict_improvement', 'reaches_solved' if s in reach else 'TRAPPED')] += 1
        res[name] = {' | '.join(key): v for key, v in sorted(tab.items())}
    # identity checks
    eq = all(C(s, T) == D(s, k, T) for s in states if len(s) == k)
    newc = min(C(sorted(list(s[:i]) + [s[i] - 1] + list(s[i + 1:]) + [1]), T) - C(s, T) for s in states for i in range(len(s)) if s[i] > 1)
    return dict(N=N, k=k, T=T, n_states=len(states), C_equals_D_when_m_eq_k=eq, min_cost_change_of_new_group_under_C=newc, table=res)

if __name__ == '__main__':
    out = [analyse(N, k) for N, k in [(12, 3), (16, 4), (20, 4), (24, 4), (30, 5), (32, 4)]]
    for r in out:
        print(f"N={r['N']} k={r['k']} T={r['T']} states={r['n_states']} C==D|m=k:{r['C_equals_D_when_m_eq_k']} min dC(new group)={r['min_cost_change_of_new_group_under_C']}")
        for sig in ['C', 'D']:
            for key, v in r['table'][sig].items(): print('   ', sig, key, v)
    json.dump(out, open('c09_theory_results.json', 'w', encoding='utf-8', newline='\n'), indent=1)
