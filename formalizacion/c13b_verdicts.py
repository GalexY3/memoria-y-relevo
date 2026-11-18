"""Evaluates the preregistered C13b hypotheses (PREREG_C13B_ORDEN_DESDE_EL_RUIDO.md) from the PRIMARY JSONs."""
import json
from pathlib import Path
R = Path(__file__).resolve().parent / 'C13_RESULTS'
ld = lambda p: {r['name']: r for r in json.loads((R / f'c13b_PRIMARY_{p}.json').read_text(encoding='utf-8'))['rows']}
B, C, A = ld('B'), ld('C'), ld('A')
S = {k: B[k]['adapt_meanD'] + C[k]['adapt_meanD'] for k in B}
TH = [f'const_t{t}_U1' for t in [6, 7, 8, 9, 10, 13]]
best_exact = min(TH, key=lambda k: S[k])
V = dict(
    N1=S['sampled_n50_U1'] < S[best_exact],
    N2=(S['sampled_n50_U1'] < S['sampled_n12_U1'] and S['sampled_n50_U1'] < S['sampled_n100_U1'] and S['sampled_n12_U1'] > 2 * S['sampled_n50_U1']),
    N3=S['sampled_n50_U1'] < S['comm_W50'],
    N4=(A['sampled_n50_U1']['recovered'] >= 0.98 and B['sampled_n50_U1']['stab_meanD'] <= B['const_t8_U1']['stab_meanD'] + 0.2),
    N5=S['sampled_n50_U20'] < S[best_exact])
out = dict(verdicts={k: 'CONFIRMADA' if v else 'REFUTADA' for k, v in V.items()}, sums=S, best_exact=best_exact,
           A_recovered={k: A[k]['recovered'] for k in A}, B_stab={k: B[k]['stab_meanD'] for k in B},
           C_stab={k: C[k]['stab_meanD'] for k in C}, B_adapt={k: B[k]['adapt_meanD'] for k in B}, C_adapt={k: C[k]['adapt_meanD'] for k in C})
(R / 'c13b_verdicts_PRIMARY.json').write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print(json.dumps(out['verdicts'], indent=1)); print('best exact', best_exact)
for k in S:
    print(k.ljust(18), 'B %.2f  C %.2f  sum %.2f | stabB %.2f stabC %.2f | A %.3f' % (B[k]['adapt_meanD'], C[k]['adapt_meanD'], S[k], B[k]['stab_meanD'], C[k]['stab_meanD'], A[k]['recovered']))
