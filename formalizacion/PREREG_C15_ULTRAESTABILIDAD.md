# PREREG C15 — Ultraestabilidad de Ashby en la autodescripción

**Fecha:** 18/11/2026. **Estado:** preregistrado antes de la ejecución primaria.

**Pilotos y confirmación.**
- **Piloto exploratorio:** `c15_pilot.py`, con semillas 8500xx (no reutilizadas); salida en `C15_RESULTS/pilot_c15.json`.
- **Confirmación:** `c15_confirm.py`, con semillas nuevas 8510xx y M = 512.
- **Simulador:** `c15_sim.py`, que es `c13x_sim.py` más el modo `ultrastable`.
- **Predicción analítica:** `c15_markov.py`; valores en `C15_RESULTS/c15_predictions.json`.
- **SHA:** en `FREEZE_C15.txt`.

**Origen.** Idea I-007: la ultraestabilidad de *Design for a Brain* (Ashby, 1952) como regulador de
segundo orden.

## Modelo
El canon normativo (las categorías fundadoras) está vigilado por un bucle de segundo orden. Este bucle
solo observa la variable esencial: el malestar compartido F, es decir, el coste del canon. No conoce el
número de grupos que pide el entorno. Si F pasa L ticks seguidos por encima del límite b = 0,05, el
bucle da un paso aleatorio sobre el canon: con probabilidad 1/2 añade un color no canónico al azar, y si
no, retira un color canónico al azar. Luego reinicia la cuenta.

Hay dos experimentos, ambos con rotación τ = 80 y s = 0,9: crear (B, k 4→5) y disolver (C, k 5→4).
En cada uno hay 3000 ticks antes del cambio y 12 000 después. Las paciencias son L ∈ {100, 200, 400, 800};
la referencia es el mismo sistema sin bucle.

## Predicción analítica (ley de Ashby para este sistema)
F solo puede bajar del límite cuando el canon tiene exactamente k_nuevo categorías. Si la paciencia
supera el tiempo de relajación de la dinámica, el tamaño del canon sigue un paseo aleatorio simétrico
sobre 0…16, con reflexión en los extremos. Por tanto, adaptarse dentro del horizonte equivale a que el
paseo llegue a k_nuevo en ⌊12 000/L⌋ pasos.

| | L = 100 | L = 200 | L = 400 | L = 800 |
|---|---|---|---|---|
| Crear (4→5) | 0,999 | 0,980 | 0,911 | 0,821 |
| Disolver (5→4) | 0,941 | 0,899 | 0,856 | 0,804 |

## Hipótesis
- **U1 (ley en el régimen paciente).** Para L ∈ {400, 800}, en ambos experimentos, |adapt_ever − predicción| ≤ 0,04.
- **U2 (régimen agitado).** Con L = 100, en ambos experimentos, adapt_ever ≤ predicción − 0,15. Una paciencia menor que el tiempo de relajación impide estabilizar.
- **U3 (sin falsas alarmas).** En la fase estable, la fracción de comunidades con algún paso del bucle es ≤ 0,01 para todo L.
- **U4 (un regulador ciego basta).** Con L = 400, adapt_ever ≥ 0,80 en ambos experimentos. Sin bucle, ≤ 0,05.
- **U5 (primer paso).** Con L = 800, en disolver (C), la fracción de comunidades con exactamente un paso es 0,50 ± 0,07. Es la probabilidad del paseo de acertar al primer intento.

Cada hipótesis se declara confirmada o refutada sin cambiar umbrales.
