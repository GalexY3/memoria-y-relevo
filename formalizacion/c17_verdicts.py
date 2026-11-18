"""Evaluates the preregistered C17 hypotheses (PREREG_C17_ROBUSTEZ_COMPENSATORIA.md) from c17_PRIMARY_C.json and _D.json."""
import json, sys
from pathlib import Path
R = Path(__file__).resolve().parent / 'C17_RESULTS'
tag = sys.argv[1] if len(sys.argv) > 1 else 'PRIMARY'; rows = []
for p in ('C', 'D'):
    rows += json.loads((R / f'c17_{tag}_{p}.json').read_text(encoding='utf-8'))['rows']
g = {(r['signal'], r['c'], r['s'], r['q']): r for r in rows}
st = lambda sig, c, s, q=0.0: g[(sig, c, s, q)]['stab_meanD']
ad = lambda sig, c, s, q=0.0: g[(sig, c, s, q)]['adapt_ever']
CS = (0.0, 0.5, 0.8, 0.95)
pairs = [((0.0, 0.5), (0.5, 0.0)), ((0.0, 0.8), (0.8, 0.0)), ((0.5, 0.8), (0.8, 0.5)),
         ((0.0, 0.95), (0.95, 0.0)), ((0.5, 0.95), (0.95, 0.5)), ((0.8, 0.95), (0.95, 0.8))]   # rho = 0.5, 0.2, 0.1, 0.05, 0.025, 0.01
pm = [(st('C', *a) + st('C', *b)) / 2 for a, b in pairs]
rel = [abs(st('C', *a) - st('C', *b)) / ((st('C', *a) + st('C', *b)) / 2) for a, b in pairs]
def s_min(c):
    ok = [s for s in (0.0, 0.5, 0.8, 0.95, 1.0) if st('C', c, s) <= 20]
    return min(ok) if ok else None
smin = {c: s_min(c) for c in CS}
peak = [ad('C', 0.5, 0.95), ad('C', 0.95, 0.5), ad('C', 0.8, 0.95), ad('C', 0.95, 0.8)]       # 0.01 <= rho <= 0.025
soc0 = [(st('C', 0.0, s), ad('C', 0.0, s)) for s in (0.0, 0.5, 0.8, 0.95, 0.97, 0.98, 0.99, 1.0)]
san0 = [(st('C', 0.0, 0.0, q), ad('C', 0.0, 0.0, q)) for q in (0.05, 0.1, 0.2, 0.3, 0.5, 1.0)]
best = lambda L: max([a for d, a in L if d <= 10], default=0.0)
V = dict(
    R1=st('C', 0.0, 0.0) >= 40 and all(st('D', c, 0.0) <= 8 for c in CS),
    R2=max(rel) <= 0.30 and all(pm[i] > pm[i + 1] for i in range(len(pm) - 1)),
    R3=all(smin[c] is not None for c in CS) and all(smin[CS[i]] >= smin[CS[i + 1]] for i in range(3)) and smin[0.95] <= smin[0.0] - 0.9
       and st('C', 0.8, 0.0, 0.05) <= 20 < st('C', 0.0, 0.0, 0.05),
    R4=all(ad('C', *x) <= 0.05 for x in ((0.0, 0.0), (0.0, 0.5), (0.5, 0.0))) and min(peak) >= 0.6
       and all(ad('C', c, 1.0) <= 0.02 for c in CS) and ad('C', 0.95, 0.95) < min(peak),
    R5=all(ad('D', c, 1.0) >= 0.95 for c in CS),
    R6=best(san0) - best(soc0) >= 0.10,
    R7=ad('C', 0.95, 0.0, 0.2) <= ad('C', 0.0, 0.0, 0.2) - 0.4 and ad('C', 0.95, 0.0, 0.05) - ad('C', 0.95, 0.0, 0.2) >= 0.3,
    R8=ad('D', 0.0, 0.0, 1.0) <= 0.5 and ad('D', 0.0, 0.0, 0.2) >= 0.95)
out = dict(verdicts={k: 'CONFIRMADA' if v else 'REFUTADA' for k, v in V.items()},
           details=dict(pair_means=pm, pair_rel_diff=rel, s_min=smin, peak=peak, best_sanction_D_le_10=best(san0), best_socialisation_D_le_10=best(soc0)),
           table=[(r['signal'], r['c'], r['s'], r['q'], round(r['stab_meanD'], 2), round(r['adapt_meanD'], 2), round(r['adapt_ever'], 3)) for r in rows])
(R / f'c17_verdicts_{tag}.json').write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print(json.dumps(out['verdicts'], indent=1)); print(json.dumps(out['details'], indent=1))
for row in out['table']:
    print(row)
