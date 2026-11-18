# PREREG C13d — ¿La semántica sigue a la estructura o se le adelanta?

**Fecha:** 18/11/2026. **Estado:** preregistrado antes de la ejecución primaria.
- **Exploratorio previo** (no reutilizado): `c13d_explore.py`, con semillas 8387xx; salida en `C13_RESULTS/explore_c13d_semantic_lag.json`.
- **Confirmación:** `c13d_confirm.py`, con semillas nuevas 8397xx y M = 512.
- **Simulador:** `c13d_sim.py`, que es `c13x_sim.py` con una sola variable añadida de seguimiento (`struct_t`). SHA en `FREEZE_C13D.txt`.
- **Origen:** idea I-020 (Luhmann: semántica y estructura; adquisiciones preadaptativas).

## Medida
En el experimento B (k 4→5, rotación τ = 80, s = 0,9) se toma, en cada comunidad, el primer color
nuevo que entra en el canon tras el cambio. Se definen:
- **Desfase** = tick de admisión − primer tick en que ese color alcanza 7 miembros (≈ T/3, «estructura naciente»).
  Positivo: la semántica sigue a la estructura. Negativo: se le adelanta.
- **Falso arranque:** el color admitido nunca llegó a 7 miembros.

## Hipótesis
- **D1 (desfase del alivio).** Con alivio, la mediana del desfase es > 100 ticks y la fracción con la semántica primero es ≤ 0,05.
- **D2 (preadaptación del canon ruidoso).** Con la muestra de 50 cada tick, la mediana del desfase es < 0, la fracción con la semántica primero es ≥ 0,90 y la de falsos arranques es ≥ 0,30.
- **D3 (la memoria larga retrasa).** Con repetición W = 200, la mediana del desfase es > 100. Con W = 50 es < 0.
- **D4 (adelantarse paga).** El canon muestreado tiene menor error de adaptación que el alivio y que la repetición W = 200, aunque tenga más falsos arranques que ambos.

Los umbrales fijos (θ = 8 y θ = 5) se informan como referencia descriptiva: su desfase está fijado en
parte por construcción. Cada hipótesis se declara confirmada o refutada sin cambiar umbrales.
