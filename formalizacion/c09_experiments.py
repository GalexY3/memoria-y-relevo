"""C09 preregistered experiments (PREREG_C09.md; seeds 8110xx-8119xx). Usage: python c09_experiments.py [M] [quick]
E1 turnover fraction x entry x signal (+ analytic vocabulary-survival curve); E2 tempo of the same 30
replacements; E3 long horizon; E4 strict acceptance rule; E5 k in {2,5}."""
import json, sys, time, hashlib
from math import comb
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parent / 'claude_cycle08'))
from c08_sim import trial_and_revert, counts, dist_D, NB, N
from c09_sim import run, dispersed

M = int(sys.argv[1]) if len(sys.argv) > 1 else 512
QUICK = len(sys.argv) > 2
T1 = 300 if QUICK else 4000; TLONG = 600 if QUICK else 64000; TSTRICT = 600 if QUICK else 16000; TWARM = 600 if QUICK else 4000
X = 16; OUT = {}; t0 = time.time()

def p_complete(n, k):
    T = N // k; return sum((-1) ** j * comb(k, j) * comb(N - j * T, n) for j in range(k + 1)) / comb(N, n)

def contiguous(M, m, rng):
    out = np.zeros((M, N), bool)
    for i in range(M):
        start = int(rng.integers(0, N)); order = [start]; seen = {start}; j = 0
        while len(order) < m:
            for v in NB[order[j]]:
                if v not in seen and len(order) < m: seen.add(v); order.append(v)
            j += 1
        out[i, order] = True
    return out

def establish(k, seed):
    col, _, _, _ = trial_and_revert(M, 'D', 0.05, 0.1, T=TWARM, k=k, X=X, seed=seed)
    S = dist_D(counts(col, X), k) == 0
    return col[S], int(S.sum())

def rate(first, horizon=None):
    ok = first >= 0 if horizon is None else (first >= 0) & (first <= horizon)
    return float(ok.mean())

def log(name, row):
    OUT.setdefault(name, []).append(row); print(name, {a: b for a, b in row.items() if not isinstance(b, list)}, flush=True)

# ---------- k = 4 establishment ----------
col4, n4 = establish(4, 811000); OUT['established_k4'] = n4; M4 = col4.shape[0]

# ---------- E1: turnover fraction ----------
for fi, f in enumerate([0.3, 0.6, 0.8, 0.9, 0.93, 0.95, 0.97]):
    m = round(f * N); rep = dispersed(M4, m, np.random.default_rng(811100 + fi))
    complete = np.array([len(np.unique(col4[i, ~rep[i]])) == 4 for i in range(M4)])
    for sig in ['coll', 'D']:
        for entry in ['vocab', 'random']:
            _, first, _ = run(col4, sig, T1, seed=811200 + fi, events={0: rep}, entry=entry, entry_seed=811300 + fi)
            rec = first >= 0
            log('E1', dict(f=f, layout='dispersed', signal=sig, entry=entry, n=M4, recovery=float(rec.mean()),
                           analytic_p_complete=p_complete(N - m, 4), empirical_complete=float(complete.mean()),
                           agreement_rec_vs_complete=float((rec == complete).mean())))
for fi, f in enumerate([0.6, 0.8, 0.9]):
    m = round(f * N); rep = contiguous(M4, m, np.random.default_rng(811400 + fi))
    complete = np.array([len(np.unique(col4[i, ~rep[i]])) == 4 for i in range(M4)])
    _, first, _ = run(col4, 'coll', T1, seed=811500 + fi, events={0: rep}, entry='vocab', entry_seed=811600 + fi)
    rec = first >= 0
    log('E1', dict(f=f, layout='contiguous', signal='coll', entry='vocab', n=M4, recovery=float(rec.mean()),
                   empirical_complete=float(complete.mean()), agreement_rec_vs_complete=float((rec == complete).mean())))

# ---------- E2: tempo of the same 30 replacements ----------
rep30 = dispersed(M4, 30, np.random.default_rng(811700))
for di, delta in enumerate([0, 1, 10, 100]):
    if delta == 0: events = {0: rep30}
    else:
        events = {}
        for i in range(M4):
            for e, a in enumerate(np.nonzero(rep30[i])[0]):
                events.setdefault(e * delta, np.zeros((M4, N), bool))[i, a] = True
    last = max(events)
    for sig in ['coll', 'D']:
        _, first, _ = run(col4, sig, last + T1 + 1, seed=811800 + di, events=events, entry='random', entry_seed=811900)
        log('E2', dict(delta=delta, signal=sig, entry='random', n=M4, recovery=rate(first, T1),
                       median_after_last=(float(np.median(first[first >= 0])) if (first >= 0).any() else None)))

# ---------- E3: long horizon ----------
colF, first, _ = run(col4, 'coll', TLONG, seed=812000, events={0: rep30}, entry='random', entry_seed=812001)
cntF = counts(colF, X); mF = (cntF > 0).sum(1); unrec = first < 0
log('E3', dict(signal='coll', entry='random', n=M4, T=TLONG, rec_4000=rate(first, 4000), rec_16000=rate(first, 16000),
               rec_64000=rate(first, 64000), median_recovered=(float(np.median(first[first >= 0])) if (first >= 0).any() else None),
               unrecovered=int(unrec.sum()), unrec_share_m_gt_k=(float((mF[unrec] > 4).mean()) if unrec.any() else None),
               unrec_share_m_lt_k=(float((mF[unrec] < 4).mean()) if unrec.any() else None),
               first_hit=[int(v) for v in first]))

# ---------- E4: strict acceptance rule ----------
for sig, entry, T in [('coll', 'vocab', T1), ('coll', 'random', TSTRICT), ('D', 'random', T1)]:
    _, first, _ = run(col4, sig, T, seed=812100, events={0: rep30}, entry=entry, entry_seed=812101, rule='strict')
    log('E4', dict(rule='strict', signal=sig, entry=entry, n=M4, T=T, recovery=rate(first)))

# ---------- E5: k in {2, 5} ----------
for k, s0 in [(2, 812200), (5, 812300)]:
    colk, nk = establish(k, s0); Mk = colk.shape[0]; repk = dispersed(Mk, 30, np.random.default_rng(s0 + 1))
    for sig in ['coll', 'D']:
        for entry in ['vocab', 'random']:
            _, first, _ = run(colk, sig, T1, k=k, seed=s0 + 2, events={0: repk}, entry=entry, entry_seed=s0 + 3)
            log('E5', dict(k=k, signal=sig, entry=entry, n=Mk, established=nk, recovery=rate(first)))

OUT['meta'] = dict(status='SMOKE' if QUICK else ('PRIMARY' if M == 512 else 'OTHER'), M=M, seconds=time.time() - t0,
                   sha256={f: hashlib.sha256((H / f).read_bytes()).hexdigest() for f in ['c09_sim.py', 'c09_experiments.py']})
name = 'c09_smoke.json' if QUICK else f'c09_PRIMARY_M{M}.json'
(H / 'C09_RESULTS').mkdir(exist_ok=True)
(H / 'C09_RESULTS' / name).write_text(json.dumps(OUT, indent=1), encoding='utf-8', newline=chr(10)); print('wrote', name, round(time.time() - t0), 's')
