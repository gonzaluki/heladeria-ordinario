import tkinter as tk
from tkinter import ttk
from config import *
from interfaz.componentes import *

ANCHO_NODO = 132
ALTO_NODO = 112
ESPACIO = 58


def revisar_empresa(texto):
    nombre = " ".join(texto.split())
    if nombre == "":
        return None, "Escribe el nombre de la empresa."
    if len(nombre) < 2:
        return None, "El nombre de la empresa es muy corto."
    if len(nombre) > 24:
        return None, "El nombre de la empresa es muy largo (máximo 24)."
    hay_letra = False
    for letra in nombre:
        if letra.isalpha():
            hay_letra = True
        if not (letra.isalnum() or letra in " .&-"):
            return None, "La empresa solo puede tener letras, números, espacios y . & -"
    if not hay_letra:
        return None, "El nombre de la empresa debe tener letras."
    return nombre, ""


class PaginaLista(tk.Frame):
    def __init__(self, padre, datos):
        tk.Frame.__init__(self, padre)
        self.datos = datos
        centro = preparar_pagina(self, "Lista Circular · Proveedores", "Directorio de proveedores")
        centro.columnconfigure(1, weight=1)
        centro.rowconfigure(0, weight=1)

        izq = tk.Frame(centro, bg=FONDO)
        izq.grid(row=0, column=0, sticky="n", padx=(0, 16))

        registro = tarjeta(izq, "Registrar proveedor")
        registro.pack(fill="x", pady=(0, 10))
        etiqueta_campo(registro, "Empresa")
        self.entrada_empresa, self.var_empresa = entrada(self, registro, 24)
        self.entrada_empresa.pack(fill="x", ipady=6)
        etiqueta_campo(registro, "Insumo")
        self.combo_insumo, self.var_insumo = combo(registro, INSUMOS, 24)
        self.combo_insumo.pack(fill="x", ipady=3)
        etiqueta_campo(registro, "Teléfono (10 dígitos)")
        self.entrada_tel, self.var_tel = entrada(self, registro, 10, True)
        self.entrada_tel.pack(fill="x", ipady=6)
        Boton(registro, "Registrar Proveedor", self.registrar, "principal").pack(fill="x", pady=(14, 0))

        baja = tarjeta(izq, "Dar de baja")
        baja.pack(fill="x", pady=(0, 10))
        self.combo_baja, self.var_baja = combo(baja, [], 24)
        self.combo_baja.pack(fill="x", ipady=3, pady=(6, 0))
        Boton(baja, "Dar de Baja Proveedor", self.dar_de_baja, "peligro").pack(fill="x", pady=(12, 0))

        nav = tarjeta(izq, "Recorrer")
        nav.pack(fill="x")
        fila = tk.Frame(nav, bg=BLANCO)
        fila.pack(fill="x", pady=(8, 0))
        fila.columnconfigure(0, weight=1)
        fila.columnconfigure(1, weight=1)
        Boton(fila, "◄ Anterior", self.ir_anterior, "chocolate").grid(row=0, column=0, sticky="ew", padx=(0, 4))
        Boton(fila, "Siguiente ►", self.ir_siguiente, "chocolate").grid(row=0, column=1, sticky="ew", padx=(4, 0))

        der = tarjeta(centro, "Proveedores")
        der.grid(row=0, column=1, sticky="nsew")
        self.canvas = tk.Canvas(der, height=300, bg=BLANCO, highlightthickness=0)
        self.barra = ttk.Scrollbar(der, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.barra.set)
        self.canvas.pack(fill="both", expand=True)
        self.barra.pack(fill="x")
        self.canvas.bind("<Configure>", self.al_cambiar_tamano)
        self.dibujar()

    def al_cambiar_tamano(self, evento):
        self.dibujar()

    def actualizar(self):
        self.actualizar_baja()
        self.dibujar()

    def actualizar_baja(self):
        opciones = []
        for nodo in self.datos.proveedores.nodos():
            opciones.append(nodo.id_prov + " - " + nodo.empresa)
        self.combo_baja.config(values=opciones)
        if self.var_baja.get() not in opciones:
            self.var_baja.set("")

    def registrar(self):
        try:
            empresa, error = revisar_empresa(self.var_empresa.get())
            if empresa is None:
                avisar(self.mensaje, error, "warn")
                return
            insumo = self.var_insumo.get()
            if insumo not in INSUMOS:
                avisar(self.mensaje, "Elige el insumo que vende el proveedor.", "warn")
                return
            telefono = self.var_tel.get().strip()
            if telefono == "":
                avisar(self.mensaje, "Escribe el teléfono del proveedor.", "warn")
                return
            if len(telefono) != 10:
                avisar(self.mensaje, "El teléfono debe tener exactamente 10 dígitos.", "warn")
                return
            lista = self.datos.proveedores
            if lista.cantidad >= MAX_PROVEEDORES:
                avisar(self.mensaje, f"Ya hay {MAX_PROVEEDORES} proveedores. Da de baja alguno primero.", "error")
                return
            for nodo in lista.nodos():
                if nodo.empresa.lower() == empresa.lower():
                    avisar(self.mensaje, f"Ya existe un proveedor llamado {empresa}.", "warn")
                    return
            nodo = lista.agregar(empresa, insumo, telefono)
            self.var_empresa.set("")
            self.var_tel.set("")
            self.actualizar_baja()
            self.dibujar()
            avisar(self.mensaje, f"Proveedor {nodo.id_prov} ({empresa}) registrado.", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def dar_de_baja(self):
        try:
            lista = self.datos.proveedores
            if lista.esta_vacia():
                avisar(self.mensaje, "No hay proveedores que dar de baja.", "warn")
                return
            elegido = self.var_baja.get()
            if elegido == "":
                avisar(self.mensaje, "Elige el proveedor que quieres dar de baja.", "warn")
                return
            id_prov = elegido.split(" - ")[0]
            nodo = lista.eliminar(id_prov)
            if nodo is None:
                avisar(self.mensaje, "Ese proveedor ya no existe.", "warn")
            else:
                avisar(self.mensaje, f"{nodo.id_prov} ({nodo.empresa}) dado de baja.", "ok")
            self.actualizar_baja()
            self.dibujar()
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def ir_siguiente(self):
        try:
            lista = self.datos.proveedores
            if lista.esta_vacia():
                avisar(self.mensaje, "No hay proveedores. Registra uno primero.", "warn")
                return
            lista.avanzar()
            self.dibujar(True)
            avisar(self.mensaje, "Proveedor actual: " + lista.actual.id_prov + " - " + lista.actual.empresa, "info")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def ir_anterior(self):
        try:
            lista = self.datos.proveedores
            if lista.esta_vacia():
                avisar(self.mensaje, "No hay proveedores. Registra uno primero.", "warn")
                return
            lista.retroceder()
            self.dibujar(True)
            avisar(self.mensaje, "Proveedor actual: " + lista.actual.id_prov + " - " + lista.actual.empresa, "info")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def dibujar(self, centrar_actual=False):
        c = self.canvas
        c.delete("all")
        lista = self.datos.proveedores
        ancho_canvas = max(c.winfo_width(), 560)
        alto_canvas = 300
        nodos = lista.nodos()
        n = len(nodos)
        if n == 0:
            c.config(scrollregion=(0, 0, ancho_canvas, alto_canvas))
            c.create_text(ancho_canvas / 2, alto_canvas / 2, text="Todavía no hay proveedores",
                          font=(FUENTE, 14), fill=GRIS)
            return

        ancho_total = 120 + n * ANCHO_NODO + (n - 1) * ESPACIO
        desfase = max(0, (ancho_canvas - ancho_total) / 2)
        y0 = 70
        xs = []
        for i in range(n):
            xs.append(desfase + 60 + i * (ANCHO_NODO + ESPACIO))

        for i in range(n - 1):
            xa = xs[i] + ANCHO_NODO
            xb = xs[i + 1]
            y = y0 + ALTO_NODO / 2
            c.create_line(xa + 2, y, xb - 2, y, arrow="both", width=2, fill=CHOCOLATE)
            pildora(c, (xa + xb) / 2, y - 16, "⇄", (FUENTE, 11, "bold"), CHOCOLATE, "white", ARENA_OSCURO)

        y_abajo = y0 + ALTO_NODO
        if n == 1:
            x_inicio = xs[0] + ANCHO_NODO / 2 + 28
            x_fin = xs[0] + ANCHO_NODO / 2 - 28
        else:
            x_inicio = xs[n - 1] + ANCHO_NODO / 2
            x_fin = xs[0] + ANCHO_NODO / 2
        c.create_line(x_inicio, y_abajo + 2, x_inicio, y_abajo + 46, (x_inicio + x_fin) / 2, y_abajo + 72,
                      x_fin, y_abajo + 46, x_fin, y_abajo + 2, smooth=True, arrow="both", width=2, fill=VERDE)

        for i, nodo in enumerate(nodos):
            x = xs[i]
            es_actual = (nodo is lista.actual)
            if es_actual:
                caja(c, x, y0, x + ANCHO_NODO, y0 + ALTO_NODO, CORAL_CLARO, CORAL, 3)
                c.create_rectangle(x, y0, x + ANCHO_NODO, y0 + 26, fill=CORAL, outline="")
            else:
                caja(c, x, y0, x + ANCHO_NODO, y0 + ALTO_NODO, BLANCO, BORDE, 1)
                c.create_rectangle(x, y0, x + ANCHO_NODO, y0 + 26, fill=CHOCOLATE, outline="")
            c.create_text(x + 10, y0 + 13, text=nodo.id_prov, anchor="w", font=F_MONO, fill="white")
            c.create_text(x + ANCHO_NODO / 2, y0 + 48, text=recortar(nodo.empresa, 15), font=F_NEGRITA, fill=TEXTO)
            c.create_text(x + ANCHO_NODO / 2, y0 + 72, text=recortar(nodo.insumo, 17), font=(FUENTE, 9), fill=GRIS)
            c.create_text(x + ANCHO_NODO / 2, y0 + 94, text=nodo.telefono, font=("Consolas", 9, "bold"), fill=TEXTO)
            if es_actual:
                pildora(c, x + ANCHO_NODO / 2, y0 - 22, "ACTUAL", F_MONO, "white", CORAL, CORAL)

        c.config(scrollregion=(0, 0, max(ancho_total, ancho_canvas), alto_canvas))

        if centrar_actual and ancho_total > ancho_canvas:
            posicion = nodos.index(lista.actual)
            centro_nodo = desfase + 60 + posicion * (ANCHO_NODO + ESPACIO) + ANCHO_NODO / 2
            fraccion = (centro_nodo - ancho_canvas / 2) / ancho_total
            c.xview_moveto(min(1.0, max(0.0, fraccion)))
