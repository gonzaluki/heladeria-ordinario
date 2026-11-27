class Cono:
    def __init__(self, tamano):
        self.tamano = tamano
        self.bolas = [None] * tamano

    def agregar(self, sabor, precio):
        for i in range(self.tamano):
            if self.bolas[i] is None:
                self.bolas[i] = (sabor, precio)
                return i
        return -1

    def quitar_ultima(self):
        for i in range(self.tamano - 1, -1, -1):
            if self.bolas[i] is not None:
                bola = self.bolas[i]
                self.bolas[i] = None
                return bola
        return None

    def lista(self):
        resultado = []
        for bola in self.bolas:
            if bola is not None:
                resultado.append(bola)
        return resultado

    def total(self):
        suma = 0
        for sabor, precio in self.lista():
            suma = suma + precio
        return suma

    def vaciar(self):
        self.bolas = [None] * self.tamano
