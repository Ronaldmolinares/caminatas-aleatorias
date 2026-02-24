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
            Ri = Xi[i] / self.m
            lista_Ri.append(Ri)

        return lista_Ri
