import time

import matplotlib.pyplot as plt
import numpy as np


class Utils:
    """
    Clase de utilidades para visualización y análisis de caminatas aleatorias.

    Proporciona métodos estáticos para graficar trayectorias individuales,
    distribuciones de posiciones finales y medir métricas de rendimiento
    (tiempo y memoria) de las simulaciones.

    Methods
    -------
    graficar_trayectorias(x, y)
        Grafica la trayectoria completa de una caminata aleatoria en 1D.

    graficar_histograma(posiciones_finales)
        Genera un histograma de las posiciones finales de múltiples
        caminatas aleatorias.

    metricas(funcion, *args)
        Mide y muestra el tiempo de ejecución y consumo de memoria de una
        función específica.

    Notes
    -----
    Todos los métodos son estáticos y no requieren instanciar la clase.
    Se pueden llamar directamente como Utils.metodo().
    """

    @staticmethod
    def graficar_trayectorias(x, y):
        """
        Graficar la trayectoria de una caminata aleatoria en una dimensión.

        Parameters
        ----------
        x : list or array-like
            Secuencia de iteraciones (números de paso).
        y : list or array-like
            Secuencia de posiciones correspondientes a cada iteración.

        """
        plt.figure(figsize=(7, 7))
        plt.plot(x, y, "o-", color="orange", linewidth=1.5, markersize=4)
        plt.axhline(y=0, color="black", linewidth=0.8)  # Línea horizontal en y=0
        plt.axvline(x=0, color="black", linewidth=0.8)  # Línea vertical en x=0
        plt.title("Grafica de movimientos de la Rana Feliz en 1D")
        plt.xlabel("Iteracion")
        plt.ylabel("Movimiento")
        plt.grid(True, alpha=0.3)
        plt.show(block=False)

    @staticmethod
    def graficar_histograma(posiciones_finales):
        """
        Generar un histograma de las posiciones finales de múltiples caminatas.


        Parameters
        ----------
        posiciones_finales : list of int
            Lista con las posiciones finales de cada caminata aleatoria.

        """

        plt.figure(figsize=(8, 6))
        bins = int(np.sqrt(len(posiciones_finales)))

        plt.hist(
            posiciones_finales,
            bins=bins,
            color="blue",
            alpha=0.7,
            edgecolor="black",
            rwidth=0.5,
        )
        plt.title("Histograma de posiciones finales de la Rana Feliz en 1D")
        plt.xlabel("Posición Final")
        plt.ylabel("Frecuencia")
        plt.grid(True, alpha=0.2, axis="y")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def metricas(funcion, *args):
        """
        Medir tiempo de ejecución y consumo de memoria (en MB) de una función.

        Parameters
        ----------
        funcion : callable
            Función a ejecutar y medir.
        *args
            Argumentos posicionales a pasar a la función.

        """
        import tracemalloc

        tracemalloc.start()

        start_time = time.time()
        resultado = funcion(*args)
        end_time = time.time()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(
            f"Tiempo de ejecución: {end_time - start_time:.4f} segundos. Equivalente en minutos: {(end_time - start_time) / 60:.2f} minutos"
        )
        print(
            f"Memoria utilizada: {current / 10**6:.4f} MB; Pico de memoria: {peak / 10**6:.4f} MB"
        )

        return resultado
