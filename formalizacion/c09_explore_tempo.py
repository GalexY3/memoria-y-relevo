"""C09 EXPLORATORY (post hoc, after P2a was refuted; seeds 8130xx): slower tempos and the fate of a
single foreign newcomer. Not part of the preregistered test."""
import json, sys
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, N
from c09_sim import run, dispersed
M = 256; X = 16; out = {}
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, seed=813000); col = col[dist_D(counts(col, X), 4) == 0]; M = col.shape[0]
# (a) one foreign newcomer: probability its colour is gone after t ticks, and recovery
rep1 = dispersed(M, 1, np.random.default_rng(813001))
newc = np.array([np.setdiff1d(np.arange(X), np.unique(col[i]))[0] for i in range(M)])
c1 = col.copy(); c1[rep1] = newc
hits = {}
for T in [25, 100, 400, 1600, 6400]:
    cT, first, _ = run(c1, 'coll', T, seed=813002, events=None)
    hits[T] = dict(foreign_gone=float(np.mean([(cT[i] == newc[i]).sum() == 0 for i in range(M)])), solved=float((dist_D(counts(cT, X), 4) == 0).mean()),
                   foreign_size_mean_if_alive=float(np.mean([(cT[i] == newc[i]).sum() for i in range(M) if (cT[i] == newc[i]).sum() > 0])) if any((cT[i] == newc[i]).sum() > 0 for i in range(M)) else None)
    print('single', T, hits[T], flush=True)
out['single_foreign_newcomer'] = hits
# (b) slower tempos for the 30 replacements
rep30 = dispersed(M, 30, np.random.default_rng(813003)); rows = []
for delta in [1000, 4000]:
    events = {}
    for i in range(M):
        for e, a in enumerate(np.nonzero(rep30[i])[0]): events.setdefault(e * delta, np.zeros((M, N), bool))[i, a] = True
    last = max(events)
    _, first, _ = run(col, 'coll', last + 4001, seed=813004, events=events, entry='random', entry_seed=813005)
    rows.append(dict(delta=delta, recovery=float((first >= 0).mean()))); print(rows[-1], flush=True)
out['slow_tempo'] = rows
(H / 'C09_RESULTS' / 'c09_explore_tempo.json').write_text(json.dumps(dict(status='EXPLORATORY_POST_HOC', M=M, **out), indent=1), encoding='utf-8', newline=chr(10))
