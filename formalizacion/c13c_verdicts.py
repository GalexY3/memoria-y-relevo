"""Evaluates the preregistered C13c hypotheses (PREREG_C13C_FILO_DE_LA_DIVISORIA.md) from c13c_PRIMARY.json."""
import json
from pathlib import Path
R = Path(__file__).resolve().parent / 'C13_RESULTS'
rows = json.loads((R / 'c13c_PRIMARY.json').read_text(encoding='utf-8'))['rows']
g = {(r['change'], r['name']): r for r in rows}
rel = lambda c: g[(c, 'relief')]; t3 = lambda c: g[(c, 'theta_T/3')]
V = dict(
    W1=rel('5->4')['adapt_ever'] >= 0.95 and rel('5->4')['adapt_meanD'] < t3('5->4')['adapt_meanD'],
    W2=all(rel(c)['adapt_ever'] <= 0.93 and rel(c)['adapt_meanD'] >= 1.5 * t3(c)['adapt_meanD'] for c in ('4->2', '10->5')),
    W3=rel('5->4')['adapt_meanD'] < rel('5->2')['adapt_meanD'] and rel('10->5')['adapt_meanD'] < rel('10->4')['adapt_meanD'],
    W4=all(rel(c)['adapt_canon_size'] < rel(c)['k_new'] for c in ('5->2', '10->4')) and rel('5->4')['adapt_canon_size'] >= 4 - 0.3,
    W5=all(t3(c)['adapt_ever'] >= 0.99 for c in ('5->4', '4->2', '10->5', '5->2', '10->4')))
out = dict(verdicts={k: 'CONFIRMADA' if v else 'REFUTADA' for k, v in V.items()},
           table=[{k: r[k] for k in ('change', 'ratio', 'name', 'theta', 'adapt_meanD', 'adapt_ever', 'adapt_canon_size', 'share_canon_below_k', 't_canon_k')} for r in rows])
(R / 'c13c_verdicts_PRIMARY.json').write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print(json.dumps(out['verdicts'], indent=1))
for r in out['table']:
    print(r['change'], '%.1f' % r['ratio'], r['name'].ljust(12), 'err %.2f ever %.3f canon %.2f below_k %.2f tk %s' % (r['adapt_meanD'], r['adapt_ever'], r['adapt_canon_size'], r['share_canon_below_k'], r['t_canon_k']))
