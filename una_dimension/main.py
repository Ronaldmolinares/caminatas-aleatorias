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

    posicion_actual = 0
    historial_posiciones = [posicion_actual]

    numeros_aleatorios = generador.siguiente_Ri(pasos)
    for numero_aleatorio in numeros_aleatorios:
        if numero_aleatorio < 0.5:
            posicion_actual -= 1  # Movimiento a la izquierda
        else:
            posicion_actual += 1  # Movimiento a la derecha
        historial_posiciones.append(posicion_actual)

    return historial_posiciones


def ejecutar_simulacion(
    numero_simulaciones, semilla_base, pasos_por_simulacion, paso_objetivo
):
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
    pasos_por_simulacion : int
        Número de pasos a simular en cada caminata aleatoria.
    paso_objetivo : int
        Paso para calcular la probabilidad de estar en el origen (0) en ese paso.

    Returns
    -------
    None
        La función muestra gráficas y imprime resultados.

    Notes
    -----
    - Genera un histograma de las posiciones finales de todas las simulaciones
    - Calcula la probabilidad de retornar al origen en el paso específico (por ejemplo, paso 4).
    - Cada simulación realiza `pasos_por_simulacion` de pasos
    """
    posiciones_finales = []
    posiciones_en_paso_objetivo = []

    print("Iniciando simulaciones de caminata aleatoria en 1D...")

    for i in range(numero_simulaciones):
        # Usar una semilla diferente en cada iteración para independencia
        semilla_actual = semilla_base + i

        historial_posiciones = caminata(semilla_actual, pasos_por_simulacion)

        posiciones_finales.append(historial_posiciones[-1])

        posiciones_en_paso_objetivo.append(historial_posiciones[paso_objetivo])

        if (i + 1) % 10 == 0 or i == numero_simulaciones - 1:
            print(f"Ejecutando simulación {i + 1}/{numero_simulaciones}")

        if i == numero_de_simulaciones - 1:
            # Graficar la trayectoria de la última caminata simulada
            Utils.graficar_trayectorias(
                list(range(len(historial_posiciones))), historial_posiciones
            )

    # Graficar el histograma de posiciones finales
    Utils.graficar_histograma(posiciones_finales)

    # Calcular y mostrar la probabilidad de estar en el origen en el paso 𝓷
    probabilidad_origen = calcular_probabilidad(
        posiciones_en_paso_objetivo, paso_objetivo
    )
    print(probabilidad_origen)


def calcular_probabilidad(posiciones, paso_especifico):
    """
    Calcula la probabilidad de estar en el origen en un paso específico.

    Parameters
    ----------
    posiciones : list of int
        Lista de posiciones finales en un paso específico de múltiples caminatas aleatorias.
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
    conteo_en_origen = sum(1 for punto in posiciones if punto == 0)

    probabilidad = conteo_en_origen / len(posiciones)

    return f"Probabilidad de que en el paso {paso_especifico} la rana este en el origen: {probabilidad}"


if __name__ == "__main__":
    # Generar semilla única basada en el tiempo actual
    semilla_base = int(time.time() * 1000000) % (2**32 - 1)

    numero_de_simulaciones = 100
    pasos_por_simulacion = 1000000
    paso_objetivo_para_probabilidad = 4

    # Ejecutar simulaciones
    Utils.metricas(
        ejecutar_simulacion,
        numero_de_simulaciones,
        semilla_base,
        pasos_por_simulacion,
        paso_objetivo_para_probabilidad,
    )
