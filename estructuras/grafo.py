def buscar_padre(padre, x):
    while padre[x] != x:
        padre[x] = padre[padre[x]]
        x = padre[x]
    return x


class Grafo:
    def __init__(self):
        self.vertices = []
        self.aristas = []    

    def agregar_vertice(self):
        if len(self.vertices) >= 10:
            return None
        letra = chr(ord("A") + len(self.vertices))
        self.vertices.append(letra)
        return letra

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
