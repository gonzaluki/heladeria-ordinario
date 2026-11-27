import tkinter as tk
from config import *
from interfaz.componentes import *


class PaginaPilas(tk.Frame):
    def __init__(self, padre, datos):
        tk.Frame.__init__(self, padre)
        self.datos = datos
        centro = preparar_pagina(self, "Pilas · Insumos por comprar",
                                 f"Lo último que agregas es lo primero que se quita (máximo {MAX_INSUMOS})")
        centro.columnconfigure(1, weight=1)
        centro.rowconfigure(0, weight=1)

        izq = tarjeta(centro, "Lista de compras", "Elige el insumo que se está acabando")
        izq.grid(row=0, column=0, sticky="n", padx=(0, 16))
        etiqueta_campo(izq, "Insumo")
        self.combo, self.var_insumo = combo(izq, INSUMOS, 24)
        self.combo.pack(fill="x", ipady=3)
        Boton(izq, "Agregar a la lista (Push)", self.agregar, "principal").pack(fill="x", pady=(16, 8))
        Boton(izq, "Quitar el último (Pop)", self.quitar, "peligro").pack(fill="x")
        self.lbl_cantidad = tk.Label(izq, text="", font=F_MONO, bg=BLANCO, fg=GRIS)
        self.lbl_cantidad.pack(anchor="w", pady=(14, 0))

        der = tarjeta(centro, "Pila de insumos", "El de arriba es el último que se agregó")
        der.grid(row=0, column=1, sticky="nsew")
        self.canvas = tk.Canvas(der, height=420, bg=BLANCO, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.al_cambiar_tamano)
        self.dibujar()

    def al_cambiar_tamano(self, evento):
        self.dibujar()

    def actualizar(self):
        self.dibujar()

    def agregar(self):
        try:
            insumo = self.var_insumo.get()
            if insumo not in INSUMOS:
                avisar(self.mensaje, "Elige un insumo de la lista.", "warn")
                return
            if insumo in self.datos.pila.lista():
                avisar(self.mensaje, f"{insumo} ya está en la lista de compras.", "warn")
                return
            if not self.datos.pila.push(insumo):
                avisar(self.mensaje, f"La pila está llena ({MAX_INSUMOS}/{MAX_INSUMOS}). Quita un insumo primero.", "error")
                return
            self.dibujar()
            avisar(self.mensaje, f"{insumo} se agregó a la lista (ahora está en el tope).", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def quitar(self):
        try:
            insumo = self.datos.pila.pop()
            if insumo is None:
                avisar(self.mensaje, "La pila está vacía, no hay nada que quitar.", "warn")
                return
            self.dibujar()
            avisar(self.mensaje, f"Se quitó {insumo} de la lista.", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def dibujar(self):
        c = self.canvas
        c.delete("all")
        pila = self.datos.pila
        insumos = pila.lista()
        self.lbl_cantidad.config(text=f"Insumos: {len(insumos)}/{pila.capacidad}")

        ancho = max(c.winfo_width(), 560)
        alto = max(c.winfo_height(), 420)
        centro_x = ancho / 2 - 50
        base = alto - 34
        alto_bloque = 38
        separacion = 5

        c.create_rectangle(centro_x - 200, base - pila.capacidad * (alto_bloque + separacion) - 6,
                           centro_x + 200, base + 6, outline=ARENA_OSCURO, width=2)
        caja(c, centro_x - 214, base + 6, centro_x + 214, base + 18, CHOCOLATE, CHOCOLATE)

        for i in range(pila.capacidad):
            y2 = base - i * (alto_bloque + separacion)
            y1 = y2 - alto_bloque
            x1 = centro_x - 190
            x2 = centro_x + 190
            if i < len(insumos):
                es_tope = (i == len(insumos) - 1)
                if es_tope:
                    caja(c, x1, y1, x2, y2, CORAL_CLARO, CORAL, 3)
                else:
                    caja(c, x1, y1, x2, y2, "#FFF1E6", "#F2C9A8", 1)
                c.create_text(centro_x, (y1 + y2) / 2, text=insumos[i], font=F_NEGRITA, fill=TEXTO)
            else:
                c.create_rectangle(x1, y1, x2, y2, outline="#D9CEC6", dash=(4, 3))
            c.create_text(x1 - 12, (y1 + y2) / 2, text=str(i + 1), anchor="e", font=("Consolas", 9), fill=GRIS)

        if len(insumos) > 0:
            y = base - (len(insumos) - 1) * (alto_bloque + separacion) - alto_bloque / 2
            c.create_line(centro_x + 262, y, centro_x + 204, y, arrow="last", width=3, fill=CORAL)
            pildora(c, centro_x + 296, y, "TOPE", F_MONO, "white", CORAL, CORAL)
        else:
            c.create_text(centro_x, alto / 2 - 20, text="La pila está vacía", font=(FUENTE, 14), fill=GRIS)
