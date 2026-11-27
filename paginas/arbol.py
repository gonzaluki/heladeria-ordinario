import math
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from config import *
from interfaz.componentes import *

RADIO = 20
MAX_CARACTERES = 12


class PaginaArbol(tk.Frame):
    def __init__(self, padre, datos):
        tk.Frame.__init__(self, padre)
        self.datos = datos
        self.camino = []
        self.encontrado = None
        self.existe = True
        self.secuencia = []

        centro = preparar_pagina(self, "Árbol Binario de Búsqueda", "Crea, busca y elimina nodos", True)
        centro.columnconfigure(1, weight=1)
        centro.rowconfigure(0, weight=1)

        izq = tarjeta(centro, "Opciones", "Números, letras o símbolos\n(se permiten repetidos)")
        izq.grid(row=0, column=0, sticky="n", padx=(0, 16))
        etiqueta_campo(izq, "Valor")
        self.entrada, self.var_valor = entrada(self, izq, MAX_CARACTERES)
        self.entrada.pack(fill="x", ipady=5)
        self.entrada.bind("<Return>", lambda e: self.crear())
        self.fuente_nodo = tkfont.Font(self, family=FUENTE, size=11, weight="bold")
        Boton(izq, "Crear Nodo", self.crear, "principal").pack(fill="x", pady=(14, 8))
        Boton(izq, "Buscar Nodo", self.buscar, "secundario").pack(fill="x", pady=(0, 8))
        Boton(izq, "Eliminar Nodo", self.eliminar, "peligro").pack(fill="x")
        tk.Frame(izq, bg=BORDE, height=1).pack(fill="x", pady=14)
        tk.Label(izq, text="Recorridos", font=F_NEGRITA, bg=BLANCO, fg=TEXTO).pack(anchor="w")
        Boton(izq, "Preorden", lambda: self.recorrer("Preorden"), "chocolate").pack(fill="x", pady=(8, 0))
        Boton(izq, "Inorden", lambda: self.recorrer("Inorden"), "chocolate").pack(fill="x", pady=(8, 0))
        Boton(izq, "Postorden", lambda: self.recorrer("Postorden"), "chocolate").pack(fill="x", pady=(8, 0))

        der = tk.Frame(centro, bg=FONDO)
        der.grid(row=0, column=1, sticky="nsew")
        der.columnconfigure(0, weight=1)
        der.rowconfigure(0, weight=1)
        arbol_card = tarjeta(der)
        arbol_card.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        leyenda = tk.Frame(arbol_card, bg=BLANCO)
        leyenda.pack(fill="x", pady=(0, 6))
        for color, texto in [(VIOLETA, "Raíz"), (AZUL, "Interno"), (TURQUESA, "Hoja"),
                             (VERDE_BRILLANTE, "Camino de búsqueda"), (AMBAR, "Recorrido")]:
            tk.Label(leyenda, text="●", fg=color, bg=BLANCO, font=(FUENTE, 12)).pack(side="left")
            tk.Label(leyenda, text=texto + "   ", fg=GRIS, bg=BLANCO, font=F_TEXTO).pack(side="left")

        marco = tk.Frame(arbol_card, bg=FONDO_TECH, highlightthickness=1, highlightbackground=BORDE)
        marco.pack(fill="both", expand=True)
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(marco, height=330, bg=FONDO_TECH, highlightthickness=0)
        barra_v = ttk.Scrollbar(marco, orient="vertical", command=self.canvas.yview)
        barra_h = ttk.Scrollbar(marco, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=barra_h.set, yscrollcommand=barra_v.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        barra_v.grid(row=0, column=1, sticky="ns")
        barra_h.grid(row=1, column=0, sticky="ew")
        self.canvas.bind("<Configure>", self.al_cambiar_tamano)

        resultado = tarjeta(der)
        resultado.grid(row=1, column=0, sticky="ew")
        self.lbl_recorrido = tk.Label(resultado, text="Recorrido: —", font=F_MONO, bg=BLANCO, fg=TEXTO,
                                      anchor="w", justify="left", wraplength=650)
        self.lbl_recorrido.pack(fill="x")
        self.dibujar()

    def al_cambiar_tamano(self, evento):
        self.dibujar()

    def actualizar(self):
        self.dibujar()

    def limpiar_resaltado(self):
        self.camino = []
        self.encontrado = None
        self.existe = True
        self.secuencia = []
        self.lbl_recorrido.config(text="Recorrido: —")

    def leer_valor(self):
        # Acepta cualquier número (enteros, negativos o con punto decimal) y, si no es número,
        # lo guarda como texto: letras, palabras o caracteres especiales.
        texto = self.var_valor.get().strip()
        if texto == "":
            return None
        try:
            return int(texto)
        except ValueError:
            pass
        try:
            numero = float(texto)
            if math.isfinite(numero):
                return numero
        except ValueError:
            pass
        return texto

    def crear(self):
        try:
            valor = self.leer_valor()
            if valor is None:
                avisar(self.mensaje, "Escribe un valor (número, letra o símbolo).", "warn")
                return
            self.datos.arbol.insertar(valor)
            self.limpiar_resaltado()
            self.dibujar()
            veces = self.datos.arbol.contar(valor)
            if veces > 1:
                avisar(self.mensaje, f"Nodo {valor} agregado (repetido, ahora hay {veces}; los iguales van a la derecha).", "ok")
            else:
                avisar(self.mensaje, f"Nodo {valor} agregado.", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def buscar(self):
        try:
            valor = self.leer_valor()
            if valor is None:
                avisar(self.mensaje, "Escribe un valor (número, letra o símbolo).", "warn")
                return
            if self.datos.arbol.raiz is None:
                avisar(self.mensaje, "El árbol está vacío. Crea algunos nodos primero.", "warn")
                return
            camino, encontrado = self.datos.arbol.buscar(valor)
            self.limpiar_resaltado()
            self.camino = camino
            self.existe = encontrado
            if encontrado:
                self.encontrado = camino[-1]
            self.dibujar()
            ruta = " → ".join(str(n.valor) for n in camino)
            if encontrado:
                avisar(self.mensaje, f"Nodo {valor} encontrado. Camino: {ruta}", "ok")
            else:
                avisar(self.mensaje, f"El nodo {valor} no existe. Camino recorrido: {ruta}", "warn")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def eliminar(self):
        try:
            valor = self.leer_valor()
            if valor is None:
                avisar(self.mensaje, "Escribe un valor (número, letra o símbolo).", "warn")
                return
            if self.datos.arbol.raiz is None:
                avisar(self.mensaje, "El árbol está vacío, no hay nada que eliminar.", "warn")
                return
            if not self.datos.arbol.eliminar(valor):
                avisar(self.mensaje, f"El nodo {valor} no existe en el árbol.", "warn")
                return
            self.limpiar_resaltado()
            self.dibujar()
            avisar(self.mensaje, f"Nodo {valor} eliminado.", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def recorrer(self, nombre):
        try:
            arbol = self.datos.arbol
            if arbol.raiz is None:
                avisar(self.mensaje, "El árbol está vacío, no hay nada que recorrer.", "warn")
                return
            if nombre == "Preorden":
                lista = arbol.nodos_preorden()
            elif nombre == "Inorden":
                lista = arbol.nodos_inorden()
            else:
                lista = arbol.nodos_postorden()
            self.limpiar_resaltado()
            self.secuencia = lista
            self.lbl_recorrido.config(text=nombre + ": " + " → ".join(str(n.valor) for n in lista))
            self.dibujar()
            avisar(self.mensaje, f"Recorrido {nombre} listo ({len(lista)} nodos).", "info")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def calcular_posiciones(self, nodo, nivel, posiciones, aristas, info):
        # Las posiciones se guardan por nodo y no por valor, así dos nodos con el mismo valor
        # se dibujan cada uno en su lugar.
        if nodo is None:
            return
        self.calcular_posiciones(nodo.izq, nivel + 1, posiciones, aristas, info)
        posiciones[nodo] = (info["contador"], nivel)
        info["contador"] = info["contador"] + 1
        if nivel > info["nivel_max"]:
            info["nivel_max"] = nivel
        self.calcular_posiciones(nodo.der, nivel + 1, posiciones, aristas, info)
        if nodo.izq is not None:
            aristas.append((nodo, nodo.izq))
        if nodo.der is not None:
            aristas.append((nodo, nodo.der))

    def dibujar(self):
        c = self.canvas
        c.delete("all")
        arbol = self.datos.arbol
        ancho_canvas = max(c.winfo_width(), 520)
        alto_canvas = max(c.winfo_height(), 300)
        if arbol.raiz is None:
            c.config(scrollregion=(0, 0, ancho_canvas, alto_canvas))
            c.create_text(ancho_canvas / 2, alto_canvas / 2, text="Árbol vacío\nCrea un nodo para empezar",
                          font=(FUENTE, 14), fill=GRIS, justify="center")
            return

        posiciones = {}
        aristas = []
        info = {"contador": 0, "nivel_max": 0}
        self.calcular_posiciones(arbol.raiz, 0, posiciones, aristas, info)

        # El tamaño del círculo crece si algún valor es largo (por ejemplo 123456 o "fresa").
        ancho_texto = 0
        for nodo in posiciones:
            ancho_texto = max(ancho_texto, self.fuente_nodo.measure(str(nodo.valor)))
        radio = max(RADIO, ancho_texto / 2 + 7)
        separacion_x = max(48, 2 * radio + 8)
        separacion_y = max(74, 2 * radio + 30)
        margen = max(40, radio + 14)
        ancho_arbol = 2 * margen + (info["contador"] - 1) * separacion_x
        desfase = max(0, (ancho_canvas - ancho_arbol) / 2)
        alto_arbol = 2 * margen + info["nivel_max"] * separacion_y + 30

        def coordenadas(nodo):
            columna, nivel = posiciones[nodo]
            return desfase + margen + columna * separacion_x, margen + nivel * separacion_y

        color_camino = VERDE_BRILLANTE
        if not self.existe:
            color_camino = AMBAR

        pares_camino = []
        for i in range(len(self.camino) - 1):
            pares_camino.append((self.camino[i], self.camino[i + 1]))
        for padre, hijo in aristas:
            x1, y1 = coordenadas(padre)
            x2, y2 = coordenadas(hijo)
            if (padre, hijo) in pares_camino:
                c.create_line(x1, y1, x2, y2, fill=color_camino, width=5)
            else:
                c.create_line(x1, y1, x2, y2, fill=GRIS_AZUL, width=2)

        for nodo in posiciones:
            x, y = coordenadas(nodo)
            if nodo in self.camino:
                color = color_camino
            elif nodo is arbol.raiz:
                color = VIOLETA
            elif nodo.izq is None and nodo.der is None:
                color = TURQUESA
            else:
                color = AZUL
            borde = "white"
            grosor = 2
            if nodo is self.encontrado:
                borde = VERDE_FUERTE
                grosor = 4
            if nodo in self.secuencia:
                borde = AMBAR
                grosor = 4
            circulo(c, x, y, radio, color, borde, grosor)
            c.create_text(x, y, text=str(nodo.valor), font=self.fuente_nodo, fill="white")
            if nodo in self.secuencia:
                orden = self.secuencia.index(nodo) + 1
                bx = x + radio - 2
                by = y - radio
                c.create_oval(bx - 10, by - 10, bx + 10, by + 10, fill=AMBAR, outline="white")
                c.create_text(bx, by, text=str(orden), font=("Consolas", 8, "bold"), fill="white")

        c.config(scrollregion=(0, 0, max(ancho_canvas, ancho_arbol + 20), max(alto_canvas, alto_arbol)))
