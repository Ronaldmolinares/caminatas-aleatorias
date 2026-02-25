class GeneradorCongruenciaLineal:
    """
    Generador de números pseudoaleatorios usando el método de Congruencia Lineal.

    Fórmula: X_{n+1} = (a * X_n + c) mod m

    Attributes
    ----------
    --> semilla (int): Valor inicial para la secuencia pseudoaleatoria (X_0).
    --> a (int): Multiplicador (1664525, valor recomendado por Numerical Recipes).
    --> c (int): Incremento (1013904223).
    --> m (int): Módulo (2^32, rango máximo de valores).
    --> Métod Formal: Ri = Xi / m


    Methods
    -------
    generar_Xi(pasos)
        Genera una secuencia de números enteros pseudoaleatorios X_i.

    generar_Ri(pasos)
        Genera una secuencia de números pseudoaleatorios uniformes en [0, 1).

    Notes
    -----
    - Los parámetros (a, c, m) están optimizados según Numerical Recipes
    - La semilla debe ser un entero positivo menor que m
    - La secuencia es determinista: misma semilla = misma secuencia
    """

    def __init__(self, semilla):
        """
        Inicializar el generador con una semilla específica.

        Parameters
        ----------
        semilla : int
            Valor inicial para la secuencia pseudoaleatoria. Debe ser un
            entero no negativo menor que 2^32.
        """
        self.semilla = semilla  # Semilla
        self.a = 1664525  # Multiplicador
        self.c = 1013904223  # Incremento
        self.m = 2**32  # Módulo

    def siguiente_Ri(self):
        """
        Genera el siguiente número pseudoaleatorio R_i en el rango [0, 1).

        Aplica la fórmula de congruencia lineal para actualizar el estado
        interno (self.semilla) y devuelve el número normalizado R_i.

        Returns
        -------
        float
            El siguiente número pseudoaleatorio R_i en el rango [0, 1).

        Notes
        -----
        - Cada llamada a este método avanza la secuencia y modifica el estado
          interno del generador.
        - El valor devuelto es siempre >= 0 y < 1.
        """
        siguiente_Xi = (
            self.a * self.semilla + self.c
        ) % self.m  # Calcular el siguiente X_i usando la fórmula de congruencia lineal
        self.semilla = siguiente_Xi
        Ri_normalizado = (
            siguiente_Xi / self.m
        )  # Normalizar X_i para obtener R_i en el rango [0, 1)
        return Ri_normalizado

    # def generar_Xi(self, pasos: int):
    #     """
    #     Generar una secuencia de números enteros pseudoaleatorios.

    #     Aplica repetidamente la fórmula de congruencia lineal para generar
    #     una secuencia de números enteros X_i en el rango [0, m).

    #     Parameters
    #     ----------
    #     pasos : int
    #         Cantidad de números pseudoaleatorios a generar.

    #     Returns
    #     -------
    #     list of int
    #         Lista con los números enteros X_i generados.

    #     Notes
    #     -----
    #     Este método modifica el estado interno (self.semilla) con cada
    #     número generado, por lo que llamadas sucesivas continuarán la
    #     secuencia desde el último valor.
    #     """
    #     secuencia_Xi = []

    #     for _ in range(pasos):
    #         siguiente_Xi = (self.a * self.semilla + self.c) % self.m
    #         self.semilla = siguiente_Xi
    #         secuencia_Xi.append(siguiente_Xi)

    #     return secuencia_Xi

    # def generar_Ri(self, pasos: int):
    #     """
    #     Generar una secuencia de números pseudoaleatorios uniformes en [0, 1).

    #     Genera números enteros X_i y los normaliza dividiéndolos por m para
    #     obtener valores en el intervalo [0, 1).

    #     Parameters
    #     ----------
    #     pasos : int
    #         Cantidad de números pseudoaleatorios a generar.

    #     Returns
    #     -------
    #     list of float
    #         Lista con números pseudoaleatorios R_i en el rango [0, 1).

    #     Notes
    #     -----
    #     - Cada R_i se calcula como: R_i = X_i / m
    #     - Los valores están uniformemente distribuidos en [0, 1)
    #     - Este método también modifica el estado interno del generador
    #     """
    #     secuencia_Ri = []
    #     secuencia_Xi = self.generar_Xi(pasos)

    #     for i in range(pasos):
    #         Ri_normalizado = secuencia_Xi[i] / self.m
    #         secuencia_Ri.append(Ri_normalizado)

    #     return secuencia_Ri
