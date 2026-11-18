# PREREG C09 — El vocabulario guarda lo que la señal no sabe

**Fecha:** 18/11/2026. **Estado:** preregistrado ANTES de la ejecución primaria (solo smokes con
M=24 y M=12 y horizontes cortos, descartados). Semillas 8110xx–8123xx, nunca usadas. Script
`c09_experiments.py` (M=512); simulador `c09_sim.py`, que reutiliza sin modificar las primitivas
congeladas de `claude_cycle08/c08_sim.py`. SHA en `FREEZE_C09.txt`. Diseño original del usuario
(github.com/GalexY3/memoria-y-relevo).

## Base teórica (comprobada antes, `c09_theory.py`, exhaustiva para N ≤ 32)
Sea C la señal colectiva original (Σ sobre grupos presentes de |s − T|) y D la corregida.
(i) Si hay exactamente k grupos, C = D. (ii) Crear un grupo nuevo sube C al menos T − 2, así que
con menos de k grupos el estado está atrapado para cualquier regla que no acepte empeorar.
(iii) Con más de k grupos el objetivo es alcanzable por movimientos neutros, pero si todos los
grupos son ≤ T y ninguno es unitario no hay mejora estricta (meseta): hay que vaciar un grupo
entero sin gradiente. (iv) D tiene mejora estricta desde todo estado no resuelto.
**Tesis:** la señal original conoce los tamaños, no el número de grupos; la entrada socializada
conserva el vocabulario de k colores, que aporta exactamente esa información, y coloca a la
comunidad en el conjunto donde C = D.

## Diseño común
Instituciones establecidas con la señal D (4000 ticks de ensayo y reversión desde colores
aleatorios; se usan solo las resueltas). Cambio respecto a C08b: allí se establecían con la
señal original y solo el 6% llegaba; aquí todas parten de un 4×25 alcanzado por dinámica local.
Después se aplica el relevo y se sigue con la señal indicada. Entrada `vocab` = color al azar
entre los que usan los titulares; `random` = cualquiera de los 16. Recuperación = alcanzar D=0
en 4000 ticks tras el último relevo, salvo donde se indica.

## Hipótesis
**E1 — Fracción de relevo f ∈ {0,3; 0,6; 0,8; 0,9; 0,93; 0,95; 0,97}, disperso.**
- P1a: con señal original y entrada `vocab`, la recuperación de cada comunidad coincide con que
  sus titulares conserven los k colores: acuerdo ≥ 0,95 en cada f (también en contiguo, f ∈
  {0,6; 0,8; 0,9}).
- P1b: la tasa de recuperación (original, `vocab`, disperso) está a ±0,05 de la curva analítica
  hipergeométrica P(los n titulares cubren los 4 colores): 1,000; 1,000; 0,994; 0,812; 0,541;
  0,249; 0,000.
- P1c: con D y entrada `vocab`, recuperación ≥ 0,95 en todos los f (D recrea roles perdidos).
- P1d: con señal original y entrada `random`, recuperación ≤ 0,20 en todos los f.
**E2 — Ritmo: los mismos 30 relevos, uno cada Δ ticks, Δ ∈ {0 (lote), 1, 10, 100}, entrada random.**
- P2a: señal original, recuperación con Δ=100 ≥ 0,80 y con Δ=0 ≤ 0,20.
- P2b: señal original, recuperación no decreciente en Δ (tolerancia 0,03).
- P2c: D, recuperación ≥ 0,95 para todo Δ.
**E3 — Horizonte largo (64 000 ticks), señal original, lote de 30 con entrada random.**
- P3a: recuperación a 64 000 ≥ 2 × recuperación a 4000 (meseta, no trampa).
- P3b: de las no recuperadas al final, ≥ 0,90 tienen más de k colores (meseta) y no menos.
**E4 — Regla estricta (solo acepta mejoras estrictas), lote de 30.**
- P4a: original + `vocab`: recuperación ≥ 0,90 (4000 ticks).
- P4b: original + `random`: recuperación ≤ 0,05 incluso a 16 000 ticks (sin deriva neutra la
  meseta es trampa).
- P4c: D + `random`: recuperación ≥ 0,95 (4000 ticks).
**E5 — k ∈ {2, 5}, lote de 30.**
- P5: original + `vocab` ≥ 0,90; original + `random` ≤ 0,20; D con ambas entradas ≥ 0,95.
  Si alguna k deja menos de 100 comunidades establecidas, esa k se declara no concluyente.

Cada predicción se declara confirmada o refutada sin cambiar umbrales; los tiempos y las demás
comparaciones son descriptivos. Errores de implementación detectados después se registran como
errata conservando la ejecución original.
