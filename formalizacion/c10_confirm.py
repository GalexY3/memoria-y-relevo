"""C10 confirmation (PREREGISTERED in PREREG_C10_PARADOJA_GATEKEEPING.md; seeds 8160xx).
Usage: python c10_confirm.py [M] [scale]   (defaults M=512, scale=1; scale<1 shortens phases for smoke tests)"""
import json, sys, time, hashlib
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D
from c10_sim import run_phases
M = int(sys.argv[1]) if len(sys.argv) > 1 else 512
SC = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
X = 16; t0 = time.time(); S_GRID = [0.0, 0.5, 0.75, 0.9, 0.95, 0.98, 1.0]
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=int(4000 * SC), seed=816000)
col = col[dist_D(counts(col, X), 4) == 0]; n = int(col.shape[0])
main, alt = [], []
for ti, tau in enumerate([20, 80]):
    for gi, sig in enumerate(['coll', 'D']):
        for si, s in enumerate(S_GRID):
            (a, b), _ = run_phases(col, [(sig, 4, int(4000 * SC)), (sig, 5, int(6000 * SC))], s, tau,
                                   seed=816100 + 10 * ti + gi, entry_seed=816200 + 10 * ti + gi)
            main.append(dict(tau=tau, signal=sig, s=s, n=n,
                             stab_meanD=float(a['meanD'].mean()), stab_occ=float(a['occupancy'].mean()), stab_colours=float(a['mean_colours'].mean()),
                             adapt_meanD=float(b['meanD'].mean()), adapt_ever=float((b['first'] >= 0).mean()),
                             adapt_occ=float(b['occupancy'].mean()), adapt_colours=float(b['mean_colours'].mean())))
            print('main', {k: (round(v, 3) if isinstance(v, float) else v) for k, v in main[-1].items()}, flush=True)
# descriptive: alternating environment 4,5,4,5 (no hypothesis), tau=80
for gi, sig in enumerate(['coll', 'D']):
    for si, s in enumerate(S_GRID):
        res, _ = run_phases(col, [(sig, 4, int(2500 * SC)), (sig, 5, int(2500 * SC)), (sig, 4, int(2500 * SC)), (sig, 5, int(2500 * SC))], s, 80,
                            seed=816300 + gi, entry_seed=816400 + gi)
        alt.append(dict(signal=sig, s=s, n=n, phase_meanD=[float(r['meanD'].mean()) for r in res],
                        overall_meanD=float(np.mean([r['meanD'].mean() for r in res]))))
        print('alt', alt[-1], flush=True)
status = 'PRIMARY' if (M == 512 and SC == 1.0) else 'SMOKE'
(H / 'C10_RESULTS' / f'c10_{status}.json').write_text(json.dumps(dict(status=status, M=M, n_established=n, scale=SC, main=main, alternating=alt,
    sha256={f: hashlib.sha256((H / f).read_bytes()).hexdigest() for f in ['c10_sim.py', 'c10_confirm.py']}, seconds=time.time() - t0), indent=1),
    encoding='utf-8', newline=chr(10))
print('done', status, round(time.time() - t0), 's')
