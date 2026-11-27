import tkinter as tk
from config import *
from interfaz.componentes import *
from estructuras.ordenamiento import quicksort

COLUMNAS = [("Folio", 80, "center"), ("Sabores", 430, "w"), ("Bolas", 80, "center"), ("Total", 100, "center")]


def fila_de_pedido(pedido):
    sabores = []
    for sabor, precio in pedido["bolas"]:
        sabores.append(sabor)
    return (pedido["folio"], ", ".join(sabores), len(pedido["bolas"]), f"${pedido['total']}")


class PaginaQuickSort(tk.Frame):
    def __init__(self, padre, datos):
        tk.Frame.__init__(self, padre)
        self.datos = datos
        centro = preparar_pagina(self, "Ordenamiento · QuickSort",
                                 "Ordena los pedidos del más barato al más caro")

        t1 = tarjeta(centro, "Pedidos en el orden en que se hicieron")
        t1.pack(fill="both", expand=True, pady=(0, 10))
        marco1, self.tabla_original = tabla(t1, COLUMNAS, 5)
        marco1.pack(fill="both", expand=True)

        Boton(centro, "Ordenar Registro (QuickSort)", self.ordenar, "secundario").pack(fill="x", pady=(0, 10))

        t2 = tarjeta(centro, "Pedidos ordenados de menor a mayor Total")
        t2.pack(fill="both", expand=True)
        marco2, self.tabla_ordenada = tabla(t2, COLUMNAS, 5)
        marco2.pack(fill="both", expand=True)

    def actualizar(self):
        llenar_tabla(self.tabla_original, [fila_de_pedido(p) for p in self.datos.pedidos])
        llenar_tabla(self.tabla_ordenada, [])
        if len(self.datos.pedidos) == 0:
            avisar(self.mensaje, "Todavía no hay pedidos. Crea uno en el módulo Arreglos.", "info")
        else:
            avisar(self.mensaje, "Presiona el botón para ordenar los pedidos.", "info")

    def ordenar(self):
        try:
            pedidos = self.datos.pedidos
            llenar_tabla(self.tabla_original, [fila_de_pedido(p) for p in pedidos])
            if len(pedidos) == 0:
                llenar_tabla(self.tabla_ordenada, [])
                avisar(self.mensaje, "No hay pedidos que ordenar. Crea uno en el módulo Arreglos.", "warn")
                return
            copia = list(pedidos)
            quicksort(copia, 0, len(copia) - 1)
            llenar_tabla(self.tabla_ordenada, [fila_de_pedido(p) for p in copia])
            avisar(self.mensaje, f"Listo: {len(copia)} pedido(s) ordenados, del más barato "
                   f"(${copia[0]['total']}) al más caro (${copia[-1]['total']}).", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")
