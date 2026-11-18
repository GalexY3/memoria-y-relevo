# C13 · Tres proposiciones sobre autodescripciones que se reescriben

## Notación
N agentes y colores c con s_c miembros; tamaño objetivo T = N/k; canon K, el conjunto de colores que
el sistema nombra como propios. El malestar compartido (coste del canon, C12) es

  F(s, K) = Σ_{c ∈ K} |s_c − T| + Σ_{c ∉ K} s_c.

Los agentes hacen prueba y reversión: un movimiento se deshace si empeora F estrictamente. Por tanto,
los movimientos neutros (ΔF = 0) se conservan y producen deriva aleatoria.

## Proposición 1 (el alivio fija la mitad)
Si una propuesta para cambiar el estatus de un color se acepta si y solo si baja F estrictamente,
entonces c entra en el canon si y solo si s_c > T/2 y sale si y solo si s_c < T/2.

*Demostración.*
- Al admitir c, su término pasa de s a |s − T|, así que ΔF = |s − T| − s.
- Si 0 ≤ s ≤ T, ΔF = T − 2s, que es negativo si y solo si s > T/2.
- Si s > T, ΔF = −T < 0.
- Al retirarlo ocurre lo simétrico: ΔF = s − |s − T|, que es negativo si y solo si s < T/2. ∎

**Corolarios.**
1. **Sin parámetros e invariante de escala:** el umbral efectivo es θ = ⌊T/2⌋ + 1 y se desplaza con T. Si T es par, s = T/2 es neutro y el color conserva el estatus que tenía.
2. **Inmune a la voz:** quién propone cambia qué se propone y cuándo, pero no qué se acepta. Una categoría de un solo miembro no entra nunca.
3. **Reconoce cuando la mitad ya está hecha:** la descripción solo nombra una categoría cuando esta ya tiene la mitad de su tamaño objetivo.

## Proposición 2 (lo nuevo y lo viejo cambian por deriva neutra)
Primer caso: tras un aumento de k (T baja), los grupos canónicos quedan por encima de T. Mover un
agente de un grupo canónico g con s_g > T a un color c fuera del canon da

  ΔF = (|s_g − 1 − T| − |s_g − T|) + 1 = −1 + 1 = 0.

Segundo caso: tras una disminución de k (T sube), los grupos canónicos quedan por debajo de T. Mover
un agente entre dos grupos canónicos por debajo de T también da ΔF = 0.

Mientras la categoría nueva está fuera del canon, solo crece por deriva neutra, sin gradiente a su
favor. Lo mismo vale para la categoría obsoleta mientras sigue dentro: solo mengua por deriva
neutra. El gradiente aparece al cruzar el umbral:
- la nueva, una vez nombrada, atrae miembros mientras s < T;
- la obsoleta, una vez retirada, los expulsa.

**Consecuencia.** El tiempo hasta reconocer lo nuevo es un tiempo de primer paso desde 0 hasta θ. El
tiempo hasta olvidar lo viejo es un tiempo de primer paso desde s₀ (el tamaño del grupo obsoleto)
hasta θ. En una deriva sin sesgo ambos crecen aproximadamente con el cuadrado de la distancia. Por
eso un θ bajo favorece crear categorías y un θ alto favorece disolverlas.

## Proposición 3 (ninguna regla estable sin memoria es rápida en ambos sentidos)
Sea una regla sin memoria con histéresis: un color fuera del canon entra si s ≥ θ_in y uno dentro sale
si s < θ_out. Si θ_in < θ_out, todo color con θ_in ≤ s < θ_out cambia de estatus en cada revisión
(entra cuando está fuera y sale cuando está dentro): el canon oscila. Por tanto, una regla que no
oscila exige θ_in ≥ θ_out.

Pero reconocer pronto pide un θ_in bajo y olvidar pronto pide un θ_out alto. Con θ_in ≥ θ_out ambas
cosas no pueden darse a la vez: lo mejor que puede hacer una regla estable sin memoria es un umbral
único que reparte la deriva entre ambas tareas.

El uptake por alivio es la regla con θ_in = θ_out = T/2. Por la Proposición 2, eso lo sitúa cerca del
óptimo para disolver y lejos del óptimo para crear.

**Cómo se esquiva.** Una regla estocástica no es función determinista del tamaño actual. Hay dos
casos: una muestra instantánea (ruido sin memoria) o el canon por repetición en una ventana corta
(ruido y memoria). La exploración C13x indica que basta el ruido y que la memoria añade retraso. Puede admitir pronto, por fluctuaciones de las citas, y retirar pronto,
cuando las citas caen. El precio es ruido en la fase estable y vulnerabilidad a la voz desigual. Sería
lo que en otras ramas del programa llamamos desviación útil: aquí la desviación está en la
autodescripción, no en los agentes.

## Proposición 4 (con alivio, la autodescripción es un jugador más de un juego de potencial)
Con el uptake por alivio, los agentes (prueba y reversión) y el canon (revisión por alivio) bajan, o
dejan igual, la misma función F. Fuera de los choques exógenos (relevo, rotación), F no aumenta nunca:
es una función de Lyapunov débil de la dinámica conjunta.

Para una partición s fija, el canon que minimiza F es K*(s) = {c : s_c > T/2}, y entonces

  F*(s) = Σ_c g(s_c),  con g(s) = mín(s, |s − T|).

La función g es una «tienda»:
- sube con pendiente 1 de 0 a T/2;
- baja con pendiente 1 de T/2 a T;
- vuelve a subir por encima de T.

Por tanto, en cuanto el canon se ha ajustado, el paisaje que ven los agentes tiene una **divisoria en T/2**:
- una categoría por debajo de la mitad de su tamaño objetivo está en la cuenca de la extinción (cada miembro que sale baja F en 2 si va a un grupo canónico por debajo de T);
- una por encima está en la cuenca de la consolidación;
- los movimientos entre grupos del mismo lado y los que salen de grupos sobredimensionados son neutros (Proposición 2).

Los mínimos globales (F* = 0) son exactamente las particiones en grupos de T o vacíos; con N = kT, los k grupos de T.

**Lectura de teoría de juegos.** La autodescripción no es un observador externo, sino un jugador más
que comparte el potencial de los miembros. Su mejor respuesta (nombrar lo que pasa de la mitad)
convierte el paisaje en uno de dos cuencas por categoría. De ahí salen tres consecuencias:
- la categoría naciente debe cruzar T/2 por deriva neutra antes de que el sistema la favorezca, de modo que reconoce tarde;
- la obsoleta queda condenada en cuanto cruza T/2 hacia abajo, de modo que olvida pronto;
- una categoría herida por debajo de la mitad tras un choque queda en la cuenca de extinción (H7).

## Lectura sociológica
- **Alivio:** la autodescripción que el sistema corrige para sentirse mejor va por detrás de la estructura al crear. Es el desfase semántico de Luhmann. En cambio, va por delante al disolver: abandona deprisa lo que ha dejado de pesar, incluidas las categorías heridas por un choque.
- **Repetición con memoria corta:** puede anticipar la estructura (preadaptación semántica). Es más vulnerable a quién tiene la palabra.
- **Umbral fijo:** obliga a elegir entre innovación y olvido. Ninguna autodescripción estable y sin memoria puede ser a la vez receptiva a lo nuevo y desapegada de lo viejo.
