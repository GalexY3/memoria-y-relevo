# C16 · Fracción de modelo requerida para crear y para disolver (variedad requerida en forma cuantitativa)

**Notación.** N agentes y k grupos objetivo de tamaño T = N/k. Señal mezcla:

  S_λ = (1 − λ) C + λ D,  con λ ∈ [0, 1].

- C es la señal colectiva original: Σ sobre los grupos presentes de |s − T|.
- D es la distancia L1 al reparto equilibrado.
- λ es la **fracción de modelo estructural** que contiene el regulador. Con λ = 0 la señal no sabe
  cuántos grupos debe haber (C09); con λ = 1 lo sabe del todo.

La dinámica es de prueba y reversión síncrona: se conservan los movimientos que no aumentan S_λ.

## Proposición 6 (umbral coalicional para crear)
Sea un estado con k − 1 grupos sobredimensionados (cada uno con s ≥ T + j) y ningún grupo vacante que
llenar. Una coalición de j agentes que se mueven a la vez a un color nuevo, cada uno desde un grupo
sobredimensionado, cambia la señal en:

  ΔC = −j + |j − T| = T − 2j  (para j ≤ T),  ΔD = −j − j = −2j.

Por tanto, ΔS_λ = (1 − λ)(T − 2j) − 2jλ = T(1 − λ) − 2j. La coalición se conserva si y solo si

  **λ ≥ 1 − 2j/T.**

Casos particulares:
- con un solo agente, hace falta λ ≥ 1 − 2/T (0,9 con T = 20; 0,8 con T = 10);
- con la señal original (λ = 0), hace falta una coalición de más de T/2 agentes a la vez.

## Proposición 7 (disolver no requiere casi modelo)
En una meseta de C (todos los grupos ≤ T, ninguno unitario, más de k grupos), mover un agente de un
grupo sobrante a un grupo por debajo de T deja C igual (ΔC = 0) y baja D en 2. Por tanto,
ΔS_λ = −2λ < 0 para todo λ > 0. Cualquier fracción positiva de modelo estructural elimina las mesetas
que impiden disolver.

## Consecuencias
1. **Asimetría de la variedad requerida.**
   - Crear una categoría exige un modelo casi completo de la estructura, salvo que la innovación sea
     colectiva.
   - Disolver una exige un modelo infinitesimal.
2. **La innovación colectiva sustituye al modelo.** Una cohorte de j pioneros que funda una categoría
   a la vez rebaja la fracción de modelo necesaria en 2j/T. Bajo dinámica síncrona, las coaliciones
   de tamaño j se dan con una frecuencia que cae muy deprisa con j, así que la adaptación es una
   **escalera** en λ con peldaños en 1 − 2j/T.
3. **Ley de escala.** Los peldaños dependen de T. Con grupos pequeños, la misma fracción de modelo
   basta para crear; con grupos grandes, no.

## Lectura cibernética y sociológica
- Es el teorema del buen regulador de Conant y Ashby en forma cuantitativa: cuánto modelo de la
  estructura debe contener el regulador para cada tipo de cambio.
- La asimetría entre crear (que exige casi todo el modelo) y destruir (que exige casi nada) recuerda
  a la destrucción creadora y a la fragilidad de la innovación institucional. Crear una categoría
  social nueva exige o una visión estructural casi completa, o una cohorte que se lance a la vez.
- Una lectura con Collins y con Elias: los pioneros que fundan juntos son el sustituto colectivo del
  plan.
