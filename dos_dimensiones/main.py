import time

from generador import GeneradorCongruenciaLineal
from utils import Utils


def caminata(semilla: int, pasos: int):
    generador = GeneradorCongruenciaLineal(semilla)

    x_actual = 0
    y_actual = 0

    trayectoria_x = [x_actual]
    trayectoria_y = [y_actual]

    for _ in range(pasos):
        siguiente_Ri = generador.siguiente_Ri()
        if siguiente_Ri <= 0.25:
            x_actual -= 1  # izquierda
        elif siguiente_Ri <= 0.5:
            x_actual += 1  # derecha
        elif siguiente_Ri <= 0.75:
            y_actual += 1  # arriba
        else:
            y_actual -= 1  # abajo

        trayectoria_x.append(x_actual)
        trayectoria_y.append(y_actual)

    return (trayectoria_x, trayectoria_y)


def ejecutar_simulacion(
    numero_simulaciones, semilla, pasos_por_simulacion, paso_objetivo
):
    """
    Ejecuta múltiples caminatas aleatorias independientes y analiza los resultados.

    Parameters
    ----------
    numero_simulaciones : int
        Cantidad de caminatas aleatorias independientes a simular.
    semilla : int
        Semilla base para generar secuencias de números pseudoaleatorios.
        Se incrementará en cada simulación para obtener secuencias diferentes.
    pasos_por_simulacion : int
        Número de pasos a simular en cada caminata aleatoria.
    paso_objetivo : int
        Paso para calcular la probabilidad de estar en el origen (0, 0) en ese paso.

    Returns
    -------
    None
    """
    posiciones_finales = []
    posiciones_en_paso_objetivo = []  # Guardar paso especifico para calcular probabilidad

    for i in range(numero_simulaciones):
        # Usar una semilla diferente en cada iteración
        semilla_actual = semilla + i

        trayectoria_x, trayectoria_y = caminata(semilla_actual, pasos_por_simulacion)

        posiciones_finales.append((trayectoria_x[-1], trayectoria_y[-1]))
        posiciones_en_paso_objetivo.append(
            (trayectoria_x[paso_objetivo], trayectoria_y[paso_objetivo])
        )

        print(
            f"Simulación {i + 1}/{numero_simulaciones} completada. Posición final: {trayectoria_x[-1], trayectoria_y[-1]}"
        )

        # Graficar la trayectoria de la última caminata simulada
        if i == numero_simulaciones - 1:
            Utils.graficar_trayectorias(trayectoria_x, trayectoria_y)

    Utils.graficar_histograma(posiciones_finales)
    Utils.graficar_heatmap(posiciones_finales)

    show_p = calcular_probabilidad(posiciones_en_paso_objetivo, paso_objetivo)
    print(show_p)


def calcular_probabilidad(posiciones, paso_objetivo):
    """Verifica si en el paso específico la rana estaba en el origen (0, 0)"""

    contador = sum(1 for coordenada in posiciones if coordenada == (0, 0))

    probabilidad = contador / len(posiciones)

    return f"Probabilidad de estar en (0, 0) en el paso {paso_objetivo}: {probabilidad:.4f}"


if __name__ == "__main__":
    # Generar semilla única basada en el tiempo actual
    semilla_base = int(time.time() * 1000000) % (2**32 - 1)

    numero_de_simulaciones = 100
    pasos_por_simulacion = 10000
    paso_objetivo_para_probabilidad = 4

    # Ejecutar simulaciones
    Utils.metricas(
        ejecutar_simulacion,
        numero_de_simulaciones,
        semilla_base,
        pasos_por_simulacion,
        paso_objetivo_para_probabilidad,
    )
