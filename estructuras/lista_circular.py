class NodoProveedor:
    def __init__(self, id_prov, empresa, insumo, telefono):
        self.id_prov = id_prov
        self.empresa = empresa
        self.insumo = insumo
        self.telefono = telefono
        self.siguiente = None
        self.anterior = None


class ListaCircular:
    def __init__(self):
        self.cabeza = None
        self.actual = None
        self.cantidad = 0
        self.contador = 0        

    def esta_vacia(self):
        return self.cabeza is None

    def agregar(self, empresa, insumo, telefono):
        self.contador = self.contador + 1
        nodo = NodoProveedor(f"PROV-{self.contador:02d}", empresa, insumo, telefono)
        if self.cabeza is None:
            nodo.siguiente = nodo
            nodo.anterior = nodo
            self.cabeza = nodo
            self.actual = nodo
        else:
            ultimo = self.cabeza.anterior
            nodo.anterior = ultimo
            nodo.siguiente = self.cabeza
            ultimo.siguiente = nodo
            self.cabeza.anterior = nodo
        self.cantidad = self.cantidad + 1
        return nodo

    def nodos(self):
        resultado = []
        nodo = self.cabeza
        for i in range(self.cantidad):
            resultado.append(nodo)
            nodo = nodo.siguiente
        return resultado

    def buscar(self, id_prov):
        for nodo in self.nodos():
            if nodo.id_prov == id_prov:
                return nodo
        return None

    def eliminar(self, id_prov):
        if self.cabeza is None:
            return None
        nodo = self.buscar(id_prov)
        if nodo is None:
            return None

        if self.cantidad == 1:
            self.cabeza = None
            self.actual = None
        else:
            if nodo is self.cabeza:
                self.cabeza = nodo.siguiente
            if self.actual is nodo:
                self.actual = nodo.siguiente
            nodo.anterior.siguiente = nodo.siguiente
            nodo.siguiente.anterior = nodo.anterior

        nodo.siguiente = None
        nodo.anterior = None
        self.cantidad = self.cantidad - 1
        return nodo

    def avanzar(self):
        if self.actual is not None:
            self.actual = self.actual.siguiente

    def retroceder(self):
        if self.actual is not None:
            self.actual = self.actual.anterior
