def clave(valor):
    # Sirve para comparar valores de distinto tipo dentro del mismo árbol:
    # primero van los números (de menor a mayor) y después los textos (en orden alfabético).
    if isinstance(valor, str):
        return (1, valor.casefold(), valor)
    return (0, valor, "")


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
        # Se permiten repetidos: un valor igual al del nodo se manda a la derecha.
        nuevo = NodoBST(valor)
        if self.raiz is None:
            self.raiz = nuevo
            self.cantidad = 1
            return nuevo
        actual = self.raiz
        while True:
            if clave(valor) < clave(actual.valor):
                if actual.izq is None:
                    actual.izq = nuevo
                    break
                actual = actual.izq
            else:
                if actual.der is None:
                    actual.der = nuevo
                    break
                actual = actual.der
        self.cantidad = self.cantidad + 1
        return nuevo

    def buscar(self, valor):
        # Regresa la lista de nodos visitados y si se encontró el valor
        # (si está repetido, se queda con el primero que encuentra, el más arriba).
        camino = []
        actual = self.raiz
        while actual is not None:
            camino.append(actual)
            if clave(valor) == clave(actual.valor):
                return camino, True
            if clave(valor) < clave(actual.valor):
                actual = actual.izq
            else:
                actual = actual.der
        return camino, False

    def contar(self, valor):
        veces = 0
        for nodo in self.nodos_inorden():
            if clave(nodo.valor) == clave(valor):
                veces = veces + 1
        return veces

    def cambiar_hijo(self, padre, viejo, nuevo):
        if padre is None:
            self.raiz = nuevo
        elif padre.izq is viejo:
            padre.izq = nuevo
        else:
            padre.der = nuevo

    def eliminar(self, valor):
        # Si el valor está repetido, elimina solo una copia (la primera que encuentra).
        padre = None
        actual = self.raiz
        while actual is not None and clave(actual.valor) != clave(valor):
            padre = actual
            if clave(valor) < clave(actual.valor):
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

    # Los recorridos guardan los nodos (para poder dibujarlos aunque haya valores repetidos)
    # y las funciones preorden / inorden / postorden regresan solo los valores.
    def nodos_preorden(self):
        resultado = []
        self.recorrer_pre(self.raiz, resultado)
        return resultado

    def nodos_inorden(self):
        resultado = []
        self.recorrer_in(self.raiz, resultado)
        return resultado

    def nodos_postorden(self):
        resultado = []
        self.recorrer_post(self.raiz, resultado)
        return resultado

    def preorden(self):
        return [nodo.valor for nodo in self.nodos_preorden()]

    def inorden(self):
        return [nodo.valor for nodo in self.nodos_inorden()]

    def postorden(self):
        return [nodo.valor for nodo in self.nodos_postorden()]

    def recorrer_pre(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo)
            self.recorrer_pre(nodo.izq, resultado)
            self.recorrer_pre(nodo.der, resultado)

    def recorrer_in(self, nodo, resultado):
        if nodo is not None:
            self.recorrer_in(nodo.izq, resultado)
            resultado.append(nodo)
            self.recorrer_in(nodo.der, resultado)

    def recorrer_post(self, nodo, resultado):
        if nodo is not None:
            self.recorrer_post(nodo.izq, resultado)
            self.recorrer_post(nodo.der, resultado)
            resultado.append(nodo)
