"""C17 confirmatory run (PREREG_C17_ROBUSTEZ_COMPENSATORIA.md). New seeds 8710xx, M = 512, tau = 20.
Institutions 4x25 under continuous re-entry; stable phase k = 4 (4000 ticks), then the environment asks k = 5
(6000 ticks). Usage: python c17_confirm.py C|D [M; anything but 512 writes a SMOKE file]  (the two parts can run in parallel; c17_verdicts.py merges them)."""
import json, sys, time
from pathlib import Path
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D
from c17_sim import run
part = sys.argv[1]; M = int(sys.argv[2]) if len(sys.argv) > 2 else 512; tag = 'PRIMARY' if M == 512 else 'SMOKE'; t0 = time.time(); rows = []
col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=4000, seed=871000); col = col[dist_D(counts(col, 16), 4) == 0]
if part == 'C':
    grid = [(c, s, 0.0) for c in (0.0, 0.5, 0.8, 0.95) for s in (0.0, 0.5, 0.8, 0.95, 1.0)]
    grid += [(0.0, s, 0.0) for s in (0.97, 0.98, 0.99)]
    grid += [(0.0, 0.0, q) for q in (0.05, 0.1, 0.2, 0.3, 0.5, 1.0)] + [(0.8, 0.0, 0.05), (0.95, 0.0, 0.05), (0.95, 0.0, 0.2)]
    mode, kw0 = 'none', {}
else:
    grid = [(c, 0.0, 0.0) for c in (0.0, 0.5, 0.8, 0.95)] + [(c, 1.0, 0.0) for c in (0.0, 0.5, 0.8, 0.95)] + [(0.0, 0.0, 0.2), (0.0, 0.0, 1.0)]
    mode, kw0 = 'mix', dict(lam=1.0)
for c, s_, q_ in grid:
    (b1, b2), _ = run(col, mode, [(4, 4000), (5, 6000)], tau=20, s=s_, cryst=c, q=q_, seed=871002, entry_seed=871003, **kw0)
    r = dict(signal=part, c=c, s=s_, q=q_, n=int(col.shape[0]), stab_meanD=float(b1['meanD'].mean()), adapt_meanD=float(b2['meanD'].mean()),
             adapt_ever=float((b2['first'] >= 0).mean()), secs=round(time.time() - t0))
    rows.append(r); print(json.dumps(r), flush=True)
(H / 'C17_RESULTS' / f'c17_{tag}_{part}.json').write_text(json.dumps(dict(status=tag, part=part, M=M, rows=rows), indent=1),
                                                          encoding='utf-8', newline=chr(10))
print('done', round(time.time() - t0), 's')
