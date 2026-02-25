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

    # return (trayectoria_x, trayectoria_y)
    return list(zip(trayectoria_x, trayectoria_y))


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
    trayectorias = []  # Guardar trayectorias completas

    for i in range(numero_simulaciones):
        # Usar una semilla diferente en cada iteración
        semilla_actual = semilla + i

        trayectoria = caminata(semilla_actual, pasos_por_simulacion)

        trayectorias.append(trayectoria)

        posiciones_finales.append(trayectoria[-1])

        print(
            f"Simulación {i + 1}/{numero_simulaciones} completada. Posición final: {trayectoria[-1]}"
        )

    # Graficar la trayectoria de la última caminata simulada
    x, y = zip(*trayectorias[-1])
    Utils.graficar_trayectorias(x, y)

    Utils.graficar_histograma(posiciones_finales)
    Utils.graficar_heatmap(posiciones_finales)

    show_p = calcular_probabilidad(trayectorias, paso_objetivo)
    print(show_p)


def calcular_probabilidad(trayectorias, paso_objetivo):
    """Verifica si en el paso específico la rana estaba en el origen (0, 0)"""

    contador = sum(
        1 for t in trayectorias if len(t) > paso_objetivo and t[paso_objetivo] == (0, 0)
    )

    probabilidad = contador / len(trayectorias)

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
