# PREREG C16 — Fracción de modelo requerida para crear y para disolver

**Fecha:** 18/11/2026. **Estado:** preregistrado antes de la ejecución primaria.
- **Piloto exploratorio:** `c16_pilot.py`, con semillas 8600xx (no reutilizadas); salida en `C16_RESULTS/pilot_c16.json`.
- **Confirmación:** `c16_confirm.py`, con semillas nuevas 8610xx, M = 512 y sin rotación (τ = 0).
- **Simulador:** `c16_sim.py`, que es `c13x_sim.py` con el modo de señal `mix`.
- **Teoría:** `TEOREMA_C16.md`, proposiciones 6 y 7. SHA en `FREEZE_C16.txt`.
- **Origen:** idea I-003, la variedad requerida en forma cuantitativa.

## Diseño
Instituciones establecidas con k_viejo grupos y señal S_λ = (1 − λ)C + λD. El entorno pasa a pedir
k_nuevo grupos durante 6000 ticks. Medidas: adapt_ever (alcanzar D = 0) y mediana del tiempo hasta
conseguirlo.

| Cambio | Tipo | Valores de λ |
|---|---|---|
| 4→5 (T = 20) | crear | 0; 0,3; 0,55; 0,65; 0,7; 0,75; 0,79; 0,8; 0,85; 0,89; 0,9; 1 |
| 5→10 (T = 10) | crear | 0,5; 0,55; 0,6; 0,65; 0,7; 0,8; 1 |
| 5→4 (T = 25) | disolver | 0; 0,05; 0,1; 0,5; 1 |

## Predicciones
Por la Proposición 6, una coalición de j pioneros se conserva si λ ≥ 1 − 2j/T. Los peldaños para
T = 20 son 0,9 (j = 1), 0,8 (pares), 0,7 (tríos) y 0,6; para T = 10, 0,8, 0,6 y 0,4. Las coaliciones
grandes son raras bajo dinámica síncrona, de modo que se espera una escalera.

## Hipótesis
- **Q1 (escalera, T = 20).** En 4→5:
  - adapt_ever ≥ 0,95 para λ ∈ {0,8; 0,85; 0,89; 0,9; 1};
  - ≤ 0,35 para λ ∈ {0,7; 0,75; 0,79};
  - ≤ 0,02 para λ ∈ {0; 0,3; 0,55}.
- **Q2 (el peldaño de pares se nota).** En 4→5, adapt_ever(0,8) − adapt_ever(0,79) ≥ 0,5.
- **Q3 (ley de escala).** Con grupos pequeños (5→10, T = 10), adapt_ever ≥ 0,80 para λ ∈ {0,6; 0,65; 0,7}. Con λ = 0,65 en grupos grandes (4→5) es ≤ 0,05.
- **Q4 (disolver no requiere casi modelo).** En 5→4, adapt_ever ≤ 0,15 con λ = 0 y ≥ 0,95 con λ ∈ {0,05; 0,1}.
- **Q5 (un pionero va más rápido que dos).** En 4→5, la mediana del tiempo de adaptación con λ ∈ {0,9; 1} es menor que con λ ∈ {0,8; 0,85}. Se compara la media de las medianas de cada par.

Cada hipótesis se declara confirmada o refutada sin cambiar umbrales.
