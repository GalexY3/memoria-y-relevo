"""Figure for C08b: recovery after 30% turnover by entry rule, original collective signal vs corrected D."""
import json, sys
from pathlib import Path
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
H = Path(__file__).resolve().parent
d = json.loads((H / 'C08_RESULTS' / 'c08b_confirm_PRIMARY.json').read_text(encoding='utf-8'))
E = ['social', 'social_global', 'incumbent_set', 'random', 'new']
L = ['copia a un\nvecino', 'copia a un\nveterano\ncualquiera', 'color de los\nveteranos\nal azar', 'cualquier\ncolor', 'color\nnuevo']
fig, axs = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
for ax, cont, title in zip(axs, [False, True], ['Relevo disperso', 'Relevo contiguo']):
    for j, (sig, c, lab) in enumerate([('coll', '#c0504d', 'señal colectiva original'), ('D', '#4f81bd', 'señal colectiva corregida (D)')]):
        rs = {r['entry']: r for r in d['rows'] if r['signal'] == sig and r['contiguous'] == cont}
        x = [i + (j - 0.5) * 0.38 for i in range(len(E))]; y = [rs[e]['recovery'] for e in E]
        lo = [y[i] - rs[e]['wilson95'][0] for i, e in enumerate(E)]; hi = [rs[e]['wilson95'][1] - y[i] for i, e in enumerate(E)]
        ax.bar(x, y, 0.36, color=c, label=f"{lab} (n={rs['social']['presolved']})", yerr=[lo, hi], capsize=2)
    ax.set_xticks(range(len(E))); ax.set_xticklabels(L, fontsize=8); ax.set_title(title, fontsize=10)
    ax.spines[['top', 'right']].set_visible(False)
axs[0].set_ylabel('Comunidades que recuperan 4×25'); axs[0].set_ylim(0, 1.05)
h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, fontsize=8, loc='lower center', ncol=2, frameon=False)
fig.suptitle('Recuperación tras sustituir al 30% según el color con que entran los recién llegados', fontsize=10)
fig.tight_layout(rect=(0, 0.07, 1, 1)); out = Path(sys.argv[1]) if len(sys.argv) > 1 else H / 'C08_RESULTS' / 'c08b_recuperacion.png'
fig.savefig(out, dpi=160); print(out)
