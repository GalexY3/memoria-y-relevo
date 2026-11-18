# PREREG C13b — Orden desde el ruido: una autodescripción imprecisa y frecuente

**Fecha:** 18/11/2026. **Estado:** preregistrado antes de la ejecución primaria.

**Antecedentes exploratorios (no reutilizados):**
- `c13x_explore.py` y `c13x_theta_u1.py`, con semillas 8380xx;
- `c13b_pilot.py`, con semillas 8480xx; salida en `C13_RESULTS/pilot_c13b.json`.

**Confirmación:** `c13b_confirm.py` con semillas nuevas 8490xx y M = 512, en tres partes (B, C y A).
Usa el simulador `c13x_sim.py`, que es `c13_sim.py` (congelado en C13) más el modo `sampled`. SHA en
`FREEZE_C13B.txt`. Idea I-025 del cuaderno.

## Pregunta y marco
C13 mostró que una autodescripción exacta y sin memoria no puede ser a la vez rápida reconociendo lo
nuevo y rápida olvidando lo viejo (Proposición 3). La exploración C13x sugirió que el canon
comunicativo esquiva ese límite gracias al ruido de muestreo, no a la memoria.

La tradición cibernética lo anticipa en abstracto:
- el principio de **orden desde el ruido** de von Foerster (1960) y la complejidad desde el ruido de Atlan;
- la ultraestabilidad de Ashby, que reorganiza con cambios aleatorios.

Aquí se pone a prueba en la autodescripción de una comunidad. ¿Es mejor un sistema que se describe
cada momento con lo que oye a unos pocos (un rumor, una muestra pequeña) que uno que se describe con
exactitud?

## Modelo
Dinámica, rotación y experimentos como en C13: B (crear, k 4→5), C (disolver, k 5→4) y A (choque del 30%).
Canones comparados:
- **Muestreado (`sampled`):** cada U ticks se toma una muestra aleatoria de n agentes. Son canónicos
  los colores con al menos r = 8n/N miembros en la muestra: el mismo umbral relativo que θ = 8, pero
  estimado con ruido. Se usa n ∈ {12, 25, 50, 100} con U = 1, y n = 50 con U ∈ {5, 20}. Con n = 100 la
  muestra es toda la población y el canon es exacto.
- **Constatativo exacto revisado en cada tick:** θ ∈ {6, 7, 8, 9, 10, 13}.
- **Comunicativo:** W = 50, r = 4, memoria de citas (C13).

Medida principal: la suma de los errores medios de adaptación de B y C (crear y disolver).

## Hipótesis
- **N1 (orden desde el ruido).** suma(muestreado n = 50, U = 1) < mín over θ de suma(constatativo exacto θ, U = 1).
- **N2 (óptimo interior del ruido).** suma(n = 50) < suma(n = 12) y suma(n = 50) < suma(n = 100); además suma(n = 12) > 2 × suma(n = 50).
- **N3 (la memoria no añade valor).** suma(muestreado n = 50, U = 1) < suma(comunicativo W = 50).
- **N4 (el ruido moderado apenas cuesta estabilidad).**
  - con n = 50 y U = 1, la recuperación en A es ≥ 0,98;
  - su error en la fase estable de B no supera en más de 0,2 al del exacto θ = 8, U = 1.
- **N5 (no hace falta revisar en cada tick).** suma(muestreado n = 50, U = 20) < mín over θ de suma(constatativo exacto θ, U = 1).

Cada hipótesis se declara confirmada o refutada sin cambiar umbrales. El resto es descriptivo.

## Lectura prevista
Una autodescripción algo imprecisa, rehecha a menudo con lo que se oye a una muestra, deja entrar
pronto lo nuevo y salir pronto lo viejo. Funciona mejor que la descripción exacta y que la memoria de
lo dicho. Demasiado ruido es anomia: el canon admite cualquier cosa. Ninguno es rigidez.
Es la tesis de la desviación útil (C10: Durkheim, March) trasladada de los miembros a la autoobservación del sistema.
