import time

import matplotlib.pyplot as plt


class Utils:
    """
    Clase de utilidades para visualización y análisis de caminatas aleatorias.

    Proporciona métodos estáticos para graficar trayectorias, distribuciones
    de posiciones finales y medir métricas de rendimiento de las simulaciones.

    Methods
    -------
    graficar_trayectorias(x, y)
        Grafica la trayectoria completa de una caminata aleatoria en 2D.

    graficar_histograma(posiciones_finales)
        Grafica la distribución espacial de posiciones finales de múltiples
        caminatas aleatorias usando scatter plots.

    metricas(funcion, *args, **kwargs)
        Mide y muestra el tiempo de ejecución y consumo de memoria de una
        función específica (ejecutar_simulacion() del main.py).

    Notes
    -----
    Todos los métodos son estáticos y no requieren instanciar la clase.
    """

    @staticmethod
    def graficar_trayectorias(x, y):
        """
        Graficar la trayectoria de una caminata aleatoria en una dimensión.

        Crea un gráfico de línea con marcadores mostrando la evolución de
        la posición a lo largo de las iteraciones. Marca el punto de inicio
        y el punto final con colores distintivos.

        Parameters
        ----------
        x : list or array-like
            Secuencia de iteraciones (números de paso).
        y : list or array-like
            Secuencia de posiciones correspondientes a cada iteración.

        Returns
        -------
        None
            Muestra la gráfica en pantalla de manera no bloqueante.

        Notes
        -----
        - El punto de inicio se marca en verde
        - El punto final se marca en rojo
        - La trayectoria completa se muestra en naranja
        """
        plt.figure(figsize=(10, 7))

        # Dibujar la trayectoria completa
        plt.plot(
            x,
            y,
            "o-",
            color="orange",
            linewidth=1.5,
            markersize=4,
            alpha=0.7,
            label="Trayectoria",
        )

        # Marcar el INICIO (punto verde)
        plt.scatter(
            [x[0]],
            [y[0]],
            s=75,
            color="green",
            marker="o",
            edgecolors="black",
            linewidths=2,
            zorder=5,
            label=f"Inicio ({x[0]}, {y[0]})",
        )

        # Marcar el FINAL (punto rojo)
        plt.scatter(
            [x[-1]],
            [y[-1]],
            s=75,
            color="red",
            marker="s",
            edgecolors="black",
            linewidths=2,
            zorder=5,
            label=f"Final ({x[-1]}, {y[-1]})",
        )

        # Líneas de referencia
        plt.axhline(y=0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
        plt.axvline(x=0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)

        plt.title("Trayectoria de la Caminata Aleatoria en 2D", fontsize=14)
        plt.xlabel("Iteración", fontsize=12)
        plt.ylabel("Posición", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(loc="best")
        plt.tight_layout()
        plt.show(block=False)

    def graficar_histograma(posiciones_finales):
        from collections import Counter

        """
        Graficar la distribución espacial de posiciones finales en 2D.
        """
        # 1. Contar cuántas veces aparece cada coordenada
        frecuencias = Counter(posiciones_finales)

        # 2. Separar las coordenadas X, Y y obtener las frecuencias para el tamaño
        coords = list(frecuencias.keys())
        x = [c[0] for c in coords]
        y = [c[1] for c in coords]
        # Multiplicamos la frecuencia por un factor (ej. 50) para que el punto sea visible
        tamaños = [f * 50 for f in frecuencias.values()]

        plt.figure(figsize=(10, 10))

        # 3. Crear el gráfico de dispersión
        # c puede ser un color fijo o basado en la frecuencia para un mapa de calor
        plt.scatter(x, y, s=tamaños, alpha=0.6, edgecolors="blue", c="skyblue")

        # Líneas de origen
        plt.axhline(y=0, color="black", linewidth=0.8)
        plt.axvline(x=0, color="black", linewidth=0.8)

        plt.title("Distribución de Posiciones Finales")
        plt.xlabel("Posición X")
        plt.ylabel("Posición Y")

        plt.grid(True, alpha=0.3)
        plt.axis("equal")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def graficar_heatmap(posiciones_finales):
        """
        Crea un mapa de calor basado en la densidad de las posiciones finales.
        """
        # Extraer x e y de la lista de tuplas
        x = [p[0] for p in posiciones_finales]
        y = [p[1] for p in posiciones_finales]

        plt.figure(figsize=(10, 8))

        # cmap="hot" o "viridis" son excelentes para densidad
        # bins define la "resolución" de la cuadrícula
        counts, xedges, yedges, im = plt.hist2d(x, y, bins=30, cmap="hot")

        # Añadir barra de color para referencia de frecuencia
        plt.colorbar(im, label="Frecuencia de Ranas")

        plt.axhline(y=0, color="white", linewidth=0.8, linestyle="--", alpha=0.5)
        plt.axvline(x=0, color="white", linewidth=0.8, linestyle="--", alpha=0.5)

        plt.title("Mapa de Calor: Concentración de Posiciones Finales Rana Feliz 2D")
        plt.xlabel("Posición X")
        plt.ylabel("Posición Y")

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

        print(
            f"Tiempo de ejecución: {end_time - start_time:.4f} segundos. Equivalente en minutos: {(end_time - start_time) / 60:.2f} minutos"
        )
        print(
            f"Memoria utilizada: {current / 10**6:.4f} MB; Pico de memoria: {peak / 10**6:.4f} MB"
        )

        return resultado
