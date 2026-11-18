# PREREG C12 — La autodescripción como modelo del sistema (Rules como regulador)

**Fecha:** 18/11/2026. **Estado:** preregistrado antes de la ejecución primaria. Piloto exploratorio
`c12_pilot.py` (semillas 8180xx, M=128; `C12_RESULTS/pilot_c12.json`), no reutilizado; smoke M=12
descartado. Semillas nuevas 8190xx. Script `c12_confirm.py` (M=512); simulador `c12_sim.py`, que
reutiliza sin cambios las primitivas congeladas de C08. SHA en `FREEZE_C12.txt`. Idea I-005 del
cuaderno; marco del TFG del usuario: Rules of the Internet como autodescripción performativa y como
tokens de eigenbehaviours (von Foerster), lista viva que el propio sistema amplía.

## Modelo
Además de los tamaños, los agentes evalúan su situación con un **canon**: la lista de categorías que
el sistema reconoce como propias. Coste = Σ_canon |s − T| + Σ_fuera del canon s (normalizado). Tres
regímenes: `none` (señal C original, sin canon); `normative` (canon fijo con los colores fundadores:
autodescripción performativa que no se revisa); `constatative` (cada 50 ticks el canon se reescribe
con los colores que tienen al menos θ miembros: autodescripción que se actualiza observando el
sistema). Barrido θ ∈ {2, 3, 5, 8, 12, 15, 20}.

Experimento A (homeostasis): relevo del 30% con colores aleatorios en instituciones 4×25; 4000 ticks.
Experimento B (morfogénesis): rotación continua (τ = 80, s = 0,9) con k = 4 durante 3000 ticks y
después el entorno exige k = 5 durante 6000 ticks.

## Hipótesis
- **S1** A: con canon normativo, recuperación ≥ 0,95; con la señal C sin canon, ≤ 0,15.
- **S2** A: canon constatativo con θ = 3, recuperación ≤ 0,30 (la descripción legitima categorías
  ajenas); con θ = 8, ≥ 0,95.
- **S3** B: canon normativo, adapt_ever ≤ 0,05 (rigidez) con error de estabilidad ≤ 3.
- **S4** B: canon constatativo con θ = 8, adapt_ever ≥ 0,90 y error de estabilidad ≤ 3; además, su
  error de adaptación es menor que el de `none` y que el de `normative`.
- **S5** B: forma de U invertida en θ para la adaptación: el error de adaptación con θ = 8 es menor
  que con θ = 3 y que con θ = 15.

El resto del barrido es descriptivo. Cada hipótesis se declara confirmada o refutada sin cambiar
umbrales.

## Lectura prevista
Una autodescripción fija da al regulador el modelo que le falta (homeostasis plena) pero congela la
estructura; una autodescripción que se revisa observando el sistema, con un umbral de
reconocimiento intermedio, consigue a la vez homeostasis y morfogénesis (homeorresis por
observación de segundo orden). Un umbral demasiado bajo convierte la desviación en canon; uno
demasiado alto impide reconocer categorías nuevas.
