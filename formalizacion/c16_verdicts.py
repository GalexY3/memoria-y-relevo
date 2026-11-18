"""Evaluates the preregistered C16 hypotheses (PREREG_C16_FRACCION_DE_MODELO.md) from c16_PRIMARY.json."""
import json
from pathlib import Path
R = Path(__file__).resolve().parent / 'C16_RESULTS'
rows = json.loads((R / 'c16_PRIMARY.json').read_text(encoding='utf-8'))['rows']
g = {(r['change'], r['lam']): r for r in rows}; a = lambda c, l: g[(c, l)]['adapt_ever']; t = lambda c, l: g[(c, l)]['t_med']
V = dict(
    Q1=all(a('4->5', l) >= 0.95 for l in (0.8, 0.85, 0.89, 0.9, 1.0)) and all(a('4->5', l) <= 0.35 for l in (0.7, 0.75, 0.79))
       and all(a('4->5', l) <= 0.02 for l in (0.0, 0.3, 0.55)),
    Q2=a('4->5', 0.8) - a('4->5', 0.79) >= 0.5,
    Q3=all(a('5->10', l) >= 0.80 for l in (0.6, 0.65, 0.7)) and a('4->5', 0.65) <= 0.05,
    Q4=a('5->4', 0.0) <= 0.15 and all(a('5->4', l) >= 0.95 for l in (0.05, 0.1)),
    Q5=(t('4->5', 0.9) + t('4->5', 1.0)) / 2 < (t('4->5', 0.8) + t('4->5', 0.85)) / 2)
out = dict(verdicts={k: 'CONFIRMADA' if v else 'REFUTADA' for k, v in V.items()},
           table=[(r['change'], r['lam'], r['adapt_ever'], r['t_med'], round(r['adapt_meanD'], 2)) for r in rows])
(R / 'c16_verdicts_PRIMARY.json').write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print(json.dumps(out['verdicts'], indent=1))
for row in out['table']:
    print(row)
