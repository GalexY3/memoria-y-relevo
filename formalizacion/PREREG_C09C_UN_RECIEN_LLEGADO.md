# PREREG C09c — Un solo recién llegado no socializado

**Fecha:** 18/11/2026. **Estado:** preregistrado antes de ejecutar (smoke M=16, T=200 descartado).
Motivo: exploración post hoc de C09 (`c09_explore_tempo.py`, semillas 8130xx, M=256): un único
recién llegado que entra con un color ausente en una comunidad 4×25 deja, con la señal original,
un quinto grupo persistente (tamaño medio ≈ 20) en ≈ 30% de las comunidades a 6400 ticks.
Confirmación con semillas nuevas 8140xx y M=1024 (`c09c_single.py`, sin argumentos).

- **U1** Señal original: fracción de comunidades donde el color ajeno sigue presente a 6400 ticks
  ∈ [0,22; 0,38].
- **U2** Señal original: de las no resueltas, ≥ 0,90 tienen 5 o más colores (meseta, Prop. 4).
- **U3** Señal D: resueltas ≥ 0,99 y color ajeno presente ≤ 0,01.

Lectura prevista si se confirma: con una señal que no cuenta grupos, una sola persona que trae su
propia categoría puede reestructurar la institución, y lo hace por deriva neutra, no por ventaja.
