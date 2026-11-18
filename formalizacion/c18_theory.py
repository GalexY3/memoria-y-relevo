"""C18 exact check of Proposition 8 (TEOREMA_C18.md) on the frozen C17 simulator: one sanction step (q = 1), no trial
moves (act = 0), no turnover. Planted configurations on stable 4x25 states (seeds 8800xx):
  lone pioneer (v_min = 2, 3)      -> predicted removal with certainty
  adjacent pair (v_min = 3)        -> each member survives w.p. 1/6 independently (P0, P1, P2 = 25/36, 10/36, 1/36)
  adjacent triangle (v_min = 4)    -> each member survives w.p. 2/6 independently
  scattered trio (v_min = 3)       -> established: untouched with certainty
  lone pioneer (v_min = 1)         -> established: untouched with certainty
Usage: python c18_theory.py [M] [SEED_BASE]   (pilot: 880000; preregistered confirmation: 881000)"""
import json, sys
from pathlib import Path
import numpy as np
from math import comb
H = Path(__file__).resolve().parent; C17 = H.parent / 'claude_cycle17'
sys.path.insert(0, str(C17)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, NB, N
from c17_sim import run
M = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
SB = int(sys.argv[2]) if len(sys.argv) > 2 else 880000; TAG = 'PRIMARY' if SB == 881000 else 'pilot'
X = 16; rng = np.random.default_rng(SB + 1)
base, _, _, _ = trial_and_revert(256, 'D', 0.05, 0.1, T=4000, seed=SB); base = base[dist_D(counts(base, X), 4) == 0]
NBS = [set(NB[a]) for a in range(N)]

def plant(kind):
    col = base[rng.integers(0, base.shape[0], M)].copy(); members = []
    for i in range(M):
        x = [c for c in range(X) if not (col[i] == c).any()][0]
        a = int(rng.integers(0, N))
        if kind == 'lone':
            m = [a]
        elif kind == 'pair':
            m = [a, int(NB[a, rng.integers(0, 6)])]
        elif kind == 'triangle':
            b = int(NB[a, rng.integers(0, 6)]); common = sorted(NBS[a] & NBS[b]); m = [a, b, int(common[rng.integers(0, len(common))])]
        elif kind == 'scattered3':
            while True:
                m = list(rng.choice(N, 3, replace=False))
                if all(m[u] not in NBS[m[v]] for u in range(3) for v in range(3) if u != v):
                    break
        col[i, m] = x; members.append((x, m))
    return col, members

out = {}
for name, kind, vmin, p_surv in [('lone_v2', 'lone', 2, 0.0), ('lone_v3', 'lone', 3, 0.0), ('pair_v3', 'pair', 3, 1 / 6),
                                 ('triangle_v4', 'triangle', 4, 2 / 6), ('scattered3_v3', 'scattered3', 3, 1.0), ('lone_v1', 'lone', 1, 1.0)]:
    col, members = plant(kind)
    _, st = run(col, 'mix', [(5, 1)], lam=1.0, tau=0, q=1.0, v_min=vmin, act=0.0, seed=SB + 2, entry_seed=SB + 3)
    after = st['col']; j = len(members[0][1])
    surv = np.array([sum(int(after[i, a] == x) for a in m) for i, (x, m) in enumerate(members)])
    obs = np.bincount(surv, minlength=j + 1) / M
    pred = np.array([comb(j, k) * p_surv ** k * (1 - p_surv) ** (j - k) for k in range(j + 1)])
    se = np.sqrt(pred * (1 - pred) / M)
    out[name] = dict(j=j, v_min=vmin, p_member=p_surv, observed=obs.round(4).tolist(), predicted=pred.round(4).tolist(),
                     max_abs_z=float(np.max(np.where(se > 0, np.abs(obs - pred) / np.where(se > 0, se, 1), np.where(obs == pred, 0, np.inf)))))
    print(name, out[name], flush=True)
(H / 'C18_RESULTS' / ('c18_theory.json' if TAG == 'pilot' else 'c18_PRIMARY_theory.json')).write_text(json.dumps(dict(status=TAG, M=M, seed_base=SB, checks=out), indent=1), encoding='utf-8', newline=chr(10))
