"""C13 figure from the PRIMARY JSONs: (a) fixed threshold, creating vs dissolving a category; (b) social memory;
(c) newcomer voice dose; (d) when the canon names the new structure."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker
H = Path(__file__).resolve().parent; R = H / 'C13_RESULTS'
AC = json.loads((R / 'c13_PRIMARY_AC.json').read_text(encoding='utf-8')); B = json.loads((R / 'c13_PRIMARY_B.json').read_text(encoding='utf-8'))
idx = lambda rows: {r['name']: r for r in rows}
Bx, C = idx(B['B']), idx(AC['C'])
TH = [3, 5, 6, 8, 10, 11, 12, 13, 15]; WS = [25, 50, 100, 200, 400, 800]
cB, cC, cR, cW = '#2a6f97', '#c8553d', '#6a4c93', '#3a7d44'
fig, ax = plt.subplots(2, 2, figsize=(11, 8.2))

a = ax[0, 0]
a.plot(TH, [Bx[f'const_t{t}']['adapt_meanD'] for t in TH], 'o-', color=cB, label='crear (k 4→5)')
a.plot(TH, [C[f'const_t{t}']['adapt_meanD'] for t in TH], 's-', color=cC, label='disolver (k 5→4)')
a.scatter([11], [Bx['reflexive']['adapt_meanD']], marker='*', s=220, color=cB, edgecolor='k', zorder=5, label='alivio (θ = T/2)')
a.scatter([13], [C['reflexive']['adapt_meanD']], marker='*', s=220, color=cC, edgecolor='k', zorder=5)
a.axhline(Bx['comm_W50']['adapt_meanD'], color=cB, ls=':', lw=1.2); a.axhline(C['comm_W50']['adapt_meanD'], color=cC, ls=':', lw=1.2)
a.text(15.2, Bx['comm_W50']['adapt_meanD'], 'repetición\nW = 50', fontsize=7, va='center', color='0.3')
a.set_xlabel('umbral de reconocimiento θ (canon constatativo)'); a.set_ylabel('error medio tras el cambio (D)')
a.set_title('(a) Ningún umbral fijo sirve para crear y disolver', fontsize=10); a.legend(fontsize=8, loc='upper center')

a = ax[0, 1]
a.plot(WS, [Bx[f'comm_W{w}']['adapt_meanD'] for w in WS], 'o-', color=cB, label='crear (k 4→5)')
a.plot(WS, [C[f'comm_W{w}']['adapt_meanD'] for w in WS], 's-', color=cC, label='disolver (k 5→4)')
a2 = a.twinx(); a2.plot(WS, [Bx[f'comm_W{w}']['stab_changes'] for w in WS], 'd--', color='0.5', label='cambios de canon / 1000 ticks (fase estable)')
a2.set_yscale('symlog', linthresh=1); a2.set_ylabel('cambios de canon por 1000 ticks', color='0.4')
a.set_xscale('log'); a.set_xticks(WS); a.set_xticklabels(WS); a.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); a.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
a.set_xlabel('memoria social W (citas recordadas), θ* = 8'); a.set_ylabel('error medio tras el cambio (D)')
a.set_title('(b) El olvido tiene un óptimo interior', fontsize=10)
h1, l1 = a.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels(); a.legend(h1 + h2, l1 + l2, fontsize=7, loc='upper left')

a = ax[1, 0]
dose = B['dose']
for (W, r, col) in [(200, 16, cW), (50, 4, cR)]:
    d = [x for x in dose if x['W'] == W]
    a.plot([x['v'] for x in d], [x['stab_meanD'] for x in d], 'o-', color=col, label=f'repetición, W = {W}')
a.axhline(Bx['reflexive']['stab_meanD'], color='k', ls='--', lw=1, label='alivio (cualquier voz)')
a.set_xlabel('fracción de turnos de palabra de los recién llegados (v)'); a.set_ylabel('error medio en la fase estable (D)')
a.set_title('(c) La voz de los recién llegados captura el canon por repetición', fontsize=10); a.legend(fontsize=8)

a = ax[1, 1]
names = [('const_t8', 'umbral fijo\nθ = 8'), ('reflexive', 'alivio\n(θ = T/2)'), ('comm_W50', 'repetición\nW = 50'),
         ('comm_W200', 'repetición\nW = 200')]
x = range(len(names)); w = 0.38
a.bar([i - w / 2 for i in x], [Bx[n]['t_canon_k_med'] or 0 for n, _ in names], w, color=cB, label='nombrar la categoría nueva (4→5)')
a.bar([i + w / 2 for i in x], [C[n]['t_canon_k_med'] or 0 for n, _ in names], w, color=cC, label='dejar de nombrar la obsoleta (5→4)')
a.set_xticks(list(x)); a.set_xticklabels([l for _, l in names], fontsize=8)
a.set_ylabel('ticks hasta nombrar k categorías (mediana)')
a.set_title('(d) El alivio reconoce tarde y olvida pronto', fontsize=10); a.legend(fontsize=8)
fig.suptitle('C13 · El canon vivo: quién escribe la autodescripción fija su sesgo temporal (n = 512 comunidades por condición)', fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(R / 'c13_figura.png', dpi=150)
print('saved', R / 'c13_figura.png')
