"""Figure C12: self-description (canon) with recognition threshold theta."""
import json
from pathlib import Path
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
H = Path(__file__).resolve().parent
d = json.loads((H / 'C12_RESULTS' / 'c12_PRIMARY.json').read_text(encoding='utf-8'))
A = {(r['mode'], r['theta']): r for r in d['A']}; B = {(r['mode'], r['theta']): r for r in d['B']}
TH = [2, 3, 5, 8, 12, 15, 20]
fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.1))
ax[0].plot(TH, [A[('constatative', t)]['recovered'] for t in TH], 'o-', color='#4f81bd', label='canon que se revisa (constatativo)')
ax[0].axhline(A[('normative', None)]['recovered'], color='#555555', ls='--', label='canon fijo (normativo)')
ax[0].axhline(A[('none', None)]['recovered'], color='#c0504d', ls=':', label='sin canon (señal original)')
ax[0].set_title('a) Homeostasis: recuperación tras un 30% de entradas ajenas', fontsize=9.5)
ax[0].set_ylabel('Comunidades que recuperan 4×25'); ax[0].set_xlabel('Umbral de reconocimiento θ (miembros para entrar en el canon)')
ax[0].legend(fontsize=7.5, frameon=False, loc='center', bbox_to_anchor=(0.52, 0.33))
ax[1].plot(TH, [B[('constatative', t)]['adapt_ever'] for t in TH], 'o-', color='#4f81bd', label='canon que se revisa')
ax[1].axhline(B[('normative', None)]['adapt_ever'], color='#555555', ls='--', label='canon fijo')
ax[1].axhline(B[('none', None)]['adapt_ever'], color='#c0504d', ls=':', label='sin canon')
ax[1].set_title('b) Morfogénesis: el entorno pasa a exigir 5 grupos', fontsize=9.5)
ax[1].set_ylabel('Comunidades que alcanzan 5×20'); ax[1].set_xlabel('Umbral de reconocimiento θ')
ax[1].legend(fontsize=7.5, frameon=False, loc='center right')
for a in ax:
    a.set_ylim(-0.03, 1.05); a.axvspan(7, 9, color='#4f81bd', alpha=0.08); a.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); out = H / 'C12_RESULTS' / 'c12_figura.png'; fig.savefig(out, dpi=160); print(out)
