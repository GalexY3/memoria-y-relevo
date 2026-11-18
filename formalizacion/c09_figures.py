"""Figures for C09: (a) recovery vs turnover fraction with the analytic vocabulary-survival curve;
(b) tempo of the same 30 replacements; (c) long-horizon recovery under the original signal."""
import json, sys
from math import comb
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
H = Path(__file__).resolve().parent
d = json.loads((H / 'C09_RESULTS' / 'c09_PRIMARY_M512.json').read_text(encoding='utf-8'))
RED, BLUE, GREY = '#c0504d', '#4f81bd', '#7f7f7f'
P = lambda n, k=4, N=100: sum((-1) ** j * comb(k, j) * comb(N - j * (N // k), n) for j in range(k + 1)) / comb(N, n)
fig, ax = plt.subplots(1, 3, figsize=(13, 3.9))
# (a)
e1 = [r for r in d['E1'] if r['layout'] == 'dispersed']
fs = sorted({r['f'] for r in e1}); fg = np.linspace(0.3, 0.97, 200)
ax[0].plot(fg, [P(round(100 * (1 - f))) if 100 * (1 - f) >= 1 else 0 for f in fg], color=GREY, lw=1.5, label='predicción analítica (vocabulario completo)')
for sig, entry, c, mk, lab in [('coll', 'vocab', RED, 'o', 'original, entran con colores de la comunidad'),
                               ('coll', 'random', RED, 'x', 'original, entran con cualquier color'),
                               ('D', 'vocab', BLUE, 's', 'corregida D, colores de la comunidad'),
                               ('D', 'random', BLUE, '+', 'corregida D, cualquier color')]:
    y = [next(r['recovery'] for r in e1 if r['f'] == f and r['signal'] == sig and r['entry'] == entry) for f in fs]
    ax[0].plot(fs, y, mk, color=c, ms=6, label=lab, mfc='none' if mk in 'os' else None)
ax[0].set_xlabel('Fracción de la comunidad sustituida'); ax[0].set_ylabel('Comunidades que recuperan 4×25')
ax[0].set_title('a) Cuánto relevo', fontsize=10); ax[0].legend(fontsize=6.5, frameon=False, loc='center left', bbox_to_anchor=(0.0, 0.45))
# (b)
e2 = d['E2']; ds = [0, 1, 10, 100]; xs = range(4)
for sig, c, lab in [('coll', RED, 'señal original'), ('D', BLUE, 'señal corregida D')]:
    ax[1].plot(xs, [next(r['recovery'] for r in e2 if r['delta'] == dl and r['signal'] == sig) for dl in ds], 'o-', color=c, label=lab)
ax[1].set_xticks(list(xs)); ax[1].set_xticklabels(['a la vez', 'cada 1', 'cada 10', 'cada 100'])
ax[1].set_xlabel('Ritmo de los mismos 30 relevos (ticks entre entradas)'); ax[1].set_ylim(-0.03, 1.03)
ax[1].set_title('b) A qué ritmo (entran con cualquier color)', fontsize=10); ax[1].legend(fontsize=7, frameon=False)
# (c)
e3 = d['E3'][0]; fh = np.array(e3['first_hit']); tg = np.unique(np.r_[np.geomspace(10, e3['T'], 120).astype(int), e3['T']])
ax[2].plot(tg, [((fh >= 0) & (fh <= t)).mean() for t in tg], color=RED)
ax[2].set_xscale('log'); ax[2].set_xlabel('Ticks desde el relevo (escala log)'); ax[2].set_ylim(-0.03, 1.03)
ax[2].set_title('c) Cuánto tarda (original, cualquier color, 30%)', fontsize=10)
for a in ax: a.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); out = H / 'C09_RESULTS' / 'c09_figura.png'; fig.savefig(out, dpi=160); print(out)
