"""C18 figure from the PRIMARY JSONs: (a) adaptation under total sanction by lam and v_min, labelled with j* = max(v_min, j_lam);
(b) median adaptation time under the structural signal (lam = 1) with and without sanction."""
import json
from math import ceil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H = Path(__file__).resolve().parent; R = H / 'C18_RESULTS'
st = json.loads((R / 'c18_PRIMARY_stair.json').read_text(encoding='utf-8'))['rows']; g = {(r['lam'], r['q'], r['v_min']): r for r in st}
L = [1.0, 0.9, 0.8, 0.7]; V = [1, 2, 3, 4]; jl = lambda l: max(1, ceil(round(20 * (1 - l) / 2, 9)))
fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.4), gridspec_kw=dict(width_ratios=[1, 1.2]))
a = ax[0]; Z = np.array([[g[(l, 1.0, v)]['adapt_ever'] for v in V] for l in L])
im = a.imshow(Z, cmap='Blues', vmin=0, vmax=1, aspect='auto')
for i, l in enumerate(L):
    for j, v in enumerate(V):
        a.text(j, i, f"{Z[i, j]:.2f}\nj* = {max(v, jl(l))}", ha='center', va='center', fontsize=8, color='white' if Z[i, j] > 0.5 else 'black')
a.set_xticks(range(4)); a.set_xticklabels([f'v_min = {v}' for v in V]); a.set_yticks(range(4))
a.set_yticklabels([f'λ = {l} (j_λ = {jl(l)})' for l in L]); a.set_title('(a) Sanción total (q = 1): manda j* = max(v_min, j_λ)', fontsize=10)
fig.colorbar(im, ax=a, fraction=0.046, label='adaptación (adapt_ever)')
a = ax[1]
cases = [('sin sanción', (1.0, 0.0, 3)), ('q = 1, v_min = 2', (1.0, 1.0, 2)), ('q = 0,5, v_min = 2', (1.0, 0.5, 2)), ('q = 0,5, v_min = 3', (1.0, 0.5, 3)),
         ('q = 0,2, v_min = 2', (1.0, 0.2, 2)), ('q = 0,2, v_min = 3', (1.0, 0.2, 3))]
vals = [g[k]['t_med'] for _, k in cases]; cols = ['0.5'] + ['#c8553d'] * 5
a.barh(range(len(cases)), vals, color=cols)
for i, (v, (_, k)) in enumerate(zip(vals, cases)):
    a.text(v + 8, i, f"{v:.0f} ticks (adapt {g[k]['adapt_ever']:.2f})", va='center', fontsize=8)
a.set_yticks(range(len(cases))); a.set_yticklabels([c for c, _ in cases]); a.invert_yaxis(); a.set_xlim(0, 820)
a.set_xlabel('mediana del tiempo hasta crear la 5.ª categoría'); a.set_title('(b) Con modelo (λ = 1), la sanción moderada acelera la creación', fontsize=10)
fig.suptitle('C18. Umbral de sanción (M = 512, sin rotación, de 4 × 25 a 5 × 20)', fontsize=11)
fig.tight_layout(); fig.savefig(R / 'c18_figura.png', dpi=140); print('ok')
