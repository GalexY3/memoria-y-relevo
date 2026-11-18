# PREREG C10b — ¿Gobierna la tasa de desviación? (confirmación de un hallazgo post hoc)

**Fecha:** 18/11/2026. **Estado:** preregistrado antes de la ejecución primaria (smoke M=12,
escala 0,3, descartado). Motivo: en C10 (`C10_RESULTS/c10_PRIMARY.json`), bajo la señal C, las
curvas de estabilidad y adaptación de τ = 20 y τ = 80 parecían coincidir al ordenarlas por la tasa
de entradas no socializadas r = (1 − s)/τ, con óptimo de adaptación en r ≈ 0,0006–0,001; bajo D no
coincidían. Es una observación post hoc; aquí se pone a prueba con τ nuevos. Semillas 8170xx.
Script `c10b_collapse.py` (M=512); simulador `c10_sim.py` sin cambios (SHA en `FREEZE_C10B.txt`).

Diseño: como C10 (estabilidad k=4, 4000 ticks; adaptación k=5, 6000 ticks), con τ ∈ {10, 40, 160}
y r ∈ {0,0005; 0,001; 0,002; 0,004}, s = 1 − rτ.

## Hipótesis
- **R1 (colapso bajo C).** Para cada r, el rango entre los tres τ del error medio de adaptación es
  ≤ 4, y el del error medio de estabilidad también ≤ 4.
- **R2 (óptimo de desviación bajo C).** Para cada τ, la r de la rejilla que minimiza el error de
  adaptación es 0,0005 o 0,001.
- **R3 (bajo D gobierna el ritmo total, no la desviación).** Para cada r, el error de estabilidad
  bajo D es mayor con τ = 10 que con τ = 40, y mayor con τ = 40 que con τ = 160.

Lectura prevista si se confirma: el regulador sin modelo de la estructura es sensible a la cualidad
de la perturbación (cuánta variedad ajena entra por unidad de tiempo); el regulador con modelo, a
su cantidad (cuántos miembros rotan). En términos durkheimianos, bajo C existe una tasa «normal»
de desviación: con ninguna, rigidez; con demasiada, anomia.
