"""C17 figure from the PRIMARY JSONs: (a) substitution law, stability against rho = (1 - c)(1 - s) under C and D;
(b) adaptation against rho (resonance); (c) stability-adaptation frontier of each compensator under C (c = 0)."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker
H = Path(__file__).resolve().parent; R = H / 'C17_RESULTS'
rows = json.loads((R / 'c17_PRIMARY_C.json').read_text(encoding='utf-8'))['rows'] + json.loads((R / 'c17_PRIMARY_D.json').read_text(encoding='utf-8'))['rows']
CC = {0.0: '#2a6f97', 0.5: '#3a7d44', 0.8: '#c8553d', 0.95: '#6a4c93'}
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
cs = [r for r in rows if r['signal'] == 'C' and r['q'] == 0 and r['s'] < 1]
for k, (key, lab) in enumerate([('stab_meanD', 'desorden en la fase estable (D medio)'), ('adapt_ever', 'adaptación (fracción que crea la 5.ª categoría)')]):
    a = ax[k]
    for c, colr in CC.items():
        pts = sorted([((1 - r['c']) * (1 - r['s']), r[key]) for r in cs if r['c'] == c and (c > 0 or r['s'] in (0.0, 0.5, 0.8, 0.95))])
        a.plot([p[0] for p in pts], [p[1] for p in pts], 'o-', color=colr, label=f'C, cristalización c = {c}')
    if key == 'stab_meanD':
        d = sorted([(1 - r['c'], r[key]) for r in rows if r['signal'] == 'D' and r['s'] == 0 and r['q'] == 0])
        a.plot([p[0] for p in d], [p[1] for p in d], 'k^--', label='D (con modelo), s = 0')
    a.set_xscale('log'); a.set_xlabel('ρ = (1 − c)(1 − s): reentradas ni reconocidas ni socializadas'); a.set_ylabel(lab)
    a.legend(fontsize=7)
ax[0].set_title('(a) Ley de sustitución: c y s actúan a través de ρ', fontsize=10)
ax[1].set_title('(b) La adaptación es máxima con ρ intermedio', fontsize=10)
a = ax[2]
soc = sorted([(r['stab_meanD'], r['adapt_ever'], r['s']) for r in rows if r['signal'] == 'C' and r['c'] == 0 and r['q'] == 0])
san = sorted([(r['stab_meanD'], r['adapt_ever'], r['q']) for r in rows if r['signal'] == 'C' and r['c'] == 0 and r['q'] > 0 and r['s'] == 0])
cry = sorted([(r['stab_meanD'], r['adapt_ever'], r['c']) for r in rows if r['signal'] == 'C' and r['s'] == 0 and r['q'] == 0])
for pts, mk, colr, lab, sym in [(soc, 'o-', '#2a6f97', 'socialización s (c = 0)', 's'), (san, 's-', '#c8553d', 'sanción q (c = 0)', 'q'), (cry, 'd-', '#6a4c93', 'cristalización c (s = 0)', 'c')]:
    a.plot([p[0] for p in pts], [p[1] for p in pts], mk, color=colr, label=lab)
    for x, y, v in pts:
        if v in (0.2, 0.5, 1.0, 0.99, 0.95):
            a.annotate(f'{sym}={v}', (x, y), fontsize=6, xytext=(3, 3), textcoords='offset points', color=colr)
a.axvline(10, color='0.6', ls=':', lw=1); a.set_xscale('log'); a.set_xticks([1, 2, 5, 10, 20, 50]); a.set_xticklabels(['1', '2', '5', '10', '20', '50'])
a.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
a.set_xlabel('desorden en la fase estable (D medio, escala log)'); a.set_ylabel('adaptación (adapt_ever)')
a.set_title('(c) A igual orden, la sanción conserva más capacidad de crear', fontsize=10); a.legend(fontsize=7)
fig.suptitle('C17. Robustez compensatoria bajo rotación continua (τ = 20, M = 512, señal C salvo indicación)', fontsize=11)
fig.tight_layout(); fig.savefig(R / 'c17_figura.png', dpi=140)
print('ok')
