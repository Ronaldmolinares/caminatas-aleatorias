import time

from generador import GeneradorCongruenciaLineal
from utils import Utils


def caminata(semilla: int, pasos: int, min: int, max: int):
    generador = GeneradorCongruenciaLineal(semilla)
    lista_Ri = generador.generar_Ni(pasos, min, max)

    iteraciones = []
    posicion_actual = 0
    historial_pasos = []

    for num in range(len(lista_Ri)):
        if lista_Ri[num] < 0.5:
            posicion_actual -= 1
        else:
            posicion_actual += 1

        historial_pasos.append(posicion_actual)
        iteraciones.append(num)

    return historial_pasos, iteraciones


def ejecutar_simulacion(numero_intentos, semilla):
    posiciones_finales = []

    for i in range(numero_intentos):
        # Usar una semilla diferente en cada iteración
        semilla_actual = semilla + i
        historial_pasos, iteraciones = caminata(semilla_actual, 50, 10, 20)

        Utils.graficar_trayectorias(iteraciones, historial_pasos)

        posiciones_finales.append(historial_pasos[-1])
    print(posiciones_finales)
    Utils.graficar_histograma(posiciones_finales)


if __name__ == "__main__":
    semilla = int(time.time() * 1000000) % (2**32 - 1)
    ejecutar_simulacion(5, semilla)
