import tkinter as tk
from config import *
from interfaz.componentes import *
from estructuras.busqueda import busqueda_binaria


class PaginaBinaria(tk.Frame):
    def __init__(self, padre, datos):
        tk.Frame.__init__(self, padre)
        self.datos = datos
        self.resultado = None
        centro = preparar_pagina(self, "Búsqueda Binaria · Consulta por folio",
                                 "Busca un pedido usando su número de folio")
        centro.columnconfigure(1, weight=1)
        centro.rowconfigure(0, weight=1)

        izq = tarjeta(centro, "Buscar pedido")
        izq.grid(row=0, column=0, sticky="n", padx=(0, 16))
        etiqueta_campo(izq, "Folios que existen")
        self.combo, self.var_folio = combo(izq, [], 22)
        self.combo.pack(fill="x", ipady=3)
        Boton(izq, "Buscar con Búsqueda Binaria", self.buscar_elegido, "secundario").pack(fill="x", pady=(14, 18))
        tk.Frame(izq, bg=BORDE, height=1).pack(fill="x")
        etiqueta_campo(izq, "O prueba otro folio (1 a 999)")
        self.spin, self.var_numero = spin(izq, range(1, 1000))
        self.spin.pack(anchor="w", ipady=4)
        Boton(izq, "Buscar este folio", self.buscar_numero, "neutro").pack(fill="x", pady=(14, 0))

        der = tarjeta(centro, "Resultado")
        der.grid(row=0, column=1, sticky="nsew")
        self.canvas = tk.Canvas(der, height=360, bg=BLANCO, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.al_cambiar_tamano)
        self.dibujar()

    def al_cambiar_tamano(self, evento):
        self.dibujar()

    def actualizar(self):
        folios = []
        for pedido in self.datos.pedidos:
            folios.append(pedido["folio"])
        self.combo.config(values=folios)
        if len(folios) > 0 and self.var_folio.get() not in folios:
            self.var_folio.set(folios[0])
        if len(folios) == 0:
            self.var_folio.set("")
            avisar(self.mensaje, "Todavía no hay pedidos. Crea uno en el módulo Arreglos.", "info")
        else:
            avisar(self.mensaje, f"Hay {len(folios)} pedido(s) para consultar.", "info")
        self.dibujar()

    def buscar_elegido(self):
        try:
            if self.var_folio.get() == "":
                avisar(self.mensaje, "Elige un folio de la lista (primero crea pedidos en Arreglos).", "warn")
                return
            self.buscar(int(self.var_folio.get()))
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def buscar_numero(self):
        try:
            self.buscar(int(self.var_numero.get()))
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def buscar(self, folio):
        pedidos = self.datos.pedidos
        if len(pedidos) == 0:
            avisar(self.mensaje, "No hay pedidos registrados. Crea uno en el módulo Arreglos.", "warn")
            return
        lugar = busqueda_binaria(pedidos, folio)
        if lugar == -1:
            self.resultado = ("no", folio)
            avisar(self.mensaje, f"Folio no encontrado: {folio:03d}.", "warn")
        else:
            self.resultado = ("si", pedidos[lugar])
            avisar(self.mensaje, f"Folio {folio:03d} encontrado.", "ok")
        self.dibujar()

    def dibujar(self):
        c = self.canvas
        c.delete("all")
        ancho = max(c.winfo_width(), 420)
        x1 = (ancho - 340) / 2
        x2 = x1 + 340
        if self.resultado is None:
            caja(c, x1, 10, x2, 340, "#FBF7F4", "#CFC3BA", raya=(4, 3))
            c.create_text(ancho / 2, 175, text="Aquí aparecerá el resultado\nde la búsqueda", font=F_TEXTO,
                          fill=GRIS, justify="center")
            return
        tipo, dato = self.resultado
        if tipo == "no":
            caja(c, x1, 10, x2, 340, "#FDE8E8", ROJO, 2)
            c.create_text(ancho / 2, 140, text="Folio no encontrado", font=(FUENTE, 18, "bold"), fill=ROJO_OSCURO)
            c.create_text(ancho / 2, 185, text=f"El folio {dato:03d} no existe.", font=F_SUB, fill=TEXTO)
            return
        pedido = dato
        caja(c, x1, 10, x2, 340, VERDE_CLARO, VERDE, 2)
        c.create_text(ancho / 2, 40, text="🍨 Pedido " + pedido["folio"], font=(FUENTE, 16, "bold"), fill=VERDE_OSCURO)
        c.create_line(x1 + 16, 66, x2 - 16, 66, fill=VERDE, dash=(5, 3))
        y = 92
        for sabor, precio in pedido["bolas"]:
            c.create_text(x1 + 24, y, text="1 bola de " + sabor, anchor="w", font=F_TEXTO, fill=TEXTO)
            c.create_text(x2 - 24, y, text=f"${precio}", anchor="e", font=F_NEGRITA, fill=TEXTO)
            y = y + 26
        c.create_line(x1 + 16, 228, x2 - 16, 228, fill=VERDE, dash=(5, 3))
        c.create_text(x1 + 24, 265, text=f"Bolas: {len(pedido['bolas'])}", anchor="w", font=F_NEGRITA, fill=TEXTO)
        pildora(c, x2 - 70, 265, f"Total ${pedido['total']}", (FUENTE, 14, "bold"), "white", CORAL, CORAL)
