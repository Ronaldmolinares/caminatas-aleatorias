import time

import matplotlib.pyplot as plt


class Utils:
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

    @staticmethod
    def graficar_trayectorias(trayectoria_x, trayectoria_y, trayectoria_z):

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")

        # Trazar la línea de la trayectoria
        ax.plot(
            trayectoria_x,
            trayectoria_y,
            trayectoria_z,
            marker="o",
            markersize=2,
            alpha=0.6,
        )

        # Marcar el punto inicial (verde)
        ax.scatter(
            trayectoria_x[0],
            trayectoria_y[0],
            trayectoria_z[0],
            color="black",
            s=100,
            marker="o",
            label=f"  Inicio: ({trayectoria_x[0]}, {trayectoria_y[0]}, {trayectoria_z[0]})",
            zorder=5,
        )

        # Mostrar coordenadas del inicio
        ax.text(
            trayectoria_x[0],
            trayectoria_y[0],
            trayectoria_z[0],
            f"  Inicio: ({trayectoria_x[0]}, {trayectoria_y[0]}, {trayectoria_z[0]})",
            color="black",
            fontsize=10,
        )

        # Marcar el punto final (rojo)
        ax.scatter(
            trayectoria_x[-1],
            trayectoria_y[-1],
            trayectoria_z[-1],
            color="red",
            s=100,
            marker="*",
            label=f"  Final: ({trayectoria_x[-1]}, {trayectoria_y[-1]}, {trayectoria_z[-1]})",
            zorder=5,
        )

        # Mostrar coordenadas del final
        ax.text(
            trayectoria_x[-1],
            trayectoria_y[-1],
            trayectoria_z[-1],
            f"  Final: ({trayectoria_x[-1]}, {trayectoria_y[-1]}, {trayectoria_z[-1]})",
            color="red",
            fontsize=10,
        )

        ax.set_title("Trayectoria de la Caminata Aleatoria en 3D de la Rana Feliz")
        ax.set_xlabel("Posición X")
        ax.set_ylabel("Posición Y")
        ax.set_zlabel("Posición Z")
        ax.legend()
        plt.show()

    # @staticmethod
    # def graficar_scatter_3D(posiciones_finales):
    #     import matplotlib.pyplot as plt

    #     x = [p[0] for p in posiciones_finales]
    #     y = [p[1] for p in posiciones_finales]
    #     z = [p[2] for p in posiciones_finales]

    #     fig = plt.figure(figsize=(10, 10))
    #     ax = fig.add_subplot(111, projection="3d")
    #     ax.scatter(x, y, z, alpha=0.5)
    #     ax.set_title("Posiciones Finales de las Simulaciones en el Espacio 3D")
    #     ax.set_xlabel("Posición X")
    #     ax.set_ylabel("Posición Y")
    #     ax.set_zlabel("Posición Z")
    #     plt.show()
    @staticmethod
    def graficar_scatter_3D(posiciones_finales, n_pasos):
        import numpy as np

        # 1. Procesar datos con NumPy para mayor eficiencia y cálculo de distancias
        # Convertimos la lista de tuplas a una matriz NumPy de forma (N, 3)
        pos = np.array(posiciones_finales)

        x = pos[:, 0]
        y = pos[:, 1]
        z = pos[:, 2]

        # Calculamos la distancia euclidiana de cada punto al origen (0,0,0)
        # Esta es la métrica clave para entender la dispersión en 3D
        distancias = np.sqrt(x**2 + y**2 + z**2)

        # 2. Configuración del gráfico
        fig = plt.figure(figsize=(12, 10))  # Un poco más ancho para la barra de color
        ax = fig.add_subplot(111, projection="3d")

        # 3. CREAR EL SCATTER CON GRADIENTE DE COLOR (Crucial)
        # 'c=distancias' asigna un color a cada punto basado en su lejanía
        # 'cmap' define la paleta. 'viridis' es excelente para percibir profundidades.
        scatter = ax.scatter(
            x, y, z, c=distancias, cmap="viridis", s=30, alpha=0.6, edgecolors="none"
        )

        # Añadir barra de color (colorbar) para referencia numérica de la distancia
        cbar = fig.colorbar(scatter, ax=ax, shrink=0.6, pad=0.1)
        cbar.set_label("Distancia Euclídeana al Origen", fontsize=12)

        # 4. MARCAR EL ORIGEN (Fundamental para el análisis)
        # Dibujamos un punto rojo grande y brillante en (0,0,0)
        ax.scatter(
            0, 0, 0, color="red", s=200, marker="*", label="Origen (0,0,0)", zorder=10
        )

        # 5. AJUSTAR PROPORCIONES (Para evitar la elipse)
        # Forzamos a que las unidades en los tres ejes midan lo mismo en pantalla
        ax.set_box_aspect([1, 1, 1])  # Aspecto de cubo perfecto

        # Definimos límites simétricos basados en sqrt(n) para dar contexto
        # sqrt(n_pasos) nos da una idea de la dispersión típica
        limite = np.sqrt(n_pasos) * 1.5  # Un margen para los outliers
        ax.set_xlim(-limite, limite)
        ax.set_ylim(-limite, limite)
        ax.set_zlim(-limite, limite)

        # 6. Estética y Leyendas
        fig.suptitle(
            f"Distribución Final en Espacio 3D tras {n_pasos:,} pasos",
            fontsize=14,
            y=0.98,
        )
        ax.set_xlabel("Posición X", fontsize=11)
        ax.set_ylabel("Posición Y", fontsize=11)
        ax.set_zlabel("Posición Z", fontsize=11)

        # Colocar la leyenda del origen de forma visible
        ax.legend(loc="upper right", frameon=True, fontsize=10)

        # Mejorar la visibilidad de la cuadrícula
        ax.grid(True, linestyle="--", alpha=0.5)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def graficar_proyecciones_ortogonales(trayectoria_x, trayectoria_y, trayectoria_z):

        fig, axs = plt.subplots(1, 3, figsize=(18, 6))

        # Proyección XY
        axs[0].scatter(trayectoria_x, trayectoria_y, alpha=0.5)
        axs[0].scatter(
            trayectoria_x[0],
            trayectoria_y[0],
            color="black",
            s=100,
            marker="o",
            label="Inicio",
            zorder=5,
        )
        axs[0].scatter(
            trayectoria_x[-1],
            trayectoria_y[-1],
            color="red",
            s=100,
            marker="*",
            label="Final",
            zorder=5,
        )
        axs[0].text(
            trayectoria_x[0],
            trayectoria_y[0],
            f"  ({trayectoria_x[0]}, {trayectoria_y[0]})",
            color="black",
            fontsize=9,
        )
        axs[0].text(
            trayectoria_x[-1],
            trayectoria_y[-1],
            f"  ({trayectoria_x[-1]}, {trayectoria_y[-1]})",
            color="red",
            fontsize=9,
        )
        axs[0].set_title("Proyección XY")
        axs[0].set_xlabel("Posición X")
        axs[0].set_ylabel("Posición Y")
        axs[0].axhline(y=0, color="black", linewidth=0.8)
        axs[0].axvline(x=0, color="black", linewidth=0.8)
        axs[0].legend(loc="upper right")

        # Proyección XZ
        axs[1].scatter(trayectoria_x, trayectoria_z, alpha=0.5)
        axs[1].scatter(
            trayectoria_x[0],
            trayectoria_z[0],
            color="black",
            s=100,
            marker="o",
            label="Inicio",
            zorder=5,
        )
        axs[1].scatter(
            trayectoria_x[-1],
            trayectoria_z[-1],
            color="red",
            s=100,
            marker="*",
            label="Final",
            zorder=5,
        )
        axs[1].text(
            trayectoria_x[0],
            trayectoria_z[0],
            f"  ({trayectoria_x[0]}, {trayectoria_z[0]})",
            color="black",
            fontsize=9,
        )
        axs[1].text(
            trayectoria_x[-1],
            trayectoria_z[-1],
            f"  ({trayectoria_x[-1]}, {trayectoria_z[-1]})",
            color="red",
            fontsize=9,
        )
        axs[1].set_title("Proyección XZ")
        axs[1].set_xlabel("Posición X")
        axs[1].set_ylabel("Posición Z")
        axs[1].axhline(y=0, color="black", linewidth=0.8)
        axs[1].axvline(x=0, color="black", linewidth=0.8)
        axs[1].legend(loc="upper right")

        # Proyección YZ
        axs[2].scatter(trayectoria_y, trayectoria_z, alpha=0.5)
        axs[2].scatter(
            trayectoria_y[0],
            trayectoria_z[0],
            color="black",
            s=100,
            marker="o",
            label="Inicio",
            zorder=5,
        )
        axs[2].scatter(
            trayectoria_y[-1],
            trayectoria_z[-1],
            color="red",
            s=100,
            marker="*",
            label="Final",
            zorder=5,
        )
        axs[2].text(
            trayectoria_y[0],
            trayectoria_z[0],
            f"  ({trayectoria_y[0]}, {trayectoria_z[0]})",
            color="black",
            fontsize=9,
        )
        axs[2].text(
            trayectoria_y[-1],
            trayectoria_z[-1],
            f"  ({trayectoria_y[-1]}, {trayectoria_z[-1]})",
            color="red",
            fontsize=9,
        )
        axs[2].set_title("Proyección YZ")
        axs[2].set_xlabel("Posición Y")
        axs[2].set_ylabel("Posición Z")
        axs[2].axhline(y=0, color="black", linewidth=0.8)
        axs[2].axvline(x=0, color="black", linewidth=0.8)
        axs[2].legend(loc="upper right")

        plt.tight_layout()
        plt.show()
