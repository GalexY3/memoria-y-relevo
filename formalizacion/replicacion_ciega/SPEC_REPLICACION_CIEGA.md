# Specification for a blind re-implementation ("Memoria y relevo" model)

You are re-implementing an agent-based model ONLY from this text. Do not open any other file in this repository
(the original code lives elsewhere and must not be read). Write all your code and outputs inside this folder
(`replicacion_ciega/`). Use Python 3 with NumPy. Report numbers honestly, including failures.

## 1. Population and space
- N = 100 agents on a 10×10 hexagonal grid with wrap-around (torus), 6 neighbours each. Cell index = r*10 + c.
  "Odd-r" offset layout: for even rows r the neighbour offsets (dr, dc) are (0,−1), (0,+1), (−1,−1), (−1,0), (+1,−1), (+1,0);
  for odd rows: (0,−1), (0,+1), (−1,0), (−1,+1), (+1,0), (+1,+1). Rows and columns wrap modulo 10.
- Each agent holds a colour in {0, …, X−1}, X = 16. s_c = number of agents with colour c.
- Target: k groups of equal size T = N/k (k = 4 → T = 25; k = 5 → T = 20).

## 2. Signals (all are COSTS, identical for every agent of a community; lower is better)
- D (structural): L1 distance from the sorted colour counts to the balanced k-partition:
  sort counts descending s(1) ≥ s(2) ≥ …; D = Σ_{i≤k} |s(i) − T| + Σ_{i>k} s(i). D = 0 iff exactly k colours of T members.
- C (the original design): C = Σ over colours PRESENT (s_c > 0) of |s_c − T|.
- Canon cost: a community also has a canon K (a set of colours it recognises). F = Σ_{c∈K} |s_c − T| + Σ_{c∉K} s_c.
  (Any positive rescaling of a signal is irrelevant.)

## 3. Dynamics: synchronous trial-and-revert with one-step memory
Simulate M independent communities in parallel. Parameters act = 0.05, explore = 0.10. Each tick t:
1. **Revert step.** Every agent that made a trial at the previous tick reverts to its previous colour if the
   community signal now is STRICTLY greater than the signal value recorded just before that trial (tolerance 1e−12).
   Because the signal is shared, either all of the previous tick's trial-makers revert or none do.
2. (Events of the experiment happen here: replacements, newcomers, canon updates; see §4–§5.)
3. Recompute the signal. Record measures (e.g. D, and whether D == 0).
4. **Trial step.** An agent is "hungry" if the current signal > 1e−12. Each hungry agent independently becomes
   active with probability act. An active agent picks a candidate colour: with probability explore a uniformly
   random colour in {0..15}; otherwise the colour of one of its 6 neighbours chosen uniformly. If the candidate
   differs from its colour it adopts it (a "trial"); record (previous colour, signal value before the trials).
   All trials of a tick happen simultaneously.
After the last tick, apply one final revert step (settle pending trials).

## 4. Experiments to run (use M = 256 communities unless stated; seeds of your choice; report n actually used)

**R1 · Learning.** Start from uniformly random colours, k = 4, 8000 ticks. Report the fraction of communities that
reach D = 0 at some tick (a) with signal D and (b) with signal C.

**R2 · Vocabulary.** Take communities that reached D = 0 under R1(a) and that END in a D = 0 state (4 colours × 25):
these are "institutions". Replace a random 90% of the agents (90 positions chosen uniformly without replacement):
each newcomer takes a colour drawn uniformly from the set of colours present among the 10 remaining incumbents
("socialised entry"). Then run 4000 ticks with signal C, k = 4. Report the fraction that reaches D = 0 after the
replacement. Separately, COMPUTE ANALYTICALLY (before looking at the simulation) the probability that the 10
remaining incumbents still contain all 4 colours of the institution, and report both numbers.

**R3 · Canon with recognition threshold θ (morphogenesis).** Start from institutions (4×25). Canon K starts as the
4 founding colours. Continuous turnover: every τ = 80 ticks (at ticks t ≡ 0 mod 80) one uniformly random agent is
replaced; with probability 0.9 the newcomer takes a colour drawn uniformly from the set of colours present among
the other 99 agents, otherwise a uniformly random colour in {0..15}. Signal: the canon cost F. "Constatative" canon:
every 50 ticks (t ≡ 0 mod 50), K is rewritten as {c : s_c ≥ θ}. Phase 1: k = 4 (T = 25) for 3000 ticks. Phase 2:
the environment changes to k = 5 (T = 20) for 6000 ticks (the canon, colours and tick counter for the 80/50
schedules continue; restarting the tick counter at the phase change is also acceptable — say which). Report, for
θ ∈ {3, 8, 15}: the fraction of communities that reach D = 0 (with k = 5) at some tick of phase 2, and the mean of D
over phase 2.

**R4 · Canon written by "relief".** Same as R3 but the canon is revised by the agents: every tick, (i) one
uniformly random agent proposes its own colour if that colour is not in K; the proposal is accepted iff adding it
STRICTLY lowers F; (ii) one colour chosen uniformly among the colours in K is put under review; it is removed iff
removing it STRICTLY lowers F. Run both:
- R4a differentiation: as R3 (k = 4 → 5);
- R4b de-differentiation: institutions 5 × 20 (obtain them as in R1 with k = 5 and signal D), canon = the 5 founding
  colours, turnover as in R3, phase 1 k = 5 for 3000 ticks, phase 2 k = 4 (T = 25) for 6000 ticks.
For both, also run the constatative canon with θ = 8. Report: fraction reaching D = 0 in phase 2, mean D in phase 2,
and the median over communities of the first tick in phase 2 at which |K| equals the new k.
Also report, under relief in R4a, the minimum size s_c of any colour at the moment it was newly admitted to K
during phase 2.

## 5. Deliverables
- `replica.py` (your implementation), `RESULTS.json` (all numbers above, with n per cell), and
  `REPORT.md` (one page: what you implemented, any ambiguity in this spec and how you resolved it, results table).
- Do not tune anything to match expected values; there are none given here on purpose.
