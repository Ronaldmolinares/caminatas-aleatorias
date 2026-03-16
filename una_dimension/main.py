import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from generador import GeneradorCongruenciaLineal
from utils import Utils

from validacion_numeros.aleatoriedad import RandomnessTest
from validacion_numeros.no_correlacion_serial import PruebaNoCorrelacionSerial
from validacion_numeros.uniformidad import PruebaUniformidad


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

        if i == numero_simulaciones - 1:
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
        numeros_prueba = gen_prueba.siguiente_Ri(50000)

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
