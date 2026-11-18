# PREREG C18 — Umbral de sanción: la sanción fija un tamaño mínimo de fundación

**Fecha:** 18/11/2026. **Estado:** preregistrado antes de la ejecución primaria.
- **Teoría:** `TEOREMA_C18.md` (Proposición 8 y corolarios 8.1 y 8.2).
- **Simulador:** `claude_cycle17/c17_sim.py`, sin cambios, congelado en C17. El SHA está repetido en `FREEZE_C18.txt`.
- **Pilotos exploratorios** (semillas 8800xx, 8801xx y 8802xx, no reutilizadas):
  - `c18_theory.py` con base 880000, salida en `C18_RESULTS/c18_theory.json`: la comprobación exacta pasa;
  - `c18_pilot.py`, salida en `pilot_c18.json`;
  - `c18_pilot_rotation.py`, salida en `pilot_c18_rotation.json`.
- **Confirmación** (semillas nuevas 8810xx, 8811xx y 8812xx; veredictos con `c18_verdicts.py`):
  - `c18_theory.py 8000 881000` para P1;
  - `c18_confirm.py stair` y `c18_confirm.py rot`, con M = 512.
- **Origen:** idea I-035, que sale de C17 (R8) y C16 (Proposición 6). Pedida por el usuario el 18/11/2026.

## Diseño
- **stair:** el escenario de C16. Sin rotación, instituciones 4 × 25 (1000 ticks) y después k = 5 (T = 20, 6000 ticks), con la señal S_λ.
  - Sanción total q = 1, con v_min ∈ {1, 2, 3, 4} y λ ∈ {1; 0,9; 0,8; 0,7}.
  - Referencias sin sanción (q = 0), con λ ∈ {1; 0,9; 0,8; 0,75; 0,7; 0,65}.
  - Sanción moderada q ∈ {0,2; 0,5}, con λ = 1 y v_min ∈ {2, 3}.
- **rot:** el escenario de C17, con señal C, rotación τ = 20, c = 0,95 y s = 0. Se compara q = 0 con q = 1 para v_min ∈ {1, 2, 3}.
- **Medidas:** adapt_ever (alcanzar 5 × 20), la mediana del tiempo de adaptación y la estabilidad (D medio con k = 4).

## Predicciones
Por el corolario 8.1, el tamaño fundador que garantiza la creación es j\* = max(v_min, j_λ), con
j_λ = max(1, ⌈T(1 − λ)/2⌉). Con T = 20, j_λ vale 1 para λ ∈ {1; 0,9}, 2 para 0,8 y 3 para 0,7.
- Las configuraciones con el mismo j\* deben adaptarse como el peldaño de C16 con ese tamaño de coalición:
  ≈ 1 con j\* ≤ 2, ≈ 0,13 con tríos y ≈ 0 con cuartetos.
- La sanción que no es la restricción activa (v_min ≤ j_λ) no debe cambiar nada.
- **Hallazgo del piloto, sin teorema:** bajo D (λ = 1), la sanción moderada acelera la creación porque
  poda las categorías solitarias que D deja fundar en paralelo.

## Hipótesis
- **P1 (Proposición 8, exacta).** Con 8000 configuraciones plantadas por caso y semillas nuevas:
  - el pionero solitario desaparece siempre (v_min = 2 y 3);
  - la coalición establecida (trío disperso con v_min = 3, solitario con v_min = 1) queda intacta siempre;
  - en el par adyacente (v_min = 3) y el triángulo (v_min = 4), la distribución de supervivientes coincide con la ley del producto (1/6 y 2/6 por miembro), con |z| ≤ 3 en cada recuento.
- **P2 (colapso sobre j\*).** En las 16 configuraciones con q = 1, adapt_ever es:
  - ≥ 0,95 si j\* ≤ 2;
  - de 0,05 a 0,40 si j\* = 3;
  - ≤ 0,02 si j\* = 4.
- **P3 (la sanción que no restringe es inerte).** Con λ = 0,7, adapt_ever con q = 1 y v_min ∈ {1, 2, 3} difiere de la referencia sin sanción en ≤ 0,08. Con λ ∈ {1; 0,9; 0,8} y v_min = 1, también difiere en ≤ 0,08.
- **P4 (la sanción moderada acelera la creación con modelo).** Con λ = 1, q = 0,2 y v_min ∈ {2, 3}, adapt_ever ≥ 0,95, y la mediana del tiempo de adaptación es ≤ 0,75 veces la de la referencia sin sanción con λ = 1.
- **P5 (corolario 8.2: la sanción total elimina la variedad de la rotación).** En rot:
  - con q = 1 y v_min ∈ {2, 3}, adapt_ever ≤ 0,02 y estabilidad D ≤ 1;
  - con q = 1 y v_min = 1, adapt_ever difiere de la referencia sin sanción en ≤ 0,10.

Cada hipótesis se declara confirmada o refutada sin cambiar umbrales. Cualquier análisis adicional será exploratorio.
