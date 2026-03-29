import sys
import time
from pathlib import Path

from utils import Utils

sys.path.insert(0, str(Path(__file__).parent.parent))

# Agregar ruta para importar desde generadores_numeros_pseudoaleatorios
generador_path = (
    Path(__file__).parent.parent.parent / "generadores_numeros_pseudoaleatorios"
)
sys.path.insert(0, str(generador_path))

from generador_numeros.congruencia_lineal import GeneradorCongruenciaLineal
from validadores.prueba_chi_cuadrado import PruebaChiCuadrado
from validadores.prueba_kolmogorov_smirnov import PruebaKolmogorovSmirnov
from validadores.prueba_medias import PruebaMedias
from validadores.prueba_poker import PruebaPoker
from validadores.prueba_rachas import PruebaRachas
from validadores.prueba_varianza import PruebaVarianza


def caminata(semilla: int, pasos: int):
    """
    Realiza una caminata aleatoria en dos dimensiones.

    En cada paso, la rana se mueve en una de cuatro direcciones con probabilidad
    0.25 cada una, según el valor generado por el generador de números pseudoaleatorios:
    - [0.00, 0.25): Movimiento a la izquierda (-1, 0)
    - [0.25, 0.50): Movimiento a la derecha (+1, 0)
    - [0.50, 0.75): Movimiento arriba (0, +1)
    - [0.75, 1.00]: Movimiento abajo (0, -1)

    Parameters
    ----------
    semilla : int
        Semilla inicial para el generador de números pseudoaleatorios.
        Determina la secuencia de movimientos de manera reproducible.
    pasos : int
        Número de pasos (movimientos) a simular en la caminata.

    Returns
    -------
    tuple of (list, list)
        Tupla con dos listas:
        - trayectoria_x: Lista de posiciones en el eje X incluyendo la inicial
        - trayectoria_y: Lista de posiciones en el eje Y incluyendo la inicial
    """
    generador = GeneradorCongruenciaLineal(semilla)

    x_actual = 0
    y_actual = 0

    trayectoria_x = [x_actual]
    trayectoria_y = [y_actual]

    numeros_aleatorios = generador.siguiente_Ri_Congruencia_Lineal(pasos)

    for siguiente_Ri in numeros_aleatorios:
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
    Ejecuta múltiples caminatas aleatorias independientes en 2D y analiza los resultados.

    Realiza varias simulaciones de caminatas aleatorias en dos dimensiones,
    cada una con una semilla diferente, y genera visualizaciones de los resultados
    incluyendo scatter plot y heatmap de frecuencias.

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
        La función muestra gráficas y imprime resultados en consola.

    Notes
    -----
    - Genera un scatter plot 2D con distribución espacial de posiciones finales
    - Genera un mapa de calor (heatmap) con la densidad de frecuencias
    - Calcula la probabilidad de retornar al origen en el paso específico
    - Cada simulación utiliza semilla diferente para garantizar independencia
    - Grafica la trayectoria de la última simulación completada
    """
    print("Iniciando simulaciones de caminata aleatoria en 2D...")

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

    Utils.graficar_scatter_plot(posiciones_finales, pasos_por_simulacion)
    Utils.graficar_heatmap(posiciones_finales, pasos_por_simulacion)

    show_p = calcular_probabilidad(posiciones_en_paso_objetivo, paso_objetivo)
    print(show_p)


def calcular_probabilidad(posiciones, paso_objetivo):
    """
    Calcula la probabilidad de estar en el origen en un paso específico de 2D.

    Cuenta cuántas simulaciones terminaron en el origen (0, 0) en un paso específico
    y calcula la probabilidad empírica.

    Parameters
    ----------
    posiciones : list of tuple
        Lista de tuplas (x, y) representando posiciones en un paso específico
        de múltiples caminatas aleatorias.
    paso_objetivo : int
        Índice del paso a analizar para calcular la probabilidad.

    Returns
    -------
    str
        Mensaje formateado con la probabilidad calculada con 4 decimales.
    """
    contador = sum(1 for coordenada in posiciones if coordenada == (0, 0))

    probabilidad = contador / len(posiciones)

    return f"Probabilidad de estar en (0, 0) en el paso {paso_objetivo}: {probabilidad:.4f}"


if __name__ == "__main__":
    numero_de_simulaciones = 100
    pasos_por_simulacion = 1000000
    paso_objetivo_para_probabilidad = 1000

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
        prueba_medias = PruebaMedias()
        prueba_varianza = PruebaVarianza()
        prueba_chi_cuadrado = PruebaChiCuadrado()
        prueba_ks = PruebaKolmogorovSmirnov()
        prueba_poker = PruebaPoker()
        prueba_rachas = PruebaRachas()

        print("\n:::::: Prueba de Medias ::::::")
        valida_medias = prueba_medias.prueba_medias(numeros_prueba)

        print("\n:::::: Prueba de Varianza ::::::")
        valida_varianza = prueba_varianza.prueba_varianza(numeros_prueba)

        print("\n:::::: Prueba de chi-cuadrado ::::::")
        valida_uniformidad = prueba_chi_cuadrado.prueba_chi_cuadrado(
            numeros_prueba, pasos_por_simulacion
        )

        print("\n:::::: Prueba de Kolmogorov-Smirnov ::::::")
        valida_uniformidad_ks = prueba_ks.prueba_kolmogorov_smirnov(numeros_prueba)

        print("\n:::::: Prueba de Poker ::::::")
        valida_poker = prueba_poker.prueba_poker(numeros_prueba)

        print("\n:::::: Prueba de Rachas ::::::")
        valida_rachas = prueba_rachas.prueba_rachas(numeros_prueba)

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
                print("  - La prueba de chi-cuadrado FALLÓ")
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
