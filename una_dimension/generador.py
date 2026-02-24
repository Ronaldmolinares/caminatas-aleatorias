class GeneradorCongruenciaLineal:
    def __init__(self, semilla):
        self.semilla = semilla  # Semilla
        self.a = 1664525  # Multiplicador
        self.c = 1013904223  # Incremento
        self.m = 2**32  # Módulo

    def generar_Xi(self, pasos: int):
        lista_Xi = []

        for _ in range(pasos):
            Xi = (self.a * self.semilla + self.c) % self.m
            self.semilla = Xi
            lista_Xi.append(Xi)

        return lista_Xi

    def generar_Ri(self, pasos: int):
        lista_Ri = []
        Xi = self.generar_Xi(pasos)

        for i in range(pasos):
            Ri = Xi[i] / (self.m - 1)
            lista_Ri.append(Ri)
        print(f"{Xi} \n")
        return lista_Ri

    def generar_Ni(self, pasos: int, a: int, b: int):
        lista_Ri = self.generar_Ri(pasos)
        lista_Ni = []

        for Ri in lista_Ri:
            Ni = a + (b - a) * Ri
            lista_Ni.append(Ni)
        print(f"{lista_Ri} \n")
        print(f"{lista_Ni} \n")
        return lista_Ni, lista_Ri
