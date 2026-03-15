import time

from generador import GeneradorCongruenciaLineal
from utils import Utils


def caminata(semilla: int, pasos: int):
    generador = GeneradorCongruenciaLineal(semilla)

    x_actual = 0
    y_actual = 0
    z_actual = 0

    trayectoria_x = [x_actual]
    trayectoria_y = [y_actual]
    trayectoria_z = [z_actual]

    numeros_aleatorios = generador.siguiente_Ri(pasos)

    for siguiente_Ri in numeros_aleatorios:
        if siguiente_Ri <= 1 / 6:
            x_actual -= 1  # izquierda
        elif siguiente_Ri <= 1 / 3:
            x_actual += 1  # derecha
        elif siguiente_Ri <= 0.5:
            y_actual += 1  # arriba
        elif siguiente_Ri <= 2 / 3:
            y_actual -= 1  # abajo
        elif siguiente_Ri <= 5 / 6:
            z_actual += 1  # adelante
        else:
            z_actual -= 1  # atrás

        trayectoria_x.append(x_actual)
        trayectoria_y.append(y_actual)
        trayectoria_z.append(z_actual)

    return (trayectoria_x, trayectoria_y, trayectoria_z)


def ejecutar_simulacion(
    numero_simulaciones, semilla, pasos_por_simulacion, paso_objetivo
):
    posiciones_finales = []
    posiciones_en_paso_objetivo = []  # Guardar paso especifico para calcular probabilidad

    for i in range(numero_simulaciones):
        semilla_actual = semilla + i
        trayectoria_x, trayectoria_y, trayectoria_z = caminata(
            semilla_actual, pasos_por_simulacion
        )

        # Guardar posición final
        posiciones_finales.append(
            (trayectoria_x[-1], trayectoria_y[-1], trayectoria_z[-1])
        )

        # Guardar posición en el paso objetivo
        if len(trayectoria_x) > paso_objetivo:
            posiciones_en_paso_objetivo.append(
                (
                    trayectoria_x[paso_objetivo],
                    trayectoria_y[paso_objetivo],
                    trayectoria_z[paso_objetivo],
                )
            )

        print(
            f"Simulación {i + 1}/{numero_simulaciones} completada. Posición final: {trayectoria_x[-1], trayectoria_y[-1], trayectoria_z[-1]}"
        )

        # Graficar la trayectoria de la última caminata simulada
        if i == numero_simulaciones - 1:
            Utils.graficar_trayectorias(trayectoria_x, trayectoria_y, trayectoria_z)

    probabilidad_en_origen = sum(
        1 for pos in posiciones_en_paso_objetivo if pos == (0, 0, 0)
    ) / len(posiciones_en_paso_objetivo)

    print(
        f"Probabilidad de estar en el origen (0, 0, 0) en el paso {paso_objetivo}: {probabilidad_en_origen:.4f}"
    )

    Utils.graficar_scatter_3D(posiciones_finales)
    Utils.graficar_proyecciones_ortogonales(trayectoria_x, trayectoria_y, trayectoria_z)


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
