import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import math

# =====================================================================
# SEMANA 5: Generador Congruencial Lineal (LCG) desde cero
# =====================================================================
def generar_lcg(n, semilla=12345):
    """
    Genera 'n' números pseudoaleatorios U(0,1) utilizando el algoritmo LCG.
    Parámetros estandarizados MINSTD (Park-Miller).
    """
    m = 2**31 - 1  # Módulo
    a = 16807      # Multiplicador
    c = 0          # Incremento

    numeros_u = np.zeros(n)
    x = semilla

    for i in range(n):
        x = (a * x + c) % m
        numeros_u[i] = x / m  # Normalización a U(0,1)

    return numeros_u

# Generamos 100,000 escenarios (impactos en la suspensión)
N_simulaciones = 100000
u_aleatorios = generar_lcg(N_simulaciones)

print(f"--- FASE 1: LCG ---")
print(f"Primeros 5 números U(0,1) generados: {u_aleatorios[:5]}\n")

# =====================================================================
# SEMANA 6: Auditoría y Validación Estadística
# =====================================================================

def prueba_chi_cuadrado(datos, num_intervalos=10):
    """Prueba de Bondad de Ajuste para Uniformidad."""
    frecuencias_obs, _ = np.histogram(datos, bins=num_intervalos, range=(0, 1))
    frecuencia_esp = len(datos) / num_intervalos

    chi_calc = np.sum((frecuencias_obs - frecuencia_esp)**2 / frecuencia_esp)
    grados_libertad = num_intervalos - 1
    p_valor = stats.chi2.sf(chi_calc, grados_libertad)

    print(f"--- FASE 2: PRUEBA CHI-CUADRADO (Uniformidad) ---")
    print(f"Estadístico Chi-Cuadrado: {chi_calc:.4f}")
    print(f"Valor p: {p_valor:.4f}")

    if p_valor > 0.05:
        print("Decisión: Se ACEPTA la Hipótesis Nula (Los datos siguen una distribución uniforme).\n")
    else:
        print("Decisión: Se RECHAZA la Hipótesis Nula.\n")

def prueba_corridas(datos):
    """Prueba de Independencia (Runs Test)."""
    mediana = 0.5 # Mediana teórica de U(0,1)
    secuencia = datos > mediana

    # Contar corridas
    corridas = 1
    n1 = np.sum(secuencia)       # Valores por encima
    n2 = len(datos) - n1         # Valores por debajo

    for i in range(1, len(datos)):
        if secuencia[i] != secuencia[i-1]:
            corridas += 1

    # Valores esperados
    media_r = ((2 * n1 * n2) / len(datos)) + 1
    var_r = (2 * n1 * n2 * (2 * n1 * n2 - len(datos))) / ((len(datos)**2) * (len(datos) - 1))
    z_calc = (corridas - media_r) / math.sqrt(var_r)
    p_valor = 2 * stats.norm.sf(abs(z_calc)) # Prueba de dos colas

    print(f"--- FASE 3: PRUEBA DE CORRIDAS (Independencia) ---")
    print(f"Estadístico Z: {z_calc:.4f}")
    print(f"Valor p: {p_valor:.4f}")

    if p_valor > 0.05:
        print("Decisión: Se ACEPTA la Hipótesis Nula (Los números son independientes).\n")
    else:
        print("Decisión: Se RECHAZA la Hipótesis Nula.\n")

# Ejecutar auditoría
prueba_chi_cuadrado(u_aleatorios)
prueba_corridas(u_aleatorios)

# =====================================================================
# SEMANA 7: Modelo Determinista y Método de Monte Carlo
# =====================================================================
print(f"--- FASE 4: SIMULACIÓN DE MONTE CARLO ---")

# 1. Variables del Modelo Determinista (Física de la Hoja de Muelle)
L = 1.2    # Longitud del muelle (metros)
b = 0.08   # Ancho de la hoja central (metros)
h = 0.02   # Grosor de la hoja central (metros)
limite_fluencia_MPa = 1300  # Esfuerzo de fluencia para Acero 51CrV4 (en MPa)

# Transformada Inversa: Asumimos que la fuerza del impacto sigue una distribución Exponencial.
# Convertimos los números U(0,1) en Fuerzas (Newtons)
fuerza_promedio_N = 35000 # Fuerza promedio de un bache en transporte pesado
fuerzas_impacto = -fuerza_promedio_N * np.log(1 - u_aleatorios)

# Ecuación Determinista: Esfuerzo de flexión máximo (sigma = 1.5 * F * L / (b * h^2))
# Convertimos el resultado de Pascales a MegaPascales (MPa) dividiendo por 1e6
esfuerzos_simulados_MPa = (1.5 * fuerzas_impacto * L) / (b * h**2) / 1e6

# 2. Condición de Acierto / Fallo
# Fallo: Si el esfuerzo supera el límite de fluencia del material
fallos = esfuerzos_simulados_MPa > limite_fluencia_MPa
numero_de_fallos = np.sum(fallos)
prob_falla_final = numero_de_fallos / N_simulaciones

print(f"Límite de fluencia crítico: {limite_fluencia_MPa} MPa")
print(f"Total de impactos simulados: {N_simulaciones}")
print(f"Impactos que causaron daño estructural (Fallo): {numero_de_fallos}")
print(f"Probabilidad de Falla Estructural: {prob_falla_final * 100:.2f}%\n")

# 3. Demostración de la Ley de los Grandes Números (Vectorizado)
# Calculamos la probabilidad acumulada paso a paso
probabilidad_acumulada = np.cumsum(fallos) / np.arange(1, N_simulaciones + 1)




# =====================================================================
# FASE 5: Visualización Física y Mapa de Calor de Esfuerzos (Heatmap)
# =====================================================================

print(f"--- FASE 5: GENERANDO MAPA DE CALOR DE LA HOJA DE MUELLE ---")

# 1. Parámetros geométricos de la ballesta
longitud = L # 1.2 metros (definido en la Fase 4)
camber = 0.15 # Curvatura máxima (flecha) del muelle sin carga (en metros)

# Generamos 500 puntos a lo largo del eje X (desde -L/2 hasta L/2)
x_coords = np.linspace(-longitud/2, longitud/2, 500)

# Ecuación de una parábola para simular la forma de la hoja de muelle: y = a*x^2 + c
# Ajustamos para que en x=0, y=0 (centro) y en x=L/2, y=camber (extremos)
y_coords = camber * (2 * x_coords / longitud)**2 

# 2. Distribución teórica del esfuerzo
# En una ballesta semi-elíptica, el momento flector (y por ende el esfuerzo)
# es máximo en el anclaje central (x=0) y se reduce hacia los extremos (x = L/2 y -L/2).
# Tomamos el esfuerzo máximo promedio de nuestra simulación anterior:
esfuerzo_max_simulado = np.mean(esfuerzos_simulados_MPa)

# Creamos un perfil de esfuerzo lineal absoluto (forma de "tienda de campaña")
perfil_esfuerzo = esfuerzo_max_simulado * (1 - np.abs(2 * x_coords / longitud))

# 3. Creación de la gráfica interactiva 2D
plt.figure(figsize=(12, 5))

# Usamos plt.scatter para poder mapear colores (cmap) a cada punto de la curva
# cmap='jet' va de azul (bajo esfuerzo) a rojo oscuro (alto esfuerzo)
mapa_calor = plt.scatter(x_coords, y_coords, c=perfil_esfuerzo, cmap='jet', 
                         s=150, edgecolor='none', label='Perfil del Muelle')

# Barra de colores lateral para indicar los valores
cbar = plt.colorbar(mapa_calor)
cbar.set_label('Esfuerzo Acumulado (MPa)', fontsize=12, fontweight='bold')

# Marcar el punto crítico (Pernos U / Centro)
plt.axvline(x=0, color='black', linestyle='--', alpha=0.6)
plt.annotate('Zona de Máximo Esfuerzo\n(Punto Crítico / Anclaje)', 
             xy=(0, 0), xytext=(0.1, 0.05),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             fontsize=11, fontweight='bold', color='darkred')

# Línea del límite de fluencia en la barra de color (opcional, para visualización)
cbar.ax.axhline(limite_fluencia_MPa, color='red', linewidth=3)
cbar.ax.text(1.5, limite_fluencia_MPa, 'Límite de\nFluencia', color='red', va='center')

# Configuraciones de la gráfica
plt.title('Simulación de Distribución de Esfuerzos en Hoja de Muelle Frontal', fontsize=15, fontweight='bold')
plt.xlabel('Posición Longitudinal a lo largo del Eje (metros)', fontsize=12)
plt.ylabel('Deflexión / Geometría (metros)', fontsize=12)
plt.gca().invert_yaxis() # Invertimos el eje Y para que parezca una suspensión vista desde el lado
plt.grid(True, linestyle=':', alpha=0.7)
plt.tight_layout()

# Mostrar la gráfica
plt.show()



# =====================================================================
# Gráficos de Convergencia
# =====================================================================
plt.figure(figsize=(10, 6))
plt.plot(np.arange(1, N_simulaciones + 1), probabilidad_acumulada, color='crimson', alpha=0.8, linewidth=1.5)
plt.axhline(y=prob_falla_final, color='black', linestyle='--', label=f'Convergencia: {prob_falla_final*100:.2f}%')
plt.title('Convergencia de Monte Carlo: Probabilidad de Falla en Hoja de Muelle', fontsize=14, fontweight='bold')
plt.xlabel('Número de Simulaciones (N)', fontsize=12)
plt.ylabel('Probabilidad Acumulada de Falla', fontsize=12)
plt.xscale('log') # Escala logarítmica para visualizar mejor la fluctuación inicial
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
