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
        Graficar la trayectoria completa de una caminata aleatoria en 2D.

        Crea un gráfico líneal que visualiza la ruta completa de la rana
        en el espacio 2D, con marcadores para el inicio (verde) y el final (rojo).

        Parameters
        ----------
        x : list or array-like
            Secuencia de posiciones en el eje X de la trayectoria.
        y : list or array-like
            Secuencia de posiciones en el eje Y correspondientes a cada paso.

        Returns
        -------
        None
            Muestra la gráfica en pantalla de manera no bloqueante.

        Notes
        -----
        - El punto de inicio se marca en verde con un círculo
        - El punto final se marca en rojo con un cuadrado
        - Se incluye líneas de referencia en los ejes X=0 e Y=0
        - La trayectoria se dibuja en naranja con opacidad para claridad
        """
        plt.figure(figsize=(10, 7))

        # Dibujar la trayectoria completa en naranja
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

        # Marcar el INICIO (punto verde con círculo)
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

        # Marcar el FINAL (punto rojo con cuadrado)
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

        # Líneas de referencia en los ejes (para ubicación relativa al origen)
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
        """
        Grafica un scatter plot 2D con distribución de posiciones finales.

        Visualiza todas las posiciones finales de las simulaciones en un gráfico 2D,
        con tamaño de puntos proporcional a la frecuencia y color basado en la
        distancia euclídea al origen. Superpone un círculo que representa la
        distancia típica esperada (√n).

        Parameters
        ----------
        posiciones_finales : list of tuple
            Lista de tuplas (x, y) con las posiciones finales de cada simulación.
        n_pasos : int
            Número de pasos realizados en cada simulación. Se usa para calcular
            la distancia esperada y titlar la gráfica.

        Returns
        -------
        None
            Muestra la gráfica en pantalla.

        Notes
        -----
        - El tamaño de cada punto representa cuántas ranas terminaron en esa posición
        - El color (mapa 'viridis') indica la distancia euclídea del punto al origen
        - El círculo rojo punteado representa la distancia típica de √n pasos
        """
        from collections import Counter

        import matplotlib.pyplot as plt
        import numpy as np

        # 1. Procesar datos: contar frecuencias de cada posición final
        frecuencias = Counter(posiciones_finales)
        coords = list(frecuencias.keys())
        x = np.array([c[0] for c in coords])
        y = np.array([c[1] for c in coords])

        # Calculamos la distancia al origen para el mapa de colores
        # (métrica clave para entender la dispersión en 2D)
        distancias = np.sqrt(x**2 + y**2)
        # El tamaño de cada punto es proporcional a su frecuencia
        tamaños = [f * 50 for f in frecuencias.values()]

        plt.figure(figsize=(10, 10))

        # 2. Crear el gráfico con gradiente (cmap) según la distancia
        # 'viridis' permite visualizar fácilmente zonas de mayor/menor dispersión
        scatter = plt.scatter(
            x, y, s=tamaños, alpha=0.7, c=distancias, cmap="viridis", edgecolors="none"
        )

        # Añadir barra de color para entender las distancias al origen
        cbar = plt.colorbar(scatter)
        cbar.set_label("Distancia Euclídeana al Origen")

        # 3. Dibujar el círculo de la "Distancia Típica" (Raíz de N)
        # Según la teoría del límite central, la distancia típica es √n
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
        """
        Grafica un mapa de calor (heatmap) 2D de la densidad de posiciones finales.

        Crea un histograma 2D que muestra la densidad de probabilidad espacial
        de las posiciones finales de todas las simulaciones. Los colores más
        cálidos indican mayor frecuencia de terminación en esa zona.

        Parameters
        ----------
        posiciones_finales : list of tuple
            Lista de tuplas (x, y) con las posiciones finales de cada simulación.
        n_pasos : int
            Número de pasos realizados en cada simulación. Se usa para calcular
            la distancia esperada y titlar la gráfica.

        Returns
        -------
        None
            Muestra la gráfica en pantalla.

        Notes
        -----
        - Usa una paleta 'hot' para visualizar la densidad (colores rojo intenso = alta frecuencia)
        - Superpone un círculo cian que representa la distancia típica √n
        - Mantiene proporciones iguales en ambos ejes para représentación correcta
        """
        import numpy as np

        # 1. Extraer coordenadas X e Y de todas las posiciones finales
        x = [p[0] for p in posiciones_finales]
        y = [p[1] for p in posiciones_finales]

        plt.figure(figsize=(11, 8))

        # 2. Crear histograma 2D con alta resolución (bins=60)
        # Mayor cantidad de bins = mejor resolución, cuadros más pequeños
        # cmap='hot' asigna colores: negro (baja freq) → rojo (alta freq)
        counts, xedges, yedges, im = plt.hist2d(
            x,
            y,
            bins=60,  # Mayor resolución (cuadros más pequeños)
            cmap="hot",  # Paleta de colores: negro → rojo
        )

        # 3. Añadir barra de color para referencia numérica
        plt.colorbar(im, label="Frecuencia de Ranas")

        # 4. Superponer el círculo de la "Distancia Típica" (√n)
        # Según teoría del límite central, la mayoría de puntos estarán
        # a una distancia aproximada de √n del origen
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
        """
        Medir tiempo de ejecución y consumo de memoria de una función.

        Ejecuta una función y registra métricas de rendimiento incluyendo:
        el tiempo total de ejecución y el uso de memoria (actual y pico).

        Parameters
        ----------
        funcion : callable
            Función a ejecutar y medir.
        *args
            Argumentos posicionales a pasar a la función.

        Returns
        -------
        any
            Retorna el resultado de la función ejecutada.

        Notes
        -----
        - El tiempo se muestra en segundos y minutos
        - La memoria se reporta en MB (megabytes)
        - El pico de memoria es el máximo alcanzado durante la ejecución
        - Usa el módulo tracemalloc para análisis preciso de memoria
        """
        import tracemalloc

        # Iniciar el rastreo de memoria
        tracemalloc.start()

        start_time = time.time()
        # Ejecutar la función con los argumentos proporcionados
        resultado = funcion(*args)
        end_time = time.time()

        # Obtener estadísticas de memoria
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Mostrar resultados formateados
        print(
            f"Tiempo de ejecución: {end_time - start_time:.4f} segundos. Equivalente en minutos: {(end_time - start_time) / 60:.2f} minutos"
        )
        print(
            f"Memoria utilizada: {current / 10**6:.4f} MB; Pico de memoria: {peak / 10**6:.4f} MB"
        )

        return resultado
