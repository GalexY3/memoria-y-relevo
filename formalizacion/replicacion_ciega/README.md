# Reimplementación ciega

`SPEC_REPLICACION_CIEGA.md` describe el modelo solo con palabras: malla, señales, dinámica de prueba y
reversión, y los experimentos. Un segundo modelo de IA lo reimplementó desde cero a partir de ese
texto, sin acceso al código de esta carpeta y sin conocer los valores esperados. El código que
escribió es `replica.py`; sus resultados con dos semillas y 256 comunidades por celda están en
`RESULTS.json` y `RESULTS_seed7.json`.

| Experimento | Reimplementación (dos semillas) | Código original |
|---|---|---|
| Aprender con la señal D / con la señal C | 1,00 / 0,066 y 0,055 | 0,98–1,00 / 0–0,09 |
| Relevo del 90% con entrada socializada: recuperan | 0,758 y 0,816 | 0,830 |
| Probabilidad analítica de que los titulares conserven los 4 colores | 0,812 | 0,812 |
| Canon con umbral θ = 3 / 8 / 15: se adaptan a 5 grupos | 0,27 / 1,00 / 0,004 (y 0,23 / 1,00 / 0,016) | 0,26 / 1,00 / 0,012 |
| Canon por alivio, crear un grupo (4→5): se adaptan | 0,762 y 0,723 | 0,711 |
| Canon por alivio, tamaño mínimo al admitir una categoría | 11 | 11 (= T/2 + 1) |
| Canon por alivio, disolver un grupo (5→4): se adaptan / error medio | 1,000 / 2,56 | 0,998 / 2,61 |
| Umbral θ = 8, disolver: se adaptan / error medio | 0,977 / 8,87 | 0,967 / 8,78 |

Las diferencias están dentro del ruido de muestreo (error típico ≈ 0,03 con 256 comunidades). Los
resultados no dependen de detalles de la implementación original. No es una réplica independiente
hecha por personas; la especificación queda aquí para quien quiera hacerla.

Para ejecutar: `python replica.py` (Python 3 y NumPy; unos 50 segundos).
