class Cola:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.datos = [None] * capacidad
        self.frente = 0
        self.final = -1
        self.tamano = 0

    def esta_vacia(self):
        return self.tamano == 0

    def esta_llena(self):
        return self.tamano == self.capacidad

    def encolar(self, valor):
        if self.esta_llena():
            return False
        self.final = (self.final + 1) % self.capacidad
        self.datos[self.final] = valor
        self.tamano = self.tamano + 1
        return True

    def desencolar(self):
        if self.esta_vacia():
            return None
        valor = self.datos[self.frente]
        self.datos[self.frente] = None
        self.frente = (self.frente + 1) % self.capacidad
        self.tamano = self.tamano - 1
        if self.tamano == 0:
            self.frente = 0
            self.final = -1
        return valor

    def lista(self):
        resultado = []
        for i in range(self.tamano):
            resultado.append(self.datos[(self.frente + i) % self.capacidad])
        return resultado
