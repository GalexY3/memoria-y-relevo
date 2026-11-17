# PREREG C08b — ¿Por qué la entrada socializada preserva la institución? (confirmación)

**Fecha:** 17/11/2026. **Estado:** preregistrado ANTES de la ejecución primaria (solo smoke
M=16/8, T=300/200, descartado). Motivo: resultado exploratorio de C08 (n=12): con la señal
colectiva original (`coll`), 12/12 comunidades resueltas se recuperan con entrada socializada y
0/12 con entrada aleatoria o de color nuevo. Semillas 8100xx–8106xx, nunca usadas. Script
`c08b_confirm.py` (args por defecto: coll M=4096, D M=1024, T0=8000, T1=4000, sucesión 2000 por
ronda); simulador `c08_sim.py` sin cambios desde FREEZE_C08. SHA en `FREEZE_C08B.txt`.

El README del diseño pide separar «la pérdida de memoria» del «desequilibrio que introduzca el
color inicial de los recién llegados». Para ello se comparan cinco reglas de entrada:
`social` (copia a un vecino titular: transmisión local), `social_global` (copia a un titular
cualquiera: conserva proporciones sin localidad), `incumbent_set` (uniforme entre los colores de
los titulares: conserva solo el conjunto de colores), `random` (16 colores), `new` (un color
ausente). Relevo del 30%, disperso y contiguo. Análisis sobre comunidades resueltas antes del
relevo (emparejadas por rendimiento previo). Recuperación = alcanzar D=0 en T1; se dan IC de Wilson.

Sucesión (fase «Sucesión» del diseño): relevos de 30, 30, 30 y 10 fundadores con entrada
socializada y 2000 ticks entre rondas, hasta que no queda ningún fundador.

## Hipótesis
- **B1** coll, `social`: recuperación ≥ 0,80 en disperso y en contiguo.
- **B2** coll, `random` y `new`: recuperación ≤ 0,20 en disperso y en contiguo (4 celdas).
- **B3** coll, `social_global`: recuperación ≥ 0,80 (disperso y contiguo). La localidad no es
  necesaria; basta conservar las proporciones.
- **B4** coll, `incumbent_set`: recuperación ≥ 0,80 (disperso y contiguo). Predicción de
  mecanismo: lo decisivo es no introducir colores nuevos.
- **B5** Sucesión: con coll, fracción de comunidades pre-resueltas en D=0 al final de la ronda 4
  ≥ 0,70; con D ≥ 0,95.
- Referencia: con D todas las reglas de entrada ≥ 0,95.

Cada hipótesis se declara confirmada o refutada sin cambiar umbrales. Las comparaciones no
listadas (tiempos, choque) son descriptivas.
