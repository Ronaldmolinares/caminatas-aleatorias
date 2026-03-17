import sys
import time
from pathlib import Path

from utils import Utils

sys.path.insert(0, str(Path(__file__).parent.parent))
from generador_numeros.congruencia_lineal import GeneradorCongruenciaLineal
from validacion_numeros.aleatoriedad import RandomnessTest
from validacion_numeros.no_correlacion_serial import PruebaNoCorrelacionSerial
from validacion_numeros.uniformidad import PruebaUniformidad


def caminata(semilla: int, pasos: int):
    generador = GeneradorCongruenciaLineal(semilla)

    x_actual = 0
    y_actual = 0
    z_actual = 0

    trayectoria_x = [x_actual]
    trayectoria_y = [y_actual]
    trayectoria_z = [z_actual]

    numeros_aleatorios = generador.siguiente_Ri_Congruencia_Lineal(pasos)

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
    print("Iniciando simulaciones de caminata aleatoria en 3D...")
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
    numero_de_simulaciones = 100
    pasos_por_simulacion = 1000000
    paso_objetivo_para_probabilidad = 4

    validacion_exitosa = False

    while not validacion_exitosa:
        # Generar semilla
        semilla_base = int(time.time() * 1000000) % (2**32 - 1)

        print("=" * 50)
        print("Pruebas sobre números Pseudoaleatorios")
        print("=" * 50)

        # Crear generador de prueba
        gen_prueba = GeneradorCongruenciaLineal(semilla_base)
        numeros_prueba = gen_prueba.siguiente_Ri_Congruencia_Lineal(50000)

        # Validar propiedades
        aleatoriedad = RandomnessTest()
        uniformidad = PruebaUniformidad()
        no_correlacion_serial = PruebaNoCorrelacionSerial()

        print("\n:::::: Prueba de Medias ::::::")
        valida_medias = aleatoriedad.prueba_medias(numeros_prueba)

        print("\n:::::: Prueba de Varianza ::::::")
        valida_varianza = aleatoriedad.prueba_varianza(numeros_prueba)

        print("\n:::::: Prueba de chi-cuadrado ::::::")
        valida_uniformidad = uniformidad.prueba_chi_cuadrado(numeros_prueba)

        print("\n:::::: Prueba de Kolmogorov-Smirnov ::::::")
        valida_uniformidad_ks = uniformidad.prueba_kolmogorov_smirnov(numeros_prueba)

        print("\n:::::: Prueba de Poker ::::::")
        valida_poker = no_correlacion_serial.prueba_poker(numeros_prueba)

        print("\n:::::: Prueba de Rachas ::::::")
        valida_rachas = no_correlacion_serial.prueba_rachas(numeros_prueba)

        print("\n" + "=" * 50)
        if (
            valida_medias
            and valida_varianza
            and valida_uniformidad
            and valida_uniformidad_ks
            and valida_poker
            and valida_rachas
        ):
            print("Números pseudoaleatorios válidos.")
            print("=" * 50 + "\n")
            validacion_exitosa = True

            # Ejecutar simulaciones
            Utils.metricas(
                ejecutar_simulacion,
                numero_de_simulaciones,
                semilla_base,
                pasos_por_simulacion,
                paso_objetivo_para_probabilidad,
            )
        else:
            print("Números pseudoaleatorios NO válidos.")
            if not valida_medias:
                print("  - La prueba de medias FALLÓ")
            if not valida_varianza:
                print("  - La prueba de varianza FALLÓ")
            if not valida_uniformidad:
                print("  - La prueba de uniformidad FALLÓ")
            if not valida_uniformidad_ks:
                print("  - La prueba de Kolmogorov-Smirnov FALLÓ")
            if not valida_poker:
                print("  - La prueba de Poker FALLÓ")
            if not valida_rachas:
                print("  - La prueba de Rachas FALLÓ")
            print("=" * 50)

            # Preguntar al usuario
            print("\nOpciones:")
            print("1. Reintentar con otra semilla")
            print("2. Salir")

            opcion = input("\nElige una opción (1-2): ")
            if opcion == "1":
                print("Reintentando con una nueva semilla...\n")

            else:
                print("Simulación cancelada.")
                break
