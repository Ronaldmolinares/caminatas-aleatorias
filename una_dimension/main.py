import time

from generador import GeneradorCongruenciaLineal
from utils import Utils


def caminata(semilla: int, pasos: int):
    """
    Realiza una caminata aleatoria en una dimensión.

    En cada paso, la rana se mueve hacia la izquierda (-1) o hacia la
    derecha (+1) con probabilidad 0.5 cada una, según el valor generado
    por el generador de números pseudoaleatorios.

    Parameters
    ----------
    semilla : int
        Semilla inicial para el generador de números pseudoaleatorios.
        Determina la secuencia de movimientos de manera reproducible.
    pasos : int
        Número de pasos (movimientos) a simular en la caminata.

    Returns
    -------
    list of int
        Lista con las posiciones de la rana en cada paso, incluyendo
        la posición inicial (0).

    """
    # Crear un nuevo generador con esta semilla específica
    generador = GeneradorCongruenciaLineal(semilla)

    # Generar los números aleatorios necesarios
    secuencia_Ri = generador.generar_Ri(pasos)

    posicion_actual = 0
    historial_posiciones = [posicion_actual]

    for numero_aleatorio in secuencia_Ri:
        if numero_aleatorio < 0.5:
            posicion_actual -= 1  # Movimiento a la izquierda
        else:
            posicion_actual += 1  # Movimiento a la derecha
        historial_posiciones.append(posicion_actual)

    return historial_posiciones


def ejecutar_simulacion(numero_simulaciones, semilla_base, pasos_por_simulacion):
    """
    Ejecuta múltiples caminatas aleatorias independientes y analiza los resultados.

    Realiza varias simulaciones de caminatas aleatorias, cada una con una semilla
    diferente (semilla_base + i), y genera un histograma de las posiciones finales.
    También calcula la probabilidad de estar en el origen en un paso específico.

    Parameters
    ----------
    numero_simulaciones : int
        Cantidad de caminatas aleatorias independientes a simular.
    semilla_base : int
        Semilla inicial. Cada simulación usará semilla_base + i donde i es el
        índice de la simulación (0, 1, 2, ..., numero_simulaciones-1).

    Returns
    -------
    None
        La función muestra gráficas y imprime resultados.

    Notes
    -----
    - Genera un histograma de las posiciones finales de todas las simulaciones
    - Calcula la probabilidad de retornar al origen en el paso específico (por ejemplo, paso 4).
    - Cada simulación realiza 1,000,000 de pasos
    """
    posiciones_finales = []
    historiales_completos = []

    for i in range(numero_simulaciones):
        # Usar una semilla diferente en cada iteración para independencia
        semilla_actual = semilla_base + i

        # Cada llamada a caminata() crea su propio generador interno
        historial_posiciones = caminata(semilla_actual, pasos_por_simulacion)

        historiales_completos.append(historial_posiciones)
        posiciones_finales.append(historial_posiciones[-1])

    # Graficar el histograma de posiciones finales
    Utils.graficar_histograma(posiciones_finales)

    # Calcular y mostrar la probabilidad de estar en el origen en el paso 𝓷
    probabilidad_origen = calcular_probabilidad(historiales_completos, 4)
    print(probabilidad_origen)


def calcular_probabilidad(historiales, paso_especifico):
    """
    Calcula la probabilidad de estar en el origen en un paso específico.

    Analiza múltiples historiales de caminatas aleatorias y determina qué
    proporción de ellas se encontraban en la posición 0 (origen) en un paso dado.

    Parameters
    ----------
    historiales : list of list of int
        Lista de historiales de posiciones. Cada historial es una lista de
        posiciones en cada paso de una caminata aleatoria.
    paso_especifico : int
        Índice del paso a analizar (0 = posición inicial, 1 = primer paso, etc.).

    Returns
    -------
    str
        Mensaje formateado con la probabilidad calculada.

    Notes
    -----
    Si el paso_especifico excede la longitud de algún historial, ese historial
    será ignorado al acceder al índice.
    """
    conteo_en_origen = 0

    for historial in historiales:
        if historial[paso_especifico] == 0:
            conteo_en_origen += 1

    probabilidad = conteo_en_origen / len(historiales)

    return f"Probabilidad de que en el paso {paso_especifico} la rana este en el origen: {probabilidad}"


if __name__ == "__main__":
    # Generar semilla única basada en el tiempo actual
    semilla_inicial = int(time.time() * 1000000) % (2**32 - 1)

    # Ejecutar 100 simulaciones dando en cada una 1,000,000 de pasos y medir métricas de rendimiento
    Utils.metricas(ejecutar_simulacion, 100, semilla_inicial, 1000000)
