import time

import matplotlib.pyplot as plt


class Utils:
    def graficar_trayectorias(x, y):
        plt.figure(figsize=(7, 7))
        plt.plot(x, y, "o-", color="orange", linewidth=1.5, markersize=4)
        plt.axhline(y=0, color="black", linewidth=0.8)  # Línea horizontal en y=0
        plt.axvline(x=0, color="black", linewidth=0.8)  # Línea vertical en x=0
        plt.title("Grafica de movimientos de la Rana Feliz en 1D")
        plt.xlabel("Iteracion")
        plt.ylabel("Movimiento")
        plt.grid(True, alpha=0.3)
        plt.show()

    def graficar_histograma(posiciones_finales):
        plt.figure(figsize=(7, 7))
        plt.hist(posiciones_finales, bins=20, color="blue", alpha=0.7)
        plt.title("Histograma de posiciones finales de la Rana Feliz")
        plt.xlabel("Posición Final")
        plt.ylabel("Frecuencia")
        plt.grid(True, alpha=0.2)
        plt.show()

    def tiempo_ejecucion(funcion, *args):
        start_time = time.time()
        resultado = funcion(*args)
        end_time = time.time()
        print(f"Tiempo de ejecución: {end_time - start_time:.4f} segundos")
        return resultado

    def memoria_utilizada(funcion, *args):
        import tracemalloc

        tracemalloc.start()
        resultado = funcion(*args)
        current, peak = tracemalloc.get_traced_memory()
        print(
            f"Memoria utilizada: {current / 10**6:.4f} MB; Pico de memoria: {peak / 10**6:.4f} MB"
        )
        tracemalloc.stop()
        return resultado
