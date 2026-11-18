# PREREG C13c — El filo de la divisoria: olvido en masa cuando una fusión es radical

**Fecha:** 18/11/2026. **Estado:** preregistrado antes de la ejecución primaria.
- **Antecedentes exploratorios** (no reutilizados): `c13x_scale.py`, con semillas 8385xx, y `c13c_pilot.py`, con semillas 8386xx; salida en `C13_RESULTS/pilot_c13c_watershed.json`.
- **Confirmación:** `c13c_confirm.py`, con semillas nuevas 8396xx y M = 512, sobre el simulador `c13x_sim.py` (sin cambios desde C13b). SHA en `FREEZE_C13C.txt`.
- **Origen:** idea I-032.

## Pregunta
Con alivio, el canon admite y retira categorías en la divisoria T/2 (Proposición 1 de C13). Cuando
el entorno exige fusionar categorías (k baja), los grupos antiguos tienen tamaño T_viejo = N/k_viejo.
- Si T_viejo > T_nuevo/2, como en 5→4 (razón 0,8), quedan por encima de la divisoria: el alivio solo
  retira las que se encogen, y olvida a tiempo.
- Si T_viejo = T_nuevo/2, como en 4→2 y 10→5 (razón 0,5), todas quedan en el filo, y la deriva hace
  que se retiren varias a la vez.
- Si T_viejo < T_nuevo/2, como en 5→2 y 10→4 (razón 0,4), todas quedan por debajo: el canon se vacía
  y el sistema deja de reconocerse.

Lectura sociológica: una autodescripción interesada lleva bien las fusiones suaves, pero ante una
fusión radical lo olvida todo a la vez.

## Diseño
- **Canones comparados:** alivio; umbrales fijos revisados en cada tick, uno absoluto (θ = 8) y tres
  relativos al tamaño objetivo nuevo (T/4, T/3 y T/2 + 1).
- **Rotación:** τ = 80, s = 0,9.
- **Fases:** 3000 ticks con k_viejo y 6000 con k_nuevo.
- **Medidas:** error medio de adaptación; adapt_ever; tamaño medio del canon en la fase de
  adaptación; fracción de comunidades con el canon medio por debajo de k_nuevo.

## Hipótesis
- **W1 (fusión suave).** En 5→4, el alivio tiene adapt_ever ≥ 0,95 y un error menor que θ = T/3.
- **W2 (fusión a la mitad).** En 4→2 y en 10→5, el alivio tiene adapt_ever ≤ 0,93 y un error ≥ 1,5 × el de θ = T/3.
- **W3 (cuanto más radical, peor).** Con el mismo k_viejo, el error del alivio crece al bajar la razón:
  - error(5→4) < error(5→2);
  - error(10→5) < error(10→4).
- **W4 (colapso del canon).** En las dos fusiones de razón 0,4, el tamaño medio del canon con alivio en la fase de adaptación es menor que k_nuevo. En 5→4 es ≥ k_nuevo − 0,3.
- **W5 (regla fija robusta).** El umbral relativo θ = T_nuevo/3 tiene adapt_ever ≥ 0,99 en las cinco fusiones.

Cada hipótesis se declara confirmada o refutada sin cambiar umbrales.
