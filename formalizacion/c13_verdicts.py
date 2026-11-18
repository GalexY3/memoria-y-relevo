"""Evaluates the preregistered C13 hypotheses (PREREG_C13_CANON_VIVO.md) from the PRIMARY JSONs.
Usage: python c13_verdicts.py [STATUS]   (STATUS = PRIMARY by default)"""
import json, sys
from pathlib import Path
H = Path(__file__).resolve().parent; R = H / 'C13_RESULTS'
ST = sys.argv[1] if len(sys.argv) > 1 else 'PRIMARY'
AC = json.loads((R / f'c13_{ST}_AC.json').read_text(encoding='utf-8')); B = json.loads((R / f'c13_{ST}_B.json').read_text(encoding='utf-8'))
idx = lambda rows: {r['name']: r for r in rows}
A, A2, C, Bx = idx(AC['A']), idx(AC['A2']), idx(AC['C']), idx(B['B'])
TH = [3, 5, 6, 8, 10, 11, 12, 13, 15]
V = {}
# H1
r, c8 = Bx['reflexive'], Bx['const_t8']
V['H1'] = dict(ok=(r['adapt_ever'] <= 0.85 and r['adapt_ever'] <= c8['adapt_ever'] - 0.15 and r['t_canon_k_med'] is not None
                   and c8['t_canon_k_med'] is not None and r['t_canon_k_med'] >= 2 * c8['t_canon_k_med']),
               detail=dict(adapt_ever_reflexive=r['adapt_ever'], adapt_ever_t8=c8['adapt_ever'], t_canon5_reflexive=r['t_canon_k_med'], t_canon5_t8=c8['t_canon_k_med']))
# H2
r, c8 = C['reflexive'], C['const_t8']
V['H2'] = dict(ok=(r['adapt_ever'] >= 0.95 and r['adapt_meanD'] < c8['adapt_meanD'] and r['t_canon_k_med'] is not None
                   and c8['t_canon_k_med'] is not None and r['t_canon_k_med'] <= 0.5 * c8['t_canon_k_med']),
               detail=dict(adapt_ever_reflexive=r['adapt_ever'], err_reflexive=r['adapt_meanD'], err_t8=c8['adapt_meanD'],
                           t_canon4_reflexive=r['t_canon_k_med'], t_canon4_t8=c8['t_canon_k_med']))
# H3
eB = {th: Bx[f'const_t{th}']['adapt_meanD'] for th in TH}; eC = {th: C[f'const_t{th}']['adapt_meanD'] for th in TH}
aB, aC = min(eB, key=eB.get), min(eC, key=eC.get); mB, mC = eB[aB], eC[aC]
V['H3'] = dict(ok=(aB in (5, 6, 8) and aC in (11, 12, 13, 15) and all((eB[t] - mB > 2) or (eC[t] - mC > 2) for t in TH)),
               detail=dict(argmin_B=aB, argmin_C=aC, err_B=eB, err_C=eC))
# H4
rr, rn = Bx['reflexive'], Bx['reflexive_new']; cu, cn = Bx['comm_W200'], Bx['comm_W200_new']
V['H4'] = dict(ok=(abs(rn['stab_meanD'] - rr['stab_meanD']) <= 0.5 and cn['stab_meanD'] >= 2 * cu['stab_meanD']
                   and cn['stab_novel_size_med'] is not None and cn['stab_novel_size_med'] <= 2),
               detail=dict(stab_reflexive=rr['stab_meanD'], stab_reflexive_new=rn['stab_meanD'], stab_comm=cu['stab_meanD'],
                           stab_comm_new=cn['stab_meanD'], stab_novel_size_med_comm_new=cn['stab_novel_size_med'], stab_novel_n_comm_new=cn['stab_novel_n']))
# H5
WS = [25, 50, 100, 200, 400, 800]; eW = {w: Bx[f'comm_W{w}']['adapt_meanD'] for w in WS}; aW = min(eW, key=eW.get)
V['H5'] = dict(ok=(aW in (50, 100) and Bx['comm_W800']['adapt_ever'] <= 0.10 and Bx['comm_W25']['stab_changes'] >= 5),
               detail=dict(err_by_W=eW, argmin=aW, adapt_ever_W800=Bx['comm_W800']['adapt_ever'], stab_changes_W25=Bx['comm_W25']['stab_changes']))
# H6
s50 = Bx['comm_W50']['adapt_meanD'] + C['comm_W50']['adapt_meanD']; sth = {t: eB[t] + eC[t] for t in TH}
V['H6'] = dict(ok=s50 < min(sth.values()), detail=dict(sum_W50=s50, sum_by_theta=sth, best_theta=min(sth, key=sth.get),
                                                         sum_reflexive=Bx['reflexive']['adapt_meanD'] + C['reflexive']['adapt_meanD']))
# H7
V['H7'] = dict(ok=A2['reflexive']['recovered'] <= A2['const_t8']['recovered'] - 0.05,
               detail=dict(rec_reflexive=A2['reflexive']['recovered'], rec_t8=A2['const_t8']['recovered'], all={k: v['recovered'] for k, v in A2.items()}))
# H8
names = ['reflexive', 'reflexive_new', 'reflexive_old', 'comm_W50', 'comm_W100', 'comm_W200']
V['H8'] = dict(ok=all(A[nm]['recovered'] >= 0.93 for nm in names), detail={nm: A[nm]['recovered'] for nm in names})
# implementation check (not a hypothesis)
chk = all((Bx[nm]['novel_size_min'] is None) or Bx[nm]['novel_size_min'] >= 11 for nm in ['reflexive', 'reflexive_new', 'reflexive_old'])
out = dict(status=ST, verdicts={k: ('CONFIRMADA' if v['ok'] else 'REFUTADA') for k, v in V.items()}, details={k: v['detail'] for k, v in V.items()},
           implementation_check_reflexive_admits_ge_11=chk, n=dict(A=AC['A'][0]['n'], B=B['B'][0]['n'], C=AC['C'][0]['n']))
(R / f'c13_verdicts_{ST}.json').write_text(json.dumps(out, indent=1), encoding='utf-8', newline=chr(10))
print(json.dumps(out['verdicts'], indent=1)); print('check', chk, out['n'])
for k, v in out['details'].items():
    print(k, json.dumps(v)[:400])
