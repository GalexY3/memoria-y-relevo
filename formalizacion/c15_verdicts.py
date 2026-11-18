"""Evaluates the preregistered C15 hypotheses (PREREG_C15_ULTRAESTABILIDAD.md) from c15_PRIMARY.json."""
import json
from pathlib import Path
R = Path(__file__).resolve().parent / 'C15_RESULTS'
rows = json.loads((R / 'c15_PRIMARY.json').read_text(encoding='utf-8'))['rows']; pred = json.loads((R / 'c15_predictions.json').read_text(encoding='utf-8'))
g = {(r['exp'], r['name']): r for r in rows}; a = lambda x, L: g[(x, f'ultra_L{L}')]['adapt_ever']
V = dict(
    U1=all(abs(a(x, L) - pred[f'{x}_L{L}']) <= 0.04 for x in 'BC' for L in (400, 800)),
    U2=all(a(x, 100) <= pred[f'{x}_L100'] - 0.15 for x in 'BC'),
    U3=all(r['stab_any_step'] <= 0.01 for r in rows),
    U4=all(a(x, 400) >= 0.80 for x in 'BC') and all(g[(x, 'no_loop')]['adapt_ever'] <= 0.05 for x in 'BC'),
    U5=abs(g[('C', 'ultra_L800')]['share_one_step'] - 0.50) <= 0.07)
out = dict(verdicts={k: 'CONFIRMADA' if v else 'REFUTADA' for k, v in V.items()},
           table=[dict(exp=x, L=L, observed=a(x, L), predicted=pred[f'{x}_L{L}'], steps_med=g[(x, f'ultra_L{L}')]['steps_med'],
                       share_one_step=g[(x, f'ultra_L{L}')]['share_one_step'], adapt_meanD=g[(x, f'ultra_L{L}')]['adapt_meanD'])
                  for x in 'BC' for L in (100, 200, 400, 800)],
           no_loop={x: g[(x, 'no_loop')]['adapt_ever'] for x in 'BC'})
(R / 'c15_verdicts_PRIMARY.json').write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print(json.dumps(out['verdicts'], indent=1))
for t in out['table']:
    print(t['exp'], 'L', t['L'], 'obs %.3f pred %.3f diff %+.3f | steps med %s one-step %.2f | err %.2f' % (t['observed'], t['predicted'], t['observed'] - t['predicted'], t['steps_med'], t['share_one_step'], t['adapt_meanD']))
print('no loop', out['no_loop'])
