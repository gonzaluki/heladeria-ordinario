from config import *
from estructuras.arreglo import Cono
from estructuras.cola import Cola
from estructuras.pila import Pila
from estructuras.lista_circular import ListaCircular
from estructuras.arbol import ArbolBST
from estructuras.grafo import Grafo


class Datos:
    def __init__(self):
        self.cono = Cono(MAX_BOLAS)
        self.pedidos = []
        self.cola = Cola(MAX_CLIENTES)
        self.pila = Pila(MAX_INSUMOS)
        self.proveedores = ListaCircular()
        self.arbol = ArbolBST()
        self.grafo = Grafo()
