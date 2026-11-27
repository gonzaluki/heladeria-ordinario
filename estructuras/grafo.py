def buscar_padre(padre, x):
    while padre[x] != x:
        padre[x] = padre[padre[x]]
        x = padre[x]
    return x


class Grafo:
    def __init__(self):
        self.vertices = []
        self.aristas = []    

    def agregar_vertice(self, nombre):
        # El nombre lo escribe el usuario (cualquier texto) y no hay límite de vértices.
        # Lo único que no se permite es repetir un nombre, porque así se identifica al vértice.
        if nombre in self.vertices:
            return False
        self.vertices.append(nombre)
        return True

    def existe_arista(self, a, b):
        for origen, destino, peso in self.aristas:
            if (origen == a and destino == b) or (origen == b and destino == a):
                return True
        return False

    def agregar_arista(self, a, b, peso):
        self.aristas.append((a, b, peso))

    def kruskal(self):
        padre = {}
        for v in self.vertices:
            padre[v] = v
        ordenadas = sorted(self.aristas, key=lambda arista: arista[2])

        aceptadas = []
        rechazadas = []
        costo = 0
        for origen, destino, peso in ordenadas:
            raiz_a = buscar_padre(padre, origen)
            raiz_b = buscar_padre(padre, destino)
            if raiz_a != raiz_b:
                padre[raiz_a] = raiz_b
                aceptadas.append((origen, destino, peso))
                costo = costo + peso
            else:
                rechazadas.append((origen, destino, peso))
        partes = []
        for v in self.vertices:
            raiz = buscar_padre(padre, v)
            if raiz not in partes:
                partes.append(raiz)
        return aceptadas, rechazadas, costo, len(partes)
