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
        plt.xlabel("Posición X", fontsize=12)
        plt.ylabel("Posición Y", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(loc="best")
        plt.tight_layout()
        plt.show(block=False)

    @staticmethod
    def graficar_scatter_plot(posiciones_finales, n_pasos):
        from collections import Counter

        import matplotlib.pyplot as plt
        import numpy as np

        # 1. Procesar datos
        frecuencias = Counter(posiciones_finales)
        coords = list(frecuencias.keys())
        x = np.array([c[0] for c in coords])
        y = np.array([c[1] for c in coords])

        # Calculamos la distancia al origen para el mapa de colores
        distancias = np.sqrt(x**2 + y**2)
        tamaños = [f * 50 for f in frecuencias.values()]

        plt.figure(figsize=(10, 10))

        # 2. Crear el gráfico con gradiente (cmap) según la distancia
        # 'viridis' o 'plasma' para resaltar la dispersión
        scatter = plt.scatter(
            x, y, s=tamaños, alpha=0.7, c=distancias, cmap="viridis", edgecolors="none"
        )

        # Añadir barra de color para entender las distancias
        cbar = plt.colorbar(scatter)
        cbar.set_label("Distancia Euclídeana al Origen")

        # 3. Dibujar el círculo de la "Distancia Típica" (Raíz de N)
        distancia_esperada = np.sqrt(n_pasos)
        circulo = plt.Circle(
            (0, 0),
            distancia_esperada,
            color="red",
            fill=False,
            linestyle="--",
            linewidth=2,
            label=f"Distancia esperada (√n ≈ {distancia_esperada:,})",
        )
        plt.gca().add_patch(circulo)

        # 4. Marcar el origen con un punto destacado
        plt.scatter(0, 0, color="red", marker="+", s=200, label="Origen (0,0)")

        # Estética y ejes
        plt.axhline(y=0, color="black", linewidth=1, alpha=0.5)
        plt.axvline(x=0, color="black", linewidth=1, alpha=0.5)

        plt.title(
            f"Distribución Espacial tras {n_pasos:,} pasos en Caminata Aleatoria 2D",
            fontsize=14,
        )
        plt.xlabel("Posición X")
        plt.ylabel("Posición Y")
        plt.legend(loc="upper right")
        plt.grid(True, alpha=0.3)
        plt.axis("equal")

        plt.tight_layout()
        plt.show()

    @staticmethod
    def graficar_heatmap(posiciones_finales, n_pasos):
        import numpy as np

        # 1. Extraer coordenadas
        x = [p[0] for p in posiciones_finales]
        y = [p[1] for p in posiciones_finales]

        plt.figure(figsize=(11, 8))

        # 2. Aumentar BINS para mejor resolución
        counts, xedges, yedges, im = plt.hist2d(
            x,
            y,
            bins=60,  # Mayor resolución (cuadros más pequeños)
            cmap="hot",  # 'inferno' o 'magma' 'hot'
        )

        # 3. Añadir barra de color
        plt.colorbar(im, label="Frecuencia de Ranas")

        # 4. Superponer el círculo de la "Distancia Típica" (√n)
        distancia_esperada = np.sqrt(n_pasos)
        circulo = plt.Circle(
            (0, 0),
            distancia_esperada,
            color="cyan",
            fill=False,
            linestyle="--",
            linewidth=2,
            label=f"Radio esperado (√n ≈ {distancia_esperada:,})",
        )
        plt.gca().add_patch(circulo)

        # Ejes de origen centrados
        plt.axhline(y=0, color="white", linewidth=0.8, linestyle="--", alpha=0.5)
        plt.axvline(x=0, color="white", linewidth=0.8, linestyle="--", alpha=0.5)

        plt.title(
            f"Mapa de Calor: Densidad de Probabilidad ({n_pasos:,} pasos)", fontsize=14
        )
        plt.xlabel("Posición X")
        plt.ylabel("Posición Y")
        plt.legend(
            loc="upper right", facecolor="black", labelcolor="white"
        )  # Leyenda visible sobre fondo oscuro
        plt.axis("equal")
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
