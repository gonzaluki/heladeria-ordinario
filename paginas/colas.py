import tkinter as tk
from config import *
from interfaz.componentes import *


def revisar_nombre(texto):
    nombre = " ".join(texto.split())
    if nombre == "":
        return None, "Escribe el nombre del cliente."
    if len(nombre) < 2:
        return None, "El nombre es muy corto (mínimo 2 letras)."
    if len(nombre) > 20:
        return None, "El nombre es muy largo (máximo 20 caracteres)."
    if not nombre.replace(" ", "").isalpha():
        return None, "El nombre solo puede tener letras y espacios."
    return nombre, ""


class PaginaColas(tk.Frame):
    def __init__(self, padre, datos):
        tk.Frame.__init__(self, padre)
        self.datos = datos
        centro = preparar_pagina(self, "Colas · Fila de clientes",
                                 f"El primero que llega es el primero que se atiende (máximo {MAX_CLIENTES})")
        centro.columnconfigure(1, weight=1)
        centro.rowconfigure(0, weight=1)

        izq = tk.Frame(centro, bg=FONDO)
        izq.grid(row=0, column=0, sticky="n", padx=(0, 16))
        llegada = tarjeta(izq, "Nueva llegada")
        llegada.pack(fill="x", pady=(0, 12))
        etiqueta_campo(llegada, "Nombre del cliente")
        self.entrada, self.var_nombre = entrada(self, llegada, 20)
        self.entrada.pack(fill="x", ipady=7)
        self.entrada.bind("<Return>", lambda e: self.agregar())
        Boton(llegada, "Agregar a la Fila (Encolar)", self.agregar, "principal").pack(fill="x", pady=(14, 8))
        Boton(llegada, "Atender Cliente (Desencolar)", self.atender, "secundario").pack(fill="x")

        atendiendo = tarjeta(izq, "Atendiendo ahora")
        atendiendo.pack(fill="x")
        self.lbl_atendido = tk.Label(atendiendo, text="—", font=(FUENTE, 14, "bold"),
                                     bg=VERDE_CLARO, fg=VERDE_OSCURO, pady=18, width=20)
        self.lbl_atendido.pack(fill="x", pady=(6, 0))
        self.lbl_fila = tk.Label(atendiendo, text="", font=F_MONO, bg=BLANCO, fg=GRIS)
        self.lbl_fila.pack(anchor="w", pady=(10, 0))

        der = tarjeta(centro, "Fila hacia el mostrador", "El orden sigue la numeración #1, #2, #3...")
        der.grid(row=0, column=1, sticky="nsew")
        self.canvas = tk.Canvas(der, height=330, bg=BLANCO, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.dibujar()

    def actualizar(self):
        self.dibujar()

    def agregar(self):
        try:
            nombre, error = revisar_nombre(self.var_nombre.get())
            if nombre is None:
                avisar(self.mensaje, error, "warn")
                return
            if not self.datos.cola.encolar(nombre):
                avisar(self.mensaje, "La fila está llena (10/10). Atiende a alguien primero.", "error")
                return
            self.var_nombre.set("")
            self.dibujar()
            avisar(self.mensaje, f"{nombre} se formó en la fila (lugar {self.datos.cola.tamano}).", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def atender(self):
        try:
            nombre = self.datos.cola.desencolar()
            if nombre is None:
                avisar(self.mensaje, "No hay clientes en la fila.", "warn")
                return
            self.lbl_atendido.config(text=nombre)
            self.dibujar()
            avisar(self.mensaje, f"Atendiendo a {nombre}, el primero que llegó.", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def dibujar(self):
        c = self.canvas
        c.delete("all")
        cola = self.datos.cola
        clientes = cola.lista()
        self.lbl_fila.config(text=f"En fila: {len(clientes)}/{cola.capacidad}")

        caja(c, 12, 66, 98, 300, CHOCOLATE, CHOCOLATE)
        c.create_text(55, 183, text="MOSTRADOR", angle=90, font=(FUENTE, 12, "bold"), fill="white")

        for i in range(cola.capacidad):
            fila = i // 5
            columna = i % 5
            x = 128 + columna * 124
            y = 86 + fila * 130
            if i >= len(clientes):
                c.create_rectangle(x, y, x + 112, y + 72, outline="#D9CEC6", dash=(4, 3))
                c.create_text(x + 56, y + 36, text="#" + str(i + 1), font=F_TEXTO, fill="#CFC3BA")
                continue

            es_frente = (i == 0)
            es_final = (i == len(clientes) - 1)
            relleno = BLANCO
            borde = BORDE
            if es_final:
                relleno, borde = VERDE_CLARO, VERDE
            if es_frente:
                relleno, borde = CORAL_CLARO, CORAL
            caja(c, x, y, x + 112, y + 72, relleno, borde, 2 if (es_frente or es_final) else 1)
            c.create_text(x + 8, y + 10, text="#" + str(i + 1), anchor="w", font=("Consolas", 9, "bold"), fill=GRIS)
            c.create_text(x + 56, y + 42, text=recortar(clientes[i], 13), font=F_NEGRITA, fill=TEXTO)

            if columna == 0:
                c.create_line(x, y + 36, 100, y + 36, arrow="last", fill=CHOCOLATE, width=2)
            else:
                c.create_line(x, y + 36, x - 12, y + 36, arrow="last", fill=CHOCOLATE, width=2)

            if es_frente and es_final:
                pildora(c, x + 56, y - 14, "FRENTE / FINAL", ("Consolas", 9, "bold"), "white", CHOCOLATE, CHOCOLATE)
            elif es_frente:
                pildora(c, x + 56, y - 14, "FRENTE", ("Consolas", 9, "bold"), "white", CORAL, CORAL)
            elif es_final:
                pildora(c, x + 56, y - 14, "FINAL", ("Consolas", 9, "bold"), "white", VERDE, VERDE)

        if len(clientes) == 0:
            c.create_text(430, 180, text="La fila está vacía", font=(FUENTE, 14), fill=GRIS)
