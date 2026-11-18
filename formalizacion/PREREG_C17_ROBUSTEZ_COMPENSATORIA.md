# PREREG C17 — Robustez compensatoria: cristalización, socialización y sanción

**Fecha:** 18/11/2026. **Estado:** preregistrado antes de la ejecución primaria.
- **Pilotos exploratorios** (semillas 8700xx, 8702xx y 8703xx, no reutilizadas):
  - `c17_pilot.py`, con salida en `C17_RESULTS/pilot_c17.json` y M = 128;
  - `c17_mechanism.py`, que hace las pruebas de eliminación (`mechanism_c17.json`);
  - `c17_frontier.py`, que traza la frontera estabilidad-adaptación (`frontier_c17.json`).
- **Confirmación:** `c17_confirm.py C` y `c17_confirm.py D`, con semillas nuevas 8710xx y M = 512. Los veredictos los calcula `c17_verdicts.py`.
- **Simulador:** `c17_sim.py`, que es `c16_sim.py` con dos añadidos: la cristalización (`cryst`) en la reentrada y la sanción simbólica (`q`, `v_min`). SHA en `FREEZE_C17.txt`.
- **Origen:** idea I-012, diseñada con el usuario el 18/11/2026.
  - La cristalización sigue la entrada 2 del Anexo I del TFG.
  - La regulación compara socialización y sanción como equivalentes funcionales.
  - El orden se mide como estabilidad más coste.
  - La señal principal es C, con D como control.

## Conceptos (Anexo I del TFG)
- **Cristalización identitaria (entrada 2).** Es el grado en que un entorno permite a un participante
  una identidad reconocible, acumulativa y persistente, de modo que otros le reconozcan una trayectoria.
  En el modelo, cuando un puesto rota, el miembro que reentra es reconocido y vuelve como sí mismo, con
  su categoría, con probabilidad c. Con probabilidad 1 − c reentra como nadie: con una categoría al azar,
  salvo que se le socialice.
- **Robustez compensatoria (entrada 27).** Los mecanismos colectivos de regulación deben ser más
  intensos cuanto menor sea la cristalización individual disponible.
- **Regulación colectiva:**
  - **Socialización s:** el recién llegado no reconocido adopta una de las categorías presentes, elegida al azar.
  - **Sanción simbólica q:** cada tick, quien está en una categoría con menos de v_min = 3 miembros pasa, con probabilidad q, a la categoría establecida de un vecino.

## Diseño
- Instituciones 4 × 25 (k = 4 grupos de T = 25) bajo rotación continua: un puesto por institución cada τ = 20 ticks.
- Fase estable de 4000 ticks con k = 4; después el entorno pide k = 5 durante 6000 ticks.
- **Medidas:**
  - estabilidad: la D media en la fase estable (cuanto menor, más orden);
  - adaptación: adapt_ever, la fracción que alcanza D = 0 con k = 5.
- **Señales:** C (sin modelo de cuántos grupos debe haber) y D (con ese modelo, λ = 1 en C16).

| Parte | Configuraciones (c, s, q) |
|---|---|
| C | c ∈ {0; 0,5; 0,8; 0,95} × s ∈ {0; 0,5; 0,8; 0,95; 1}, con q = 0 |
| C | c = 0 con s ∈ {0,97; 0,98; 0,99} |
| C | c = 0 con q ∈ {0,05; 0,1; 0,2; 0,3; 0,5; 1} y s = 0 |
| C | (0,8; 0; 0,05), (0,95; 0; 0,05) y (0,95; 0; 0,2) |
| D | c ∈ {0; 0,5; 0,8; 0,95} con s = 0 y con s = 1; c = 0 con q ∈ {0,2; 1} |

## Argumentos previos
1. **Ley de sustitución.** Bajo C, solo desordena la reentrada que no es reconocida ni socializada,
   porque introduce una categoría al azar. Su tasa por puesto es ρ = (1 − c)(1 − s)/τ. Si la estabilidad
   depende sobre todo de ρ, cristalización y socialización son sustitutos. La socialización mínima para
   un nivel de orden dado cae entonces como s_min = 1 − ρ*/(1 − c): es la entrada 27 en forma de ecuación.
   El residuo esperado es pequeño: el socializado elige categoría al azar entre las presentes y perturba
   los tamaños.
2. **Resonancia.** Bajo C, una categoría nueva solo nace de recién llegados no socializados. Ninguna
   adaptación ocurre sin rotación ni con todos los recién llegados socializados (`mechanism_c17.json`).
   El exceso de ruido impide el orden y su defecto impide la creación, así que la adaptación debe ser
   máxima con un ρ intermedio.
3. **Con modelo no hay compensación necesaria.** D repara la composición directamente, de modo que ni
   la estabilidad ni la creación dependen de los recién llegados (C16: un pionero basta con λ = 1).
4. **Sanción frente a socialización.** La sanción actúa sobre las categorías pequeñas, que es donde está
   el desorden, y deja pasar la variedad que llega. La socialización suprime esa variedad en la entrada.
   Por eso, a igual estabilidad, la sanción debería conservar más capacidad de crear.
5. **Sobrerregulación.** Con cristalización alta, el desorden que queda es escaso, y la misma sanción
   pasa a eliminar sobre todo a los pioneros.
6. **La sanción dura bloquea incluso con modelo.** Con q = 1 y v_min = 3, una categoría nueva solo
   sobrevive si nace con 3 miembros a la vez. Es una coalición rara bajo dinámica síncrona, como en la
   Proposición 6 de C16.

## Hipótesis
Todas se evalúan con `c17_verdicts.py` sobre `c17_PRIMARY_C.json` y `c17_PRIMARY_D.json`.
- **R1 (sin modelo hace falta compensar; con modelo, no).** Bajo C, con c = s = q = 0, la estabilidad es D ≥ 40. Bajo D, con s = q = 0, es D ≤ 8 para todo c.
- **R2 (ley de sustitución).** Se toman seis pares bajo C con el mismo ρ, intercambiando c y s: (0; 0,5)/(0,5; 0), (0; 0,8)/(0,8; 0), (0,5; 0,8)/(0,8; 0,5), (0; 0,95)/(0,95; 0), (0,5; 0,95)/(0,95; 0,5) y (0,8; 0,95)/(0,95; 0,8).
  - En cada par, la diferencia relativa de estabilidad es ≤ 0,30.
  - La media de cada par decrece estrictamente con ρ (0,5 > 0,2 > 0,1 > 0,05 > 0,025 > 0,01).
- **R3 (robustez compensatoria, entrada 27).** Bajo C, sea s_min(c) la menor s de la rejilla {0; 0,5; 0,8; 0,95; 1} con estabilidad D ≤ 20.
  - s_min existe para todo c, no crece con c, y s_min(0,95) ≤ s_min(0) − 0,9.
  - Con sanción ocurre lo mismo: D(c = 0,8; q = 0,05) ≤ 20 < D(c = 0; q = 0,05).
- **R4 (resonancia y coste de la compensación total, bajo C).**
  - adapt_ever ≤ 0,05 con ρ ≥ 0,5, en (0; 0), (0; 0,5) y (0,5; 0).
  - adapt_ever ≥ 0,6 en las cuatro configuraciones con 0,01 ≤ ρ ≤ 0,025: (0,5; 0,95), (0,95; 0,5), (0,8; 0,95) y (0,95; 0,8).
  - adapt_ever ≤ 0,02 con s = 1, para todo c.
  - adapt_ever(0,95; 0,95), con ρ = 0,0025, es menor que el mínimo de esas cuatro.
- **R5 (con modelo, la compensación total no cuesta).** Bajo D con s = 1, adapt_ever ≥ 0,95 para todo c.
- **R6 (equivalentes funcionales con efectos distintos).** Bajo C con c = 0, entre las configuraciones con estabilidad D ≤ 10, la mejor adaptación con sanción supera a la mejor con socialización en ≥ 0,10. Si ninguna configuración cumple la condición, su mejor adaptación cuenta como 0.
- **R7 (sobrerregulación).** Bajo C:
  - adapt_ever(c = 0,95; q = 0,2) ≤ adapt_ever(c = 0; q = 0,2) − 0,4;
  - adapt_ever(c = 0,95; q = 0,05) − adapt_ever(c = 0,95; q = 0,2) ≥ 0,3.
- **R8 (la sanción dura bloquea la creación incluso con modelo).** Bajo D con c = 0, adapt_ever ≤ 0,5 con q = 1 y ≥ 0,95 con q = 0,2.

Cada hipótesis se declara confirmada o refutada sin cambiar umbrales. Cualquier análisis adicional será exploratorio.
