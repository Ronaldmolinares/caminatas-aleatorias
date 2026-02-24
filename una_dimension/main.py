import time

from generador import GeneradorCongruenciaLineal
from utils import Utils


def caminata(semilla: int, pasos: int):
    generador = GeneradorCongruenciaLineal(semilla)
    lista_Ri = generador.generar_Ri(pasos)

    iteraciones = [0]
    posicion_actual = 0
    historial_pasos = [posicion_actual]

    for num in range(len(lista_Ri)):
        if lista_Ri[num] < 0.5:
            posicion_actual -= 1
        else:
            posicion_actual += 1

        historial_pasos.append(posicion_actual)
        iteraciones.append(num + 1)

    return historial_pasos
    # return historial_pasos, iteraciones


def ejecutar_simulacion(numero_intentos, semilla):
    posiciones_finales = []
    lista = []

    for i in range(numero_intentos):
        # Usar una semilla diferente en cada iteración
        semilla_actual = semilla + i
        historial_pasos = caminata(semilla_actual, 1000000)
        lista.append(historial_pasos)
        # Utils.graficar_trayectorias(iteraciones, historial_pasos)

        posiciones_finales.append(historial_pasos[-1])

    Utils.graficar_histograma(posiciones_finales)

    show_p = calcular_probabilidad(lista, 4)
    print(show_p)


def calcular_probabilidad(lista_historiales, paso_objetivo):
    contador = 0
    for sublista in lista_historiales:
        if sublista[paso_objetivo] == 0:
            contador += 1

    probabilidad = contador / len(lista_historiales)

    return f"Probabilidad de que en el paso {paso_objetivo} la posición sea 0: {probabilidad}"


if __name__ == "__main__":
    semilla = int(time.time() * 1000000) % (2**32 - 1)
    Utils.metricas(ejecutar_simulacion, 100, semilla)
