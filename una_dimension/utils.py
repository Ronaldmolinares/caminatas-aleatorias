import time

import matplotlib.pyplot as plt


class Utils:
    @staticmethod
    def graficar_trayectorias(x, y):
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
        import numpy as np

        plt.figure(figsize=(7, 7))
        min_pos = int(min(posiciones_finales))
        max_pos = int(max(posiciones_finales))
        bins = np.arange(min_pos - 0.5, max_pos + 1.5, 1)

        plt.hist(
            posiciones_finales, bins=bins, color="blue", alpha=0.7, edgecolor="black"
        )
        plt.title("Histograma de posiciones finales de la Rana Feliz")
        plt.xlabel("Posición Final")
        plt.ylabel("Frecuencia")
        plt.grid(True, alpha=0.2, axis="y")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def metricas(funcion, *args):
        import tracemalloc

        tracemalloc.start()

        start_time = time.time()
        resultado = funcion(*args)
        end_time = time.time()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Tiempo de ejecución: {end_time - start_time:.4f} segundos")
        print(
            f"Memoria utilizada: {current / 10**6:.4f} MB; Pico de memoria: {peak / 10**6:.4f} MB"
        )

        return resultado
