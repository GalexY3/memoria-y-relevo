# Teorema C09 — Qué sabe cada señal colectiva sobre la estructura del reparto

**Notación.** N agentes, objetivo k grupos de tamaño T = N/k (entero, T ≥ 3). Un estado es el
multiconjunto de tamaños positivos s₁ ≥ s₂ ≥ … ≥ s_m de los m grupos presentes (los colores son
intercambiables). Un *movimiento* lleva a un agente de un grupo a otro grupo presente o a un grupo
nuevo. Señales (costes):

- **C** (señal colectiva original del diseño): C(s) = Σ_{i≤m} |sᵢ − T|.
- **D** (corregida): distancia L1 al reparto equilibrado más cercano,
  D(s) = Σ_{i≤k} |sᵢ − T| + Σ_{i>k} sᵢ, con sᵢ = 0 para i > m. Equivale al mínimo, sobre todas
  las elecciones de k grupos que conservan su color, del número de cambios necesarios ×2.

Una dinámica es *no empeorante* si nunca acepta un movimiento que sube el coste (el ensayo y
reversión de C08 lo es, salvo movimientos simultáneos); *estricta* si solo acepta bajadas.

## Proposición 1 (D no tiene trampas ni mesetas)
Desde todo estado no resuelto existe un movimiento que baja D en 2.

*Prueba.* (a) m < k: como Σs = kT y hay menos de k grupos, algún sᵢ > T. Llevar un agente de ese
grupo a un grupo nuevo baja |sᵢ − T| en 1 y el grupo nuevo entra entre los k primeros pasando de
un déficit T a T − 1: ΔD ≤ −2. (b) m ≥ k y existe un grupo fuera de los k primeros: la suma de los
k primeros es < kT, luego alguno de ellos tiene sⱼ < T; mover un agente del grupo sobrante a ese
grupo baja ambos términos: ΔD ≤ −2 (con la elección de grupos anterior; el mínimo solo puede ser
menor). (c) m = k, no resuelto: hay un grupo > T y otro < T; mover de uno a otro: ΔD = −2. ∎

## Proposición 2 (C con exactamente k grupos)
Si m = k, entonces C(s) = D(s), y si el estado no está resuelto existe un movimiento entre grupos
presentes que baja C en 2.

*Prueba.* Con m = k no hay grupos fuera de los k primeros, luego ambas sumas coinciden. El
movimiento es el de 1(c). ∎

## Proposición 3 (C no puede crear grupos: trampas con menos de k)
Crear un grupo nuevo sube C al menos T − 2 > 0. Por tanto, bajo cualquier dinámica no
empeorante, el número de grupos presentes nunca aumenta, y todo estado con m < k está atrapado:
no alcanza el reparto equilibrado.

*Prueba.* Si el agente sale de un grupo de tamaño s, ΔC = (|s − 1 − T| − |s − T|) + |1 − T|
≥ −1 + (T − 1) = T − 2. El reparto equilibrado tiene m = k. ∎

## Proposición 4 (C con más de k grupos: alcanzable, pero por mesetas)
Si m > k, existe un camino de movimientos no empeorantes hasta el reparto equilibrado. Además,
ningún movimiento baja C estrictamente **si y solo si** todos los grupos son ≤ T y ninguno es
unitario (estados meseta).

*Prueba.* Mientras haya un grupo > T, existe otro < T (porque m > k implica tamaño medio < T):
mover de uno a otro da ΔC ∈ {−2, 0}. Cuando todos son ≤ T, se vacía el grupo más pequeño hacia otro
grupo < T (existe: si todos los demás valieran T, la suma superaría kT). Cada paso intermedio da
ΔC = +1 − 1 = 0, y el último, cuando sale el único miembro, da ΔC = −(T − 1) − 1 < 0. Se repite
hasta m = k y se aplica la Proposición 2. Para la segunda parte: entre grupos ≤ T, salir de un
grupo no unitario cuesta +1 y entrar en un grupo < T ahorra 1 (en uno = T cuesta +1); crear grupo
cuesta ≥ T − 2. Ningún movimiento baja C. Recíprocamente, si hay un grupo > T, mover de él a un
grupo < T baja C en 2; si hay un grupo unitario, vaciarlo hacia un grupo < T baja C en T. ∎

## Corolario (vocabulario)
Tras un relevo, si los recién llegados solo usan colores de los titulares y los titulares conservan
los k colores, el estado tiene m = k: la comunidad está en el conjunto donde C = D y puede
recuperarse por mejoras estrictas (Proposición 2). Si el vocabulario de los titulares ha perdido
un color, m < k y la comunidad queda atrapada bajo C (Proposición 3), pero no bajo D
(Proposición 1). Si los recién llegados introducen colores ajenos, m > k y la recuperación bajo C
exige atravesar mesetas (Proposición 4): imposible para una regla estricta, lenta para una que
acepta movimientos neutros.

**Lectura.** C sabe qué tamaño debe tener cada grupo, pero no cuántos grupos debe haber: no cobra
nada por un grupo que falta y cobra poco por un grupo sobrante de tamaño medio. El vocabulario
compartido aporta justo esa información (el número de categorías). Socialización y
retroalimentación estructural son, en este modelo, sustitutivas.

**Comprobación.** `c09_theory.py` enumera todos los estados para (N, k) ∈ {(12,3), (16,4), (20,4),
(24,4), (30,5), (32,4)} y verifica: C = D cuando m = k; ningún estado con m < k alcanza el objetivo
bajo C; todo estado con m ≥ k lo alcanza; todo estado no resuelto tiene mejora estricta bajo D; y el número de estados meseta coincide
exactamente con la caracterización de la Proposición 4 (6, 9, 27, 77, 148 y 461).
Movimientos simultáneos de varios agentes quedan fuera de las proposiciones; su efecto se mide en
las simulaciones.
