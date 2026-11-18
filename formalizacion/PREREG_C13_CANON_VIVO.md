# PREREG C13 — El canon vivo: la autodescripción escrita por el propio sistema

**Fecha:** 18/11/2026. **Estado:** preregistrado antes de la ejecución primaria.

- **Pilotos exploratorios** con semillas 8280xx–8283xx, no reutilizados:
  - `c13_pilot.py`, `c13_pilot_c.py` y `c13_pilot_a2.py`, con salidas en `C13_RESULTS/pilot_*`;
  - dos diagnósticos en el bloc de notas: dosis de voz y barrido de θ en ambos sentidos.
- **Confirmación** con semillas nuevas 8290xx: `c13_confirm.py` (M = 512, en dos partes, `AC` y `B`).
- **Simulador** `c13_sim.py`, que reutiliza sin cambios las primitivas congeladas de C08.
- **SHA** en `FREEZE_C13.txt`.
- **Origen:** idea I-017 del cuaderno. Sigue a C12, donde el canon se reescribía con un mecanismo postulado, un observador externo con umbral θ.

## Pregunta
En C12 el canon (la lista de categorías que el sistema reconoce como propias) funcionaba como el
modelo del regulador, pero lo reescribía un observador externo. Las Rules del TFG son una lista viva:
alguien propone una entrada y otros la aceptan. Aquí son los propios agentes quienes escriben el canon.
Las preguntas son tres:
- ¿qué umbral de reconocimiento emerge?
- ¿qué sesgo temporal tiene la autodescripción resultante?
- ¿importa quién habla?

## Modelo
El coste del canon y la dinámica de prueba y reversión son los de C12. Hay tres formas de escribir el canon:

- **Constatativo (referencia, C12):** cada 50 ticks, canon = colores con al menos θ miembros. Se
  barre θ ∈ {3, 5, 6, 8, 10, 11, 12, 13, 15}. `const_half` usa θ = ⌊T/2⌋ + 1, recalculado con el T vigente.
- **Uptake por alivio (`reflexive`):** cada tick ocurren dos cosas.
  - Un hablante propone su propio color si no es canónico.
  - Un color canónico al azar se somete a revisión.

  El cambio se acepta si y solo si baja el malestar compartido (el coste del canon).
- **Uptake por repetición (`communicative`):** cada tick un hablante cita su color. El canon son los
  colores citados al menos r veces en las últimas W citas: memoria social con olvido. Se usa
  r = 0,08·W, es decir θ* = rN/W = 8, con W ∈ {25, 50, 100, 200, 400, 800}.
- **Voz:** `uniform` (cualquiera habla). `new` (con probabilidad 0,5, el hablante es alguien que entró hace menos de 160 ticks). `old` (con probabilidad 0,5, es alguien con al menos la antigüedad mediana).

**Proposición (alivio ⇒ mitad).** Con el coste del canon, admitir un color c con s miembros cambia su
término de s a |s − T|; quitarlo hace lo contrario. Por tanto el uptake por alivio admite un color si y
solo si s > T/2 y lo retira si y solo si s < T/2. Se siguen tres consecuencias:
- el umbral efectivo es la mitad del tamaño objetivo, no tiene parámetros libres y es invariante de escala;
- quién proponga no cambia qué se acepta;
- la autodescripción solo reconoce lo que ya ha alcanzado la mitad del éxito.

## Experimentos
- **A (homeostasis):** instituciones 4×25 sometidas a un choque que reemplaza al 30% de los agentes por colores aleatorios; 4000 ticks.
- **A2 (la categoría herida):** el mismo diseño con un choque del 45%.
- **B (diferenciación):** rotación continua (τ = 80, s = 0,9); k = 4 durante 3000 ticks y después k = 5 durante 6000 ticks.
- **C (desdiferenciación):** instituciones 5×20 con la misma rotación; k = 5 durante 3000 ticks y después k = 4 durante 6000 ticks. Una categoría debe desaparecer.

Medidas:
- error medio D en cada fase;
- adapt_ever: alcanzar D = 0 en la segunda fase;
- t_canon_k: primer tick en que el canon nombra k categorías;
- tamaño de las categorías nuevas en el momento de su primera admisión;
- cambios de canon por cada 1000 ticks.

## Hipótesis
- **H1 (desfase semántico del alivio, B).**
  - reflexive tiene adapt_ever ≤ 0,85 y, además, ≤ adapt_ever(const_t8) − 0,15;
  - la mediana de t_canon_k de reflexive es ≥ 2 × la de const_t8.
- **H2 (olvido temprano del alivio, C).**
  - reflexive tiene adapt_ever ≥ 0,95;
  - su error de adaptación es menor que el de const_t8;
  - la mediana de t_canon_k de reflexive es ≤ 0,5 × la de const_t8.
- **H3 (ningún umbral único sirve en ambos sentidos; barrido constatativo).**
  - el θ que minimiza el error de adaptación en B está en {5, 6, 8};
  - el que lo minimiza en C está en {11, 12, 13, 15};
  - para todo θ del barrido, el error supera en más de 2 al mínimo de B o al mínimo de C.
- **H4 (voz: el alivio es inmune y la repetición se deja capturar; fase estable de B).**
  - |error(reflexive_new) − error(reflexive)| ≤ 0,5;
  - error(comm_W200_new) ≥ 2 × error(comm_W200);
  - la mediana del tamaño de las categorías admitidas en esa fase con comm_W200_new es ≤ 2 miembros.
- **H5 (óptimo interior de la memoria social, B, θ* = 8).**
  - el error de adaptación es mínimo en W ∈ {50, 100};
  - W = 800 tiene adapt_ever ≤ 0,10;
  - W = 25 tiene ≥ 5 cambios de canon por 1000 ticks en la fase estable.
- **H6 (la memoria corta supera a todo umbral fijo).**
  - error_B + error_C de comm_W50 < mín sobre θ del barrido de [error_B(θ) + error_C(θ)].
- **H7 (el alivio da por perdida la categoría herida, A2).**
  - recuperación(reflexive) ≤ recuperación(const_t8) − 0,05.
- **H8 (homeostasis preservada, A).**
  - recuperación ≥ 0,93 para reflexive (las tres voces) y para comm W50, W100 y W200 con voz uniforme.

Cada hipótesis se declara confirmada o refutada sin cambiar umbrales.

Hay además una **verificación de implementación** que no cuenta como hipótesis: con reflexive, toda
admisión nueva en B ocurre con s ≥ 11.

El resto (barrido de W en C, dosis de voz, A y A2 por condición, tamaños de admisión) es descriptivo.

## Lectura prevista
Quién escribe la autodescripción, y cómo, fija su sesgo temporal:
- **Alivio:** reconoce tarde lo nuevo y olvida pronto lo viejo. Es una semántica que va por detrás de la estructura al crear y por delante al disolver; no la capturan los recién llegados ruidosos, pero abandona las categorías heridas.
- **Repetición con memoria:** reconoce con un umbral ajustable. Una memoria corta (olvido) da al sistema un ruido útil que acelera la creación y la disolución, al precio de quedar expuesto a la voz de los recién llegados.
- **Umbral fijo:** obliga a elegir entre reconocer pronto lo nuevo y olvidar pronto lo obsoleto.
