import tkinter as tk
from config import *
from interfaz.componentes import *


class PaginaArreglos(tk.Frame):
    def __init__(self, padre, datos):
        tk.Frame.__init__(self, padre)
        self.datos = datos
        self.ultimo = None
        centro = preparar_pagina(self, "Arreglos · Arma tu helado",
                                 f"Elige los sabores bola por bola (máximo {MAX_BOLAS} por cono)")
        centro.columnconfigure(1, weight=1)
        centro.rowconfigure(0, weight=1)

        izq = tarjeta(centro, "Arma tu cono", "El precio de cada sabor ya está puesto")
        izq.grid(row=0, column=0, sticky="n", padx=(0, 16))
        etiqueta_campo(izq, "Sabor de la bola")
        opciones = []
        for sabor, precio in SABORES:
            opciones.append(f"{sabor} - ${precio}")
        self.combo, self.var_sabor = combo(izq, opciones, 24)
        self.combo.pack(fill="x", ipady=3)
        Boton(izq, "Agregar bola", self.agregar_bola, "principal").pack(fill="x", pady=(14, 6))
        Boton(izq, "Quitar última bola", self.quitar_bola, "neutro").pack(fill="x", pady=(0, 6))
        self.lbl_total = tk.Label(izq, text="Total: $0", font=(FUENTE, 16, "bold"),
                                  bg=BLANCO, fg=CORAL)
        self.lbl_total.pack(anchor="w", pady=(10, 10))
        Boton(izq, "Finalizar Helado", self.finalizar, "secundario").pack(fill="x")

        der = tarjeta(centro, "Tu helado")
        der.grid(row=0, column=1, sticky="nsew")
        self.canvas_cono = tk.Canvas(der, width=270, height=420, bg=BLANCO, highlightthickness=0)
        self.canvas_cono.pack(side="left")
        self.canvas_ticket = tk.Canvas(der, height=420, bg=BLANCO, highlightthickness=0)
        self.canvas_ticket.pack(side="left", fill="both", expand=True)
        self.canvas_ticket.bind("<Configure>", self.al_cambiar_tamano)
        self.dibujar_cono()
        self.dibujar_ticket()

    def al_cambiar_tamano(self, evento):
        self.dibujar_ticket()

    def actualizar(self):
        self.refrescar_cono()
        self.dibujar_ticket()

    def refrescar_cono(self):
        self.dibujar_cono()
        self.lbl_total.config(text=f"Total: ${self.datos.cono.total()}")

    def agregar_bola(self):
        try:
            numero = self.combo.current()
            if numero < 0:
                avisar(self.mensaje, "Elige un sabor antes de agregar la bola.", "warn")
                return
            sabor, precio = SABORES[numero]
            lugar = self.datos.cono.agregar(sabor, precio)
            if lugar == -1:
                avisar(self.mensaje, f"El cono ya está lleno ({MAX_BOLAS} bolas). "
                       "Finaliza el helado o quita una bola.", "error")
                return
            self.refrescar_cono()
            avisar(self.mensaje, f"Se agregó una bola de {sabor} (${precio}).", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def quitar_bola(self):
        try:
            bola = self.datos.cono.quitar_ultima()
            if bola is None:
                avisar(self.mensaje, "El cono está vacío, no hay bolas que quitar.", "warn")
                return
            self.refrescar_cono()
            avisar(self.mensaje, f"Se quitó la bola de {bola[0]}.", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def finalizar(self):
        try:
            cono = self.datos.cono
            if len(cono.lista()) == 0:
                avisar(self.mensaje, "Primero agrega al menos una bola al cono.", "warn")
                return
            if len(self.datos.pedidos) >= MAX_PEDIDOS:
                avisar(self.mensaje, f"Se alcanzó el máximo de {MAX_PEDIDOS} pedidos.", "error")
                return
            numero = len(self.datos.pedidos) + 1
            pedido = {
                "folio": f"{numero:03d}",
                "folio_n": numero,
                "bolas": cono.lista(),
                "total": cono.total(),
            }
            self.datos.pedidos.append(pedido)
            self.ultimo = pedido
            cono.vaciar()
            self.refrescar_cono()
            self.dibujar_ticket()
            avisar(self.mensaje, f"Pedido {pedido['folio']} listo: {len(pedido['bolas'])} bola(s), "
                   f"total ${pedido['total']}.", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def dibujar_cono(self):
        c = self.canvas_cono
        c.delete("all")
        c.create_polygon(83, 253, 183, 253, 133, 408, fill=SOMBRA, outline="")
        c.create_polygon(80, 250, 180, 250, 130, 405, fill="#E2B97B", outline="#C89B5B", width=2)
        c.create_line(95, 250, 140, 355, fill="#C89B5B")
        c.create_line(165, 250, 120, 355, fill="#C89B5B")
        c.create_line(93, 290, 167, 290, fill="#C89B5B")
        c.create_line(106, 330, 154, 330, fill="#C89B5B")

        bolas = self.datos.cono.lista()
        if len(bolas) == 0:
            c.create_text(130, 150, text="Agrega bolas\npara armar tu cono", font=F_TEXTO,
                          fill=GRIS, justify="center")
        for i, (sabor, precio) in enumerate(bolas):
            y = 228 - i * 44
            circulo(c, 130, y, 38, COLOR_SABOR[sabor])
            c.create_text(130, y, text=recortar(sabor, 10), font=(FUENTE, 9, "bold"), fill=TEXTO)

    def dibujar_ticket(self):
        c = self.canvas_ticket
        c.delete("all")
        ancho = max(c.winfo_width(), 340)
        x1 = (ancho - 300) / 2
        x2 = x1 + 300
        if self.ultimo is None:
            caja(c, x1, 10, x2, 350, "#FBF7F4", "#CFC3BA", raya=(4, 3))
            c.create_text(ancho / 2, 180, text="Aquí aparecerá el ticket\ncuando finalices un helado",
                          font=F_TEXTO, fill=GRIS, justify="center")
            return
        pedido = self.ultimo
        caja(c, x1, 10, x2, 350, "#FFFDF7", ARENA_OSCURO)
        c.create_text(ancho / 2, 36, text=" HELADERÍA ARTESANAL", font=(FUENTE, 12, "bold"), fill=CHOCOLATE)
        c.create_text(ancho / 2, 60, text="Folio " + pedido["folio"], font=F_MONO, fill=CORAL)
        c.create_line(x1 + 16, 80, x2 - 16, 80, fill=ARENA_OSCURO, dash=(5, 3))
        y = 104
        for sabor, precio in pedido["bolas"]:
            c.create_text(x1 + 22, y, text="1 bola de " + sabor, anchor="w", font=F_TEXTO, fill=TEXTO)
            c.create_text(x2 - 22, y, text=f"${precio}", anchor="e", font=F_NEGRITA, fill=TEXTO)
            y = y + 26
        c.create_line(x1 + 16, 240, x2 - 16, 240, fill=ARENA_OSCURO, dash=(5, 3))
        c.create_text(x1 + 22, 275, text="TOTAL", anchor="w", font=(FUENTE, 13, "bold"), fill=TEXTO)
        pildora(c, x2 - 62, 275, f"${pedido['total']}", (FUENTE, 15, "bold"), "white", CORAL, CORAL)
        c.create_text(ancho / 2, 320, text="¡Gracias por tu compra!", font=F_TEXTO, fill=GRIS)
