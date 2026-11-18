"""Evaluates the preregistered C18 hypotheses (PREREG_C18_UMBRAL_DE_SANCION.md). Usage: python c18_verdicts.py [PRIMARY|SMOKE]"""
import json, sys
from math import ceil
from pathlib import Path
R = Path(__file__).resolve().parent / 'C18_RESULTS'; tag = sys.argv[1] if len(sys.argv) > 1 else 'PRIMARY'
th = json.loads((R / ('c18_PRIMARY_theory.json' if tag == 'PRIMARY' else 'c18_theory.json')).read_text(encoding='utf-8'))['checks']
st = json.loads((R / f'c18_{tag}_stair.json').read_text(encoding='utf-8'))['rows']
ro = json.loads((R / f'c18_{tag}_rot.json').read_text(encoding='utf-8'))['rows']
g = {(r['lam'], r['q'], r['v_min']): r for r in st}; a = lambda l, q, v: g[(l, q, v)]['adapt_ever']; t = lambda l, q, v: g[(l, q, v)]['t_med']
T = 20
j_lam = lambda l: max(1, ceil(round(T * (1 - l) / 2, 9)))
jstar = {(l, v): max(v, j_lam(l)) for v in (1, 2, 3, 4) for l in (1.0, 0.9, 0.8, 0.7)}
def band(js, x):
    return x >= 0.95 if js <= 2 else (0.05 <= x <= 0.40 if js == 3 else x <= 0.02)
rg = {(r['q'], r['v_min']): r for r in ro}
V = dict(
    P1=all(th[k]['observed'] == th[k]['predicted'] for k in ('lone_v2', 'lone_v3', 'scattered3_v3', 'lone_v1'))
       and all(th[k]['max_abs_z'] <= 3 for k in ('pair_v3', 'triangle_v4')),
    P2=all(band(js, a(l, 1.0, v)) for (l, v), js in jstar.items()),
    P3=all(abs(a(0.7, 1.0, v) - a(0.7, 0.0, 3)) <= 0.08 for v in (1, 2, 3)) and all(abs(a(l, 1.0, 1) - a(l, 0.0, 3)) <= 0.08 for l in (1.0, 0.9, 0.8)),
    P4=all(a(1.0, 0.2, v) >= 0.95 and t(1.0, 0.2, v) <= 0.75 * t(1.0, 0.0, 3) for v in (2, 3)),
    P5=all(rg[(1.0, v)]['adapt_ever'] <= 0.02 and rg[(1.0, v)]['stab_meanD'] <= 1.0 for v in (2, 3))
       and abs(rg[(1.0, 1)]['adapt_ever'] - rg[(0.0, 3)]['adapt_ever']) <= 0.10)
out = dict(verdicts={k: 'CONFIRMADA' if v else 'REFUTADA' for k, v in V.items()}, jstar={f'{l},{v}': js for (l, v), js in jstar.items()},
           theory=th, stair=[(r['lam'], r['q'], r['v_min'], round(r['adapt_ever'], 3), r['t_med'], round(r['adapt_meanD'], 2)) for r in st],
           rot=[(r['q'], r['v_min'], round(r['stab_meanD'], 3), round(r['adapt_ever'], 3)) for r in ro])
(R / f'c18_verdicts_{tag}.json').write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print(json.dumps(out['verdicts'], indent=1)); print(json.dumps(out['jstar']))
for row in out['stair'] + out['rot']:
    print(row)
