# Simulaci-n-de-esfuerzo-en-Hojas-de-Muelle
Se plantea la simulación de puntos de esfuerzo tras cargas pseudoaleatorias en hojas de muelle para suspensión de transporte pesado




Se presentaron los siguientes resultados:

--- FASE 1: LCG ---
Primeros 5 números U(0,1) generados: [0.09661653 0.83399463 0.9477025  0.03587859 0.01154585]

--- FASE 2: PRUEBA CHI-CUADRADO (Uniformidad) ---
Estadístico Chi-Cuadrado: 1.4670
Valor p: 0.9974
Decisión: Se ACEPTA la Hipótesis Nula (Los datos siguen una distribución uniforme).

/tmp/ipykernel_5994/2334414550.py:72: RuntimeWarning: overflow encountered in scalar multiply
  var_r = (2 * n1 * n2 * (2 * n1 * n2 - len(datos))) / ((len(datos)**2) * (len(datos) - 1))
--- FASE 3: PRUEBA DE CORRIDAS (Independencia) ---
Estadístico Z: -3.3585
Valor p: 0.0008
Decisión: Se RECHAZA la Hipótesis Nula.

--- FASE 4: SIMULACIÓN DE MONTE CARLO ---
Límite de fluencia crítico: 1300 MPa
Total de impactos simulados: 100000
Impactos que causaron daño estructural (Fallo): 51631
Probabilidad de Falla Estructural: 51.63%

Distribución de esfuerzos en una Hoja de Muelle frontal
<img width="1118" height="490" alt="image" src="https://github.com/user-attachments/assets/94ec2ee5-e198-4dac-b697-7c7c489cade3" />

Probabilidad de fallo con Monte Carlo
<img width="990" height="590" alt="image" src="https://github.com/user-attachments/assets/b7c90771-341a-45d0-b9a9-e4272de840d0" />
