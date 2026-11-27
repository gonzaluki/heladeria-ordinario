class Pila:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.items = [None] * capacidad
        self.tope = -1

    def esta_vacia(self):
        return self.tope == -1

    def esta_llena(self):
        return self.tope == self.capacidad - 1

    def cantidad(self):
        return self.tope + 1

    def push(self, valor):
        if self.esta_llena():
            return False
        self.tope = self.tope + 1
        self.items[self.tope] = valor
        return True

    def pop(self):
        if self.esta_vacia():
            return None
        valor = self.items[self.tope]
        self.items[self.tope] = None
        self.tope = self.tope - 1
        return valor

    def peek(self):
        if self.esta_vacia():
            return None
        return self.items[self.tope]

    def lista(self):
        resultado = []
        for i in range(self.tope + 1):
            resultado.append(self.items[i])
        return resultado
