class NodoBST:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None


class ArbolBST:
    def __init__(self):
        self.raiz = None
        self.cantidad = 0

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = NodoBST(valor)
            self.cantidad = 1
            return True
        actual = self.raiz
        while True:
            if valor == actual.valor:
                return False
            if valor < actual.valor:
                if actual.izq is None:
                    actual.izq = NodoBST(valor)
                    break
                actual = actual.izq
            else:
                if actual.der is None:
                    actual.der = NodoBST(valor)
                    break
                actual = actual.der
        self.cantidad = self.cantidad + 1
        return True

    def buscar(self, valor):
        camino = []
        actual = self.raiz
        while actual is not None:
            camino.append(actual.valor)
            if valor == actual.valor:
                return camino, True
            if valor < actual.valor:
                actual = actual.izq
            else:
                actual = actual.der
        return camino, False

    def cambiar_hijo(self, padre, viejo, nuevo):
        if padre is None:
            self.raiz = nuevo
        elif padre.izq is viejo:
            padre.izq = nuevo
        else:
            padre.der = nuevo

    def eliminar(self, valor):
        padre = None
        actual = self.raiz
        while actual is not None and actual.valor != valor:
            padre = actual
            if valor < actual.valor:
                actual = actual.izq
            else:
                actual = actual.der
        if actual is None:
            return False

        if actual.izq is None and actual.der is None:
            self.cambiar_hijo(padre, actual, None)
        elif actual.izq is None:
            self.cambiar_hijo(padre, actual, actual.der)
        elif actual.der is None:
            self.cambiar_hijo(padre, actual, actual.izq)
        else:
            padre_suc = actual
            sucesor = actual.der
            while sucesor.izq is not None:
                padre_suc = sucesor
                sucesor = sucesor.izq
            actual.valor = sucesor.valor
            self.cambiar_hijo(padre_suc, sucesor, sucesor.der)

        self.cantidad = self.cantidad - 1
        return True

    def preorden(self):
        resultado = []
        self.recorrer_pre(self.raiz, resultado)
        return resultado

    def recorrer_pre(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.valor)
            self.recorrer_pre(nodo.izq, resultado)
            self.recorrer_pre(nodo.der, resultado)

    def inorden(self):
        resultado = []
        self.recorrer_in(self.raiz, resultado)
        return resultado

    def recorrer_in(self, nodo, resultado):
        if nodo is not None:
            self.recorrer_in(nodo.izq, resultado)
            resultado.append(nodo.valor)
            self.recorrer_in(nodo.der, resultado)

    def postorden(self):
        resultado = []
        self.recorrer_post(self.raiz, resultado)
        return resultado

    def recorrer_post(self, nodo, resultado):
        if nodo is not None:
            self.recorrer_post(nodo.izq, resultado)
            self.recorrer_post(nodo.der, resultado)
            resultado.append(nodo.valor)
