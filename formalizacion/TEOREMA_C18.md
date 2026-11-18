# C18 · Umbral de sanción: la sanción convierte toda creación en un problema de coalición (idea I-035)

**Modelo.** Es el de C17 (`claude_cycle17/c17_sim.py`, congelado), con N = 100 agentes en un toro
hexagonal 10 × 10 y la señal S_λ = (1 − λ)C + λD de C16. Cada tick sigue este orden:
1. **Reversión:** se deshacen todos los movimientos de prueba del tick anterior si la señal empeoró.
2. **Rotación**, si la hay.
3. **Sanción:** con los recuentos actuales, una categoría está **establecida** si tiene al menos v_min
   miembros. Cada agente de una categoría no establecida mira a un vecino al azar (uno de seis). Si ese
   vecino está en una categoría establecida, adopta su categoría con probabilidad q. El movimiento es
   forzado: no se revierte.
4. **Prueba:** cada agente actúa con probabilidad `act`. Explora un color al azar con probabilidad
   `explore`, o imita el color de un vecino.

**Consecuencia del orden.** Entre el tick en que nace una categoría (paso 4) y el primer momento en que
alguien puede unirse a ella (paso 4 del tick siguiente) siempre hay un paso de sanción. Además, la
imitación del paso 4 usa los colores anteriores a los movimientos de ese mismo tick: nadie puede imitar
a un pionero en el tick en que este se mueve.

## Proposición 8 (umbral de sanción)
Sea q = 1. Supongamos que, tras la reversión, todas las categorías presentes salvo una nueva x están
establecidas, y que x tiene j miembros.

- **(a) Las categorías establecidas son inmunes.** Si j ≥ v_min, ningún miembro de x es empujado:
  la sanción solo puede añadirle miembros.
- **(b) La supervivencia por debajo del umbral es un producto.** Si j < v_min, el miembro i de x sobrevive
  al paso de sanción si y solo si el vecino que mira tiene color x. Esto ocurre con probabilidad n_i/6,
  donde n_i es el número de sus vecinos con color x, y de forma independiente entre miembros. Por tanto,
  la probabilidad de que x conserve sus j miembros es ∏_i n_i/6.
- **(c) Un pionero solitario nunca funda.** Si v_min ≥ 2 y j = 1, entonces n_1 = 0 y el pionero es
  devuelto con certeza antes de que nadie pueda unirse a él.

**Demostración.**
- (a): la categoría x está establecida y la regla solo empuja a agentes de categorías no establecidas.
- (b): para el miembro i, su categoría no está establecida. El vecino que mira está en una categoría
  establecida, y entonces el empuje es seguro (q = 1), salvo que tenga color x, que es la única no
  establecida. La elección del vecino es independiente entre agentes.
- (c): es (b) con n_1 = 0. Por la consecuencia del orden, la sanción llega antes de cualquier unión. ∎

## Corolario 8.1 (tamaño fundador requerido)
Se combina con la Proposición 6 de C16: una coalición de j pioneros que salen de grupos
sobredimensionados a la vez supera la reversión si y solo si λ ≥ 1 − 2j/T. Sea
j_λ = max(1, ⌈T(1 − λ)/2⌉) el tamaño mínimo que exige la señal. Con q = 1, el tamaño fundador
que **garantiza** la supervivencia es

  **j\* = max(v_min, j_λ).**

Las coaliciones menores que v_min solo sobreviven con la probabilidad del producto (b).

Para pioneros que exploran al azar ese producto es mínimo. En un tick, los que eligen el mismo color nuevo
están en posiciones al azar. Dos de ellos son vecinos con probabilidad 6/99, y aun entonces conservan
los dos su color con probabilidad (1/6)² = 1/36. La predicción es que la adaptación depende de λ y
v_min solo a través de j\*: la escalera de C16 desplazada por v_min.

## Corolario 8.2 (la sanción total elimina la variedad de la rotación)
Con rotación, el recién llegado no socializado entra en el paso 2 con un color al azar, y la sanción del
paso 3 actúa en el mismo tick. Con q = 1 y vecinos establecidos, un color nuevo traído así desaparece
antes de que nadie pueda imitarlo. Bajo C, la única vía de creación de C17 era la de los recién
llegados no socializados, así que queda cerrada. Explica la adaptación 0 de C17 con q = 1.

## Lectura
- **La sanción fija un tamaño mínimo de fundación.** Sumado al modelo que le falta al regulador
  (C16), el requisito es el máximo de los dos: no se suman, se toma el más exigente. Una comunidad que
  sanciona toda categoría con menos de v_min miembros solo admite innovaciones que llegan ya como
  grupo.
- **Sociología.** Es el problema del innovador de Merton: la innovación empieza como desviación, y la
  tolerancia cero la reduce a lo que ya nace colectivo. Es también la cohorte fundadora de Elias y
  Scotson: lo que la sanción no deja nacer de uno en uno puede nacer en grupo. Para 4chan, una jerga
  nueva solo sobrevive a la burla si la traen varios a la vez (las oleadas de I-008).
- **Cibernética.** La sanción es un filtro de amplitud sobre la variedad: deja pasar solo las
  perturbaciones de tamaño ≥ v_min.

## Alcance
- Con q < 1, un pionero solitario sobrevive cada paso con probabilidad 1 − q, y la creación pasa a ser
  una carrera entre las uniones y la sanción. Esa parte no está formalizada.
- La condición «todas las demás categorías establecidas» excluye estados desordenados con varias
  categorías pequeñas vecinas.
