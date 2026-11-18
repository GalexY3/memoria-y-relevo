"""Figure C10: gatekeeping paradox (stability vs adaptation by socialization) and collapse on the
inflow rate of unsocialized newcomers."""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
H = Path(__file__).resolve().parent
d = json.loads((H / 'C10_RESULTS' / 'c10_PRIMARY.json').read_text(encoding='utf-8'))
RED, BLUE = '#c0504d', '#4f81bd'
fig, ax = plt.subplots(1, 3, figsize=(13.5, 4.1))
for a, sig, title in [(ax[0], 'coll', 'a) Señal original C (sin modelo del número de grupos)'), (ax[1], 'D', 'b) Señal D (con modelo de la estructura)')]:
    for tau, ls in [(20, '-'), (80, '--')]:
        rs = sorted([r for r in d['main'] if r['signal'] == sig and r['tau'] == tau], key=lambda r: r['s'])
        x = [r['s'] for r in rs]
        a.plot(x, [r['stab_meanD'] for r in rs], ls, marker='o', color='#555555', ms=4, label=f'estabilidad (k=4), τ={tau}')
        a.plot(x, [r['adapt_meanD'] for r in rs], ls, marker='s', color=RED if sig == 'coll' else BLUE, ms=4, label=f'adaptación (k=5), τ={tau}')
    a.set_xlabel('Fracción de recién llegados socializados (s)'); a.set_title(title, fontsize=9.5)
    a.set_ylim(-1, 60)
ax[0].set_ylabel('Error estructural medio (menor es mejor)'); ax[0].legend(fontsize=7, frameon=False, loc='upper right')
for sig, col in [('coll', RED), ('D', BLUE)]:
    for tau, mk in [(20, 'o'), (80, 's')]:
        rs = sorted([r for r in d['main'] if r['signal'] == sig and r['tau'] == tau and r['s'] < 1], key=lambda r: (1 - r['s']) / tau)
        x = [(1 - r['s']) / tau for r in rs]
        ax[2].plot(x, [r['adapt_meanD'] for r in rs], marker=mk, color=col, ms=5, lw=1,
                   label=f"{'C' if sig == 'coll' else 'D'}, τ={tau}", mfc='none' if tau == 80 else col)
ax[2].set_xscale('log'); ax[2].set_xlabel('Entradas no socializadas por tick, (1 − s)/τ')
ax[2].set_title('c) Adaptación según la tasa de desviación', fontsize=9.5); ax[2].legend(fontsize=7, frameon=False)
for a in ax: a.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); out = H / 'C10_RESULTS' / 'c10_figura.png'; fig.savefig(out, dpi=160); print(out)
