# PREREG C10 — La paradoja del gatekeeping: morfostasis frente a morfogénesis

**Fecha:** 18/11/2026. **Estado:** preregistrado antes de la ejecución primaria. Piloto
exploratorio previo `c10_pilot.py` (semillas 8150xx, M=128, `C10_RESULTS/pilot_c10.json`), que no
se reutiliza; smoke con M=8 descartado. Semillas nuevas 8160xx. Script `c10_confirm.py` (M=512,
escala 1); simulador `c10_sim.py`, que reutiliza sin cambios las primitivas congeladas de C08.
SHA en `FREEZE_C10.txt`. Diseño original de «Memoria y relevo»: el usuario.

## Pregunta (marco: `cuaderno/MARCO_SISTEMICO.md`, Tesis 3)
Si el regulador colectivo no contiene un modelo de la estructura (señal C), ¿la socialización de los
recién llegados asegura la homeostasis pero bloquea la morfogénesis? ¿Desaparece el dilema cuando el
regulador sí modela la estructura (señal D; teorema de Conant y Ashby)?

## Diseño
Instituciones 4×25 establecidas con D (4000 ticks; solo las resueltas). Rotación continua: cada τ
ticks se sustituye a un agente al azar; el recién llegado está socializado con probabilidad s (toma
al azar uno de los colores de los titulares) o trae cualquiera de los 16 colores. Fase de
estabilidad: k = 4 durante 4000 ticks. Fase de adaptación: el entorno pasa a exigir k = 5 (T = 20)
durante 6000 ticks; la señal se actualiza en sus propios términos (C con T = 20, D con k = 5).
Rejilla s ∈ {0; 0,5; 0,75; 0,9; 0,95; 0,98; 1}, τ ∈ {20, 80}, señal ∈ {C, D}. Medidas: error
estructural medio D_k en cada fase (menor es mejor), fracción de comunidades que alcanzan alguna
vez el reparto 5×20 en la fase de adaptación (adapt_ever) y número medio de colores.

## Hipótesis
- **Q1 (estabilidad crece con la socialización bajo C).** Con C, el error medio de la fase de
  estabilidad es decreciente en s a lo largo de la rejilla (cada paso baja o sube menos de 0,5), en
  ambos τ.
- **Q2 (sin morfogénesis con socialización total; Proposición 3).** Con C y s = 1: adapt_ever ≤
  0,01 y número medio de colores en la fase de adaptación = 4,00 ± 0,01, en ambos τ.
- **Q3 (óptimo interior de la adaptación bajo C).** Con C, el s que minimiza el error medio de la
  fase de adaptación es interior (0 < s* < 1) y su error es menor que el de s = 0 y el de s = 1, en
  ambos τ. Junto con Q1: bajo C, el s que maximiza la estabilidad (1) no maximiza la adaptación.
- **Q4 (sin dilema bajo D).** Con D, s = 1 está a ≤ 0,3 del mejor error medio en ambas fases y
  ambos τ, y adapt_ever ≥ 0,95 para todo s ≥ 0,5.
- **Q5 (Conant–Ashby).** Para todo s y τ, el error medio de la fase de adaptación es menor con D
  que con C.

Descriptivo, sin hipótesis: entorno que alterna k = 4, 5, 4, 5 (2500 ticks cada uno, τ = 80).
Cada hipótesis se declara confirmada o refutada sin cambiar umbrales.

## Lectura prevista
Si se confirma: el beneficio de la rotación con reclutas no socializados (March 1991) existe solo
cuando el regulador carece de modelo de la estructura; con un regulador que la modela, la
socialización nunca perjudica. La desviación importada es la fuente de variedad que permite la
morfogénesis a un sistema que no puede crear categorías por sí mismo, y su dosis óptima es
intermedia. Conecta con el TFG: gatekeeping intenso y diferenciación decidida por la
administración (creación de /pol/).
