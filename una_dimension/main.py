from generador import GeneradorCongruenciaLineal


def caminata(semilla: int, pasos: int, min: int, max: int):
    generador = GeneradorCongruenciaLineal(semilla)
    lista_Ni, lista_Ri = generador.generar_Ni(pasos, min, max)

    for num in lista_Ri:
        if num < 0.5:
            print("Derecha")
        else:
            print("Izquierda")


if __name__ == "__main__":
    caminata(1024, 10, 10, 20)
