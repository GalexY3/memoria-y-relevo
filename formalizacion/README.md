# Formalización y simulación del diseño

Esta carpeta convierte el experimento mental del proyecto en un modelo ejecutable, demuestra sus
propiedades y prueba sus predicciones con hipótesis preregistradas. Diseño e idea: Alejandro Panera
Pascual. Programación realizada con asistencia de IA.

**Resultado central.** La señal colectiva del documento sabe qué tamaño debe tener cada grupo, pero
no cuántos grupos debe haber. Esa información la guarda el **vocabulario** de la comunidad, es
decir, los colores que usan los veteranos. Si los recién llegados entran con colores de la
comunidad, la institución se recupera si y solo si los veteranos conservan todas las categorías, y
la tasa de recuperación se puede calcular de antemano. Con una señal que sí cuenta los grupos, la
socialización deja de ser necesaria: socialización y retroalimentación estructural son sustitutivas.

![Recuperación según cuánto relevo hay, a qué ritmo llega y cuánto tarda](C09_RESULTS/c09_figura.png)

## Modelo

- Malla hexagonal toroidal de 10×10 (seis vecinos), 16 colores y meta de 4 grupos de 25.
- Agentes con una regla local de ensayo y reversión: si su señal indica malestar, prueban el
  color de un vecino (o uno al azar) y vuelven atrás en el siguiente turno si su señal empeora.
  Su memoria es de un paso y se borra al ser sustituidos.
- Tres señales: **individual** (distancia del tamaño del color propio a 25), **colectiva original**
  C (suma de |n − 25| sobre los colores presentes) y **colectiva corregida D** (distancia al reparto
  equilibrado en cuatro grupos más cercano). Variante de **dilema**: cada agente recibe además un
  premio privado por usar su color preferido, con preferencias sesgadas.

## Teorema

Demostración en [`TEOREMA_C09.md`](TEOREMA_C09.md), comprobada enumerando todos los estados
posibles para seis tamaños de comunidad (`c09_theory.py`).

1. Con exactamente cuatro grupos, la señal original y la corregida coinciden.
2. Con menos grupos de los necesarios, la señal original atrapa a la comunidad: crear un grupo
   siempre empeora la señal, así que una regla que no acepta empeorar nunca lo crea.
3. Con más grupos de los necesarios, la meta es alcanzable, pero a través de **mesetas**: estados
   en los que ningún cambio mejora y hay que vaciar un grupo entero sin que la señal lo premie. Las
   mesetas son exactamente los estados en que todos los grupos tienen como mucho 25 miembros y
   ninguno tiene uno solo.
4. La señal corregida D no tiene trampas ni mesetas.

Además, la señal individual define un juego de potencial con una trampa en tres grupos (34/33/33),
y en el dilema el reparto equilibrado se mantiene si el premio privado es menor que 1/N.

## Resultados

Todas las fases principales están preregistradas, con huellas SHA-256 del código fijadas antes de
ejecutar. En total, 49 de 53 hipótesis confirmadas; las cuatro refutadas se describen abajo. Una
reimplementación ciega a partir de una especificación escrita reproduce los resultados principales
(`replicacion_ciega/`).

**1. Aprendizaje (exploratorio).** Agentes Q independientes no resuelven la tarea con ninguna
señal. Con ensayo y reversión, la señal D llega a 4×25 en el 98–100% de las comunidades, la
individual nunca y la colectiva original en el 0–9%.

**2. Relevo del 30% (`PREREG_C08_RELEVO.md`, 5 de 6).** Con D todas las comunidades se recuperan,
entren los nuevos como entren; los que copian a un veterano aceleran la recuperación un 30–45%. La
señal individual sigue atrapada. **Refutada:** que un grupo nuevo de recién llegados rompiera esa
trampa (el grupo nuevo se vacía y se vuelve a 34/33/33).

**3. Qué necesita saber un recién llegado (`PREREG_C08B_SOCIALIZACION.md`, 5 de 5).** Con la señal
original y 248 comunidades que ya coordinaban:

| Color de entrada | Recuperan (disperso / contiguo) |
|---|---|
| copia a un vecino veterano | 248/248 · 248/248 |
| copia a un veterano cualquiera | 248/248 · 248/248 |
| uno de los colores de los veteranos, al azar | 248/248 · 248/248 |
| cualquier color | 8/248 · 7/248 |
| un color nuevo | 4/248 · 11/248 |

Lo transmitido es el vocabulario, no la proximidad ni las proporciones. Con relevos sucesivos hasta
no dejar ningún fundador, las comunidades siguen coordinadas.

**4. Ley de supervivencia del vocabulario (`PREREG_C09.md`, 12 de 13; 512 comunidades por celda).**

- Si los recién llegados usan colores de la comunidad, la recuperación ocurre exactamente cuando los
  veteranos que quedan conservan los cuatro colores: acuerdo del 100%, comunidad a comunidad, con
  relevos del 30% al 97%, dispersos o contiguos.
- La tasa coincide con la probabilidad hipergeométrica de que los veteranos cubran los cuatro
  colores, calculada antes de simular:

  | Sustituidos | 30% | 60% | 80% | 90% | 93% | 95% | 97% |
  |---|---|---|---|---|---|---|---|
  | Predicción | 1,000 | 1,000 | 0,994 | 0,812 | 0,541 | 0,249 | 0 |
  | Simulación | 1,000 | 1,000 | 0,994 | 0,830 | 0,563 | 0,246 | 0 |

- Con la señal D, todas las comunidades se recuperan en todos los casos, aunque se pierdan
  categorías: la señal las recrea.
- Si los recién llegados traen colores ajenos, la comunidad no queda bloqueada sino en una meseta:
  la mitad se recupera en 64 000 turnos (mediana 26 115, unas 500 veces más que con entrada
  socializada). Si los agentes solo aceptan mejoras estrictas, la meseta se convierte en trampa.
- El patrón se repite con 2 y 5 grupos.
- **Refutada:** espaciar en el tiempo los mismos 30 relevos no ayuda. El color ajeno no desaparece
  rápido: a menudo un vecino lo adopta antes de que su portador lo abandone.

**5. Un solo recién llegado (`PREREG_C09C_UN_RECIEN_LLEGADO.md`, 3 de 3; 1024 comunidades).** Una
única persona que entra con un color propio en una comunidad ya coordinada deja un quinto grupo
persistente de unas 20 personas en el 25,6% de las comunidades con la señal original. No lo logra
por ventaja, sino porque unirse a su grupo no cuesta nada. Con la señal D, nunca.

**6. La paradoja del gatekeeping (`PREREG_C10_PARADOJA_GATEKEEPING.md`, 4 de 5; y
`PREREG_C10B_TASA_DE_DESVIACION.md`, 2 de 3; 512 comunidades por celda).** Rotación continua (un
recién llegado cada τ turnos, socializado con probabilidad s) y, después de una fase estable, un
entorno que pasa a exigir cinco grupos de 20.

![Estabilidad y adaptación según la socialización y la tasa de desviación](C10_RESULTS/c10_figura.png)

- Con la señal original, socializar a todos los recién llegados da una estabilidad casi perfecta y
  hace **imposible** adaptarse: la comunidad nunca crea el quinto grupo (lo predice el teorema:
  crear un grupo siempre empeora esa señal).
- Sin socialización tampoco hay adaptación: entran tantas categorías ajenas que la comunidad se
  queda en una meseta. La adaptación es máxima con una **dosis intermedia de desviación**: más o
  menos una entrada no socializada cada 1000–2000 turnos. Recuerda la tesis de Durkheim sobre la
  normalidad del crimen: sin desviación, rigidez; con demasiada, anomia.
- Con la señal D no hay dilema: socializar siempre ayuda.
- La tasa de entradas no socializadas explica el 81–91% de la variación con la señal original; con
  la señal D lo explica todo el ritmo de rotación. **Refutadas:** que las curvas coincidieran
  exactamente al ordenarlas por esa tasa (una rotación muy alta añade un coste propio) y una
  cláusula secundaria sobre la señal D.

Lectura: el beneficio de incorporar reclutas no socializados que describió March (1991) aparecería
solo cuando el regulador colectivo no contiene un modelo de la estructura que se le exige. En 4chan,
el gatekeeping por jerga es intenso y la creación de tablones nuevos, como /pol/, la decide la
administración, no los participantes: lo que el modelo espera de un sistema muy socializado.

**7. La autodescripción como modelo del sistema (`PREREG_C12_AUTODESCRIPCION.md`, 5 de 5).** Los
agentes evalúan su situación con un canon, la lista de categorías que el sistema reconoce como
propias, al modo de unas Rules of the Internet. Si el canon es fijo, la comunidad se recupera siempre
tras el relevo (100%, frente al 2% sin canon), pero nunca crea la categoría que el entorno exige. Si
el canon se reescribe observando qué categorías tienen al menos θ miembros, consigue las dos cosas a
la vez con un umbral intermedio (θ ≈ 8, un tercio del tamaño de grupo). Con un umbral bajo, la
descripción convierte la desviación en canon; con uno alto, no reconoce lo nuevo.

![Homeostasis y morfogénesis según el umbral de reconocimiento](C12_RESULTS/c12_figura.png)

Lectura: la autodescripción le da al sistema el modelo de su propia estructura que le falta a la
señal; si además se revisa observando al sistema, este puede cambiar de estructura sin depender de
una administración externa. El umbral de reconocimiento funciona como una cristalización colectiva:
el tamaño a partir del cual una categoría se vuelve reconocible para el sistema.

**8. El canon vivo: la autodescripción escrita por el propio sistema (`PREREG_C13_CANON_VIVO.md`, 8 de 8;
512 comunidades por condición).** En el punto 7 el canon lo reescribía un observador externo. Aquí lo
escriben los agentes, de dos maneras:
- **Por alivio:** alguien propone su categoría y se acepta si reduce el malestar compartido.
- **Por repetición:** es canónico lo que se ha citado al menos r veces en las últimas W citas, una
  memoria social con olvido.

Las proposiciones están demostradas en [`TEOREMA_C13.md`](TEOREMA_C13.md).

![Umbral, memoria, voz y tiempos de reconocimiento](C13_RESULTS/c13_figura.png)

- **El alivio fija el umbral en exactamente la mitad del tamaño de grupo, T/2.** Nadie lo elige: sale
  del propio malestar, y quién proponga no cambia qué se acepta.
  - **Reconoce tarde lo nuevo:** cuando el entorno pide un quinto grupo, la comunidad falla en el 29%
    de los casos y nombra la categoría nueva 3,6 veces más tarde que con θ = 8.
  - **Olvida pronto lo viejo:** cuando el entorno pide disolver un grupo, deja de nombrarlo en 77
    turnos, frente a 1050 con θ = 8.
  - **Da por perdidas las categorías heridas:** tras un relevo del 45% se recupera el 85% de las
    comunidades, frente al 100%.
- **Ningún umbral fijo sirve para las dos cosas.** El mejor para crear un grupo es θ ≈ 6 (un tercio
  del tamaño) y el mejor para disolverlo, θ ≈ 13 (la mitad). Una regla estable que solo mire el
  tamaño actual no puede ser rápida en ambos sentidos: para no oscilar tiene que exigir más para
  entrar que para salir.
- **La memoria social tiene un óptimo interior.** Con W ≈ 50–100 citas la comunidad se adapta en
  ambos sentidos. Con W = 800 casi nunca se adapta; con W = 25 el canon parpadea.
- **La voz de los recién llegados importa en el canon por repetición y no en el de alivio.** Si
  hablan una de cada cinco veces o más, sus categorías de un solo miembro entran en el canon y
  desestabilizan la institución.
- **El paisaje del alivio no tiene trampas, pero sí muchas mesetas.** Se demuestra y se comprueba
  enumerando todos los estados en nueve tamaños de comunidad (`c13_theory.py`). Separarse de un grupo
  demasiado grande deja de costar, pero lo nuevo avanza por azar hasta cruzar la mitad.

**9. Orden desde el ruido (`PREREG_C13B_ORDEN_DESDE_EL_RUIDO.md`, 5 de 5).** Si el canon se rehace en
cada turno con lo que se ve en una muestra de 50 personas, y no contando a todas, la comunidad crea y
disuelve categorías mejor que con cualquier descripción exacta:
- con la muestra de 50, la suma de errores es 7,7;
- con el mejor umbral exacto es 10,0;
- con una muestra de 12, el canon cambia sin parar y la suma sube a 26,0.

Hay, por tanto, una dosis óptima de imprecisión. La memoria de lo dicho no añade nada, la estabilidad
no se resiente y basta con revisar el canon cada 20 turnos. Es el principio de «orden desde el ruido»
de von Foerster aplicado a la forma en que una comunidad se observa a sí misma.

Lectura: una autodescripción que se corrige para aliviarse va por detrás de la estructura cuando hay
que crear y por delante cuando hay que olvidar. Es un mecanismo para la tesis de Luhmann de que la
semántica sigue a la estructura con retraso. La autodescripción ruidosa y frecuente (como la jerga que
circula) es rápida, pero la pueden capturar las oleadas de recién llegados.

## Lectura sociológica (para discutir)

La entrada con colores de la comunidad se parece a la socialización serial de Van Maanen y Schein
(1979): los veteranos sirven de modelo. La entrada con colores propios se parece a la disyuntiva.
La señal original equivale a normas de tamaño que cada grupo vigila por su cuenta; la corregida, a un
plano explícito de la estructura, como un organigrama. El modelo predice que, cuando el control es
local y por grupos, la rotación sin socialización multiplica las categorías y vuelve muy lenta la
recuperación, mientras que un plano explícito hace innecesaria la socialización para conservar la
estructura.

## Alcance y antecedentes

Es un modelo de juguete con reglas de búsqueda local: muestra mecanismos posibles, no leyes
sociológicas. El teorema vale para cualquier regla que no acepte empeorar la señal, no para
aprendices que sí la empeoran. Trabajos más cercanos: Harrison y Carroll (1991, 2002; libro de 2006)
sobre transmisión cultural con rotación en organizaciones; Carley (1992) sobre aprendizaje
organizativo y rotación; Zoethout, Jager y Molleman (2010) sobre recién llegados en la asignación
autoorganizada de tareas; Kitts y Trowbridge (2007); modelos de juego de nombres con reemplazo de
población (Colaiori et al., 2015); March (1991). No hemos encontrado trabajos que distingan una
señal que conoce tamaños de una que conoce el número de grupos, ni que prevean la recuperación con
la supervivencia del vocabulario, pero la búsqueda no ha sido exhaustiva. Para el canon vivo, lo más
cercano son March, Schulz y Zhou (2000) sobre la dinámica de las reglas escritas; Colyvas y Maroulis
(2015) sobre cómo una práctica desviada se vuelve regla desde abajo; Centola et al. (2018) sobre
masas críticas; y Esposito sobre el olvido social. No hemos encontrado modelos que deriven el umbral
de reconocimiento del alivio ni el compromiso entre reconocer y olvidar.

## Reproducir

Requiere Python 3 con NumPy (y Matplotlib para las figuras). Desde esta carpeta:

```
python c08_pilot.py              # aprendizaje con las tres señales
python c08_pilot_dilemma.py      # variante de dilema
python c08_turnover.py           # relevo (≈2 min)
python c08b_confirm.py           # socialización y sucesión (≈40 min)
python c08b_figure.py
python c09_theory.py             # enumeración exhaustiva del teorema
python c09_experiments.py        # ley del vocabulario, ritmo, horizonte largo, regla estricta, k (≈17 min)
python c09c_single.py            # un solo recién llegado
python c09_figures.py
python c10_confirm.py            # paradoja del gatekeeping (≈30 min)
python c10b_collapse.py          # tasa de desviación (≈15 min)
python c10_figure.py
python c12_confirm.py            # autodescripción y umbral de reconocimiento (≈10 min)
python c12_figure.py
python c13_confirm.py AC          # canon vivo, homeostasis y disolución (≈14 min)
python c13_confirm.py B           # canon vivo, creación y dosis de voz (≈12 min)
python c13_verdicts.py
python c13_figure.py
python c13_theory.py              # enumeración exhaustiva del paisaje del alivio
python c13b_confirm.py B; python c13b_confirm.py C; python c13b_confirm.py A   # orden desde el ruido (≈30 min)
python c13b_verdicts.py
python c13x_explore.py            # exploratorio: frecuencia, ruido y memoria
python c13x_theta_u1.py
```

Los archivos `FREEZE_*.txt` guardan las huellas SHA-256 del código y de los preregistros fijadas
antes de ejecutar los análisis principales (`sha256sum -c FREEZE_C09C.txt`). En `FREEZE_C09.txt`,
`FREEZE_C10.txt`, `FREEZE_C12.txt`, `FREEZE_C13.txt` y `FREEZE_C13B.txt`, la ruta `../claude_cycle08/c08_sim.py` corresponde al
`c08_sim.py` de esta carpeta (misma huella).
