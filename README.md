# Simulador Estocástico de Fatiga en Ballestas Parabólicas

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Este repositorio contiene el desarrollo de un **Simulador Estocástico** avanzado diseñado para evaluar los puntos críticos de concentración de esfuerzos y predecir el fallo por fatiga estructural en hojas de muelle (ballestas parabólicas) de acero aleado **51CrV4** destinadas al transporte pesado.

El proyecto combina modelos físicos deterministas de flexión de vigas con el paradigma de **Simulación por Eventos Discretos (SED)** y la **Teoría de Colas**, abstrayendo las irregularidades viales como entidades dinámicas transitorias que impactan recursivamente la estructura del chasis.

---

## 📊 Características Principales

* **Motor Pseudoaleatorio Propio (LCG):** Implementación desde cero de un Generador Congruencial Lineal bajo el estándar numérico MINSTD ($m = 2^{31}-1$, $a = 16807$), garantizando independencia total y reproducibilidad sin librerías nativas de azar.
* **Auditoría Estadística:** Suite de pruebas integrada que ejecuta evaluaciones vectorizadas de *Uniformidad (Chi-Cuadrado $chi^{2}$)* e *Independencia (Prueba de Corridas)* para validar la calidad matemática del generador.
* **Simulación de Monte Carlo:** Procesamiento masivo de $100,000$ escenarios mediante la transformada inversa para mapear perfiles exponenciales de impacto dinámico.
* **Teoría de Colas Mecánica ($M/G/1$):** Modelado del muelle como un servidor viscoelástico con tiempos de relajación elástica, simulando la superposición lineal y el "encolamiento" de fuerzas cuando la frecuencia de baches supera el tiempo de amortiguamiento estructural.
* **Mapeo Espacial 2D (Heatmap):** Renderizado geométrico que proyecta la forma parabólica real de la viga y localiza visualmente los picos críticos de esfuerzo en el punto central de anclaje de los pernos en U.

---

## Fundamento Matemático

El esfuerzo axial por flexión instantáneo ($\sigma$) en las caras críticas del muelle se calcula en el script mediante la relación constitutiva de la mecánica de materiales:

$$\sigma = \frac{1.5 \cdot F \cdot L}{b \cdot h^2}$$

Donde:
* $F$: Fuerza estocástica del bache acumulada por el sistema ($N$).
* $L$: Longitud geométrica del componente ($1.2 \text{ m}$).
* $b$: Ancho de la sección central ($0.08 \text{ m}$).
* $h$: Espesor elástico de la hoja central ($0.02 \text{ m}$).

El software determina un fallo estructural de manera binaria en cada ciclo si la tensión inducida supera el límite de fluencia elástica del material ($\sigma > 1300 \text{ MPa}$).

Distribución de esfuerzos en una Hoja de Muelle frontal
<img width="1118" height="490" alt="image" src="https://github.com/user-attachments/assets/94ec2ee5-e198-4dac-b697-7c7c489cade3" />

Probabilidad de fallo con Monte Carlo
<img width="990" height="590" alt="image" src="https://github.com/user-attachments/assets/b7c90771-341a-45d0-b9a9-e4272de840d0" />

---

## Instalación y Requisitos

Para clonar y ejecutar este simulador de forma local, asegúrate de contar con Python 3.8+ y las siguientes librerías científicas:

```bash
# Clonar el repositorio
git clone [https://github.com/tu_usuario/tu_repositorio.git](https://github.com/tu_usuario/tu_repositorio.git)
cd tu_repositorio

# Instalar dependencias científicas
pip install numpy matplotlib scipy

