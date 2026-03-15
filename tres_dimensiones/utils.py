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
            color="green",
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
            color="green",
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

    @staticmethod
    def graficar_scatter_3D(posiciones_finales):
        import matplotlib.pyplot as plt

        x = [p[0] for p in posiciones_finales]
        y = [p[1] for p in posiciones_finales]
        z = [p[2] for p in posiciones_finales]

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(x, y, z, alpha=0.5)
        ax.set_title("Posiciones Finales de las Simulaciones en el Espacio 3D")
        ax.set_xlabel("Posición X")
        ax.set_ylabel("Posición Y")
        ax.set_zlabel("Posición Z")
        plt.show()

    @staticmethod
    def graficar_proyecciones_ortogonales(trayectoria_x, trayectoria_y, trayectoria_z):

        fig, axs = plt.subplots(1, 3, figsize=(18, 6))

        # Proyección XY
        axs[0].scatter(trayectoria_x, trayectoria_y, alpha=0.5)
        axs[0].set_title("Proyección XY")
        axs[0].set_xlabel("Posición X")
        axs[0].set_ylabel("Posición Y")
        axs[0].axhline(y=0, color="black", linewidth=0.8)
        axs[0].axvline(x=0, color="black", linewidth=0.8)

        # Proyección XZ
        axs[1].scatter(trayectoria_x, trayectoria_z, alpha=0.5)
        axs[1].set_title("Proyección XZ")
        axs[1].set_xlabel("Posición X")
        axs[1].set_ylabel("Posición Z")
        axs[1].axhline(y=0, color="black", linewidth=0.8)
        axs[1].axvline(x=0, color="black", linewidth=0.8)

        # Proyección YZ
        axs[2].scatter(trayectoria_y, trayectoria_z, alpha=0.5)
        axs[2].set_title("Proyección YZ")
        axs[2].set_xlabel("Posición Y")
        axs[2].set_ylabel("Posición Z")
        axs[2].axhline(y=0, color="black", linewidth=0.8)
        axs[2].axvline(x=0, color="black", linewidth=0.8)

        plt.tight_layout()
        plt.show()
