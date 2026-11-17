# PREREG C08 — Relevo (turnover) en «Memoria y relevo»

**Fecha:** 17/11/2026. **Estado:** preregistrado ANTES de cualquier ejecución primaria (solo smoke
M=8, T=300, descartado). Semillas 809xxx no usadas antes. Pilotos exploratorios (8080xx–8083xx) en
`C08_RESULTS/pilot_*.json`, no se reutilizan. Script: `c08_turnover.py` (args por defecto M=256,
T0=T1=4000); simulador `c08_sim.py`. SHA256 congelados en `FREEZE_C08.txt`.

## Diseño
- Rejilla hexagonal toroidal 10×10, X=16 colores, objetivo k=4 grupos de 25. Regla competente:
  ensayo y reversión (act .05, explore .1), memoria individual de un paso.
- Señales: `D` (colectiva corregida), `ind` (hambre individual), `coll` (colectiva original,
  suma sobre colores presentes), `dilemma_sub` (−D/2N + bonus .005 por color preferido entre
  0..3, preferencias sesgadas skew .2; bonus < 1/N = coste marginal de una desviación).
- Calentamiento T0=4000 desde colores aleatorios. Relevo: 30% de agentes, disperso o contiguo
  (BFS en la rejilla). Entrada: `random` (color uniforme), `social` (copia el color de un vecino
  titular; es el «mensaje» de socialización), `new` (todos en un color ausente). T1=4000 más.
  Números aleatorios comunes entre reglas de entrada.
- Medidas: ocupación = fracción de los últimos 1000 ticks con D=0 asentado; recuperación =
  alcanza D=0 tras el relevo; tiempo mediano de recuperación. Para D y dilemma_sub se analizan las
  comunidades resueltas antes del relevo (emparejamiento por rendimiento previo).

## Hipótesis (umbral fijado ahora)
- **H1 (D se autorrepara).** Señal D: recuperación ≥ 0,90 entre pre-resueltas en las 6
  condiciones (2 espacial × 3 entrada). Razón: D no tiene trampas de un agente.
- **H2 (socialización acelera).** Señal D: tiempo mediano de recuperación `social` < `random`, en
  disperso y en contiguo.
- **H3 (dilema subumbral no rompe la institución).** dilemma_sub: recuperación ≥ 0,90 entre
  pre-resueltas con entrada random y social (4 condiciones). Razón: con bonus < 1/N toda mejora de
  D domina la pérdida privada.
- **H4 (la señal individual sigue atrapada).** ind con entrada random y social: ocupación media
  < 0,05 (4 condiciones). Razón: 34/33/33 es equilibrio de Nash y la entrada aleatoria o copiada
  no aporta un cuarto grupo de tamaño suficiente.
- **H5 (el relevo con un grupo nuevo rompe la trampa).** ind, entrada `new`, disperso: ocupación
  media ≥ 0,50. Razón: quitar ~10 de cada grupo de 34/33/33 y añadir 30 en un color nuevo deja
  ~24/23/23/30, dentro de la cuenca del reparto equilibrado. Predicción secundaria: contiguo <
  disperso en esa celda.
- **H6 (la señal colectiva original no sostiene la institución).** coll: ocupación media < 0,15
  en las 6 condiciones.

## Criterio de éxito y lectura
Se informa cada hipótesis como confirmada o refutada sin reformular umbrales. `new` frente a
`random` en D es exploratorio. Cualquier error de implementación detectado después se registra
como errata, con la ejecución original conservada.
