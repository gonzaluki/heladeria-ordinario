import tkinter as tk
from config import *
from interfaz.componentes import *

class PaginaMenu(tk.Frame):
    def __init__(self, padre, datos, ir_a):
        tk.Frame.__init__(self, padre)
        self.datos = datos
        centro = preparar_pagina(self, "🍨 Heladería Artesanal", "Bienvenido, elige qué quieres hacer")
        avisar(self.mensaje, "Todo empieza vacío: ve llenando cada módulo.", "info")

        fila = tk.Frame(centro, bg=FONDO)
        fila.pack(fill="x", pady=(0, 20))
        self.numeros = {}
        contadores = [
            ("helados", "Helados vendidos", CORAL),
            ("clientes", "Clientes en fila", CHOCOLATE),
            ("insumos", "Insumos por comprar", VERDE),
            ("proveedores", "Proveedores activos", INDIGO),
        ]
        for i, (clave, texto, color) in enumerate(contadores):
            fila.columnconfigure(i, weight=1, uniform="contador")
            t = tarjeta(fila)
            t.grid(row=0, column=i, sticky="nsew", padx=6)
            numero = tk.Label(t, text="0", font=(FUENTE, 28, "bold"), bg=BLANCO, fg=color)
            numero.pack(anchor="w")
            tk.Label(t, text=texto, font=F_TEXTO, bg=BLANCO, fg=GRIS).pack(anchor="w")
            self.numeros[clave] = numero

        tk.Label(centro, text="Ir a un módulo", font=F_TARJETA, bg=FONDO,
                 fg=TEXTO).pack(anchor="w", pady=(0, 8))
        botones = tk.Frame(centro, bg=FONDO)
        botones.pack(fill="x")
        modulos = [
            ("Arreglos", "arreglos"), 
            ("Colas", "colas"),
            ("Pilas", "pilas"), 
            ("QuickSort", "quicksort"),
            ("Búsqueda Binaria", "binaria"), 
            ("Lista Circular", "lista"),
            ("Árbol ", "arbol"), 
            ("Grafos · Kruskal", "grafos"),
        ]
        for i, (texto, clave) in enumerate(modulos):
            fila_num = i // 4
            columna = i % 4
            botones.columnconfigure(columna, weight=1, uniform="modulo")
            boton = Boton(botones, texto, lambda c=clave: ir_a(c), "chocolate")
            boton.grid(row=fila_num, column=columna, sticky="nsew", padx=6, pady=6, ipady=14)

    def actualizar(self):
        self.numeros["helados"].config(text=str(len(self.datos.pedidos)))
        self.numeros["clientes"].config(text=str(self.datos.cola.tamano))
        self.numeros["insumos"].config(text=str(self.datos.pila.cantidad()))
        self.numeros["proveedores"].config(text=str(self.datos.proveedores.cantidad))
