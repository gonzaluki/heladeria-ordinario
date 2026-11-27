import math
import tkinter as tk
import tkinter.font as tkfont
from config import *
from interfaz.componentes import *

MAX_NOMBRE = 8
RADIO_VERTICE = 24
RADIO_LAZO = 16


class PaginaGrafos(tk.Frame):
    def __init__(self, padre, datos):
        tk.Frame.__init__(self, padre)
        self.datos = datos
        self.aceptadas = []
        self.rechazadas = [] 
        self.calculado = False

        centro = preparar_pagina(self, "Grafos · Kruskal", "Conecta vértices y calcula el camino de menor peso", True)
        centro.columnconfigure(0, weight=1)
        centro.rowconfigure(1, weight=1)

        controles = tarjeta(centro)
        controles.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        fila = tk.Frame(controles, bg=BLANCO)
        fila.pack(fill="x")
        tk.Label(fila, text="Vértice", font=F_TEXTO, bg=BLANCO, fg=GRIS).pack(side="left", padx=(0, 6))
        self.entrada_vertice, self.var_vertice = entrada(self, fila, MAX_NOMBRE)
        self.entrada_vertice.config(width=10)
        self.entrada_vertice.pack(side="left", padx=(0, 8), ipady=5)
        self.entrada_vertice.bind("<Return>", lambda e: self.agregar_vertice())
        Boton(fila, "Agregar Vértice", self.agregar_vertice, "chocolate").pack(side="left", padx=(0, 18))
        tk.Label(fila, text="Origen", font=F_TEXTO, bg=BLANCO, fg=GRIS).pack(side="left", padx=(0, 6))
        self.combo_origen, self.var_origen = combo(fila, [], 6)
        self.combo_origen.pack(side="left", padx=(0, 14), ipady=3)
        tk.Label(fila, text="Destino", font=F_TEXTO, bg=BLANCO, fg=GRIS).pack(side="left", padx=(0, 6))
        self.combo_destino, self.var_destino = combo(fila, [], 6)
        self.combo_destino.pack(side="left", padx=(0, 14), ipady=3)
        tk.Label(fila, text="Peso", font=F_TEXTO, bg=BLANCO, fg=GRIS).pack(side="left", padx=(0, 6))
        self.spin, self.var_peso = spin(fila, range(1, 51), 5)
        self.spin.pack(side="left", padx=(0, 14), ipady=4)
        Boton(fila, "Conectar Arista", self.conectar, "principal").pack(side="left")
        Boton(controles, "Calcular Árbol de Expansión Mínima (Kruskal)", self.calcular,
              "secundario").pack(fill="x", pady=(10, 0))

        grafo_card = tarjeta(centro, "Grafo")
        grafo_card.grid(row=1, column=0, sticky="nsew", padx=(0, 16), pady=(0, 6))
        marco = tk.Frame(grafo_card, bg=FONDO_TECH, highlightthickness=1, highlightbackground=BORDE)
        marco.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(marco, height=330, bg=FONDO_TECH, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.al_cambiar_tamano)

        resultado = tarjeta(centro, "Resultado")
        resultado.grid(row=1, column=1, sticky="nsew", pady=(0, 6))
        tk.Label(resultado, text="Recorrido", font=F_TEXTO, bg=BLANCO, fg=GRIS, anchor="w").pack(fill="x", pady=(8, 2))
        self.lbl_recorrido = tk.Label(resultado, text="—", font=F_MONO, bg=BLANCO, fg=TEXTO, anchor="w",
                                      justify="left", wraplength=260, width=28)
        self.lbl_recorrido.pack(fill="x")
        tk.Label(resultado, text="Peso mínimo", font=F_TEXTO, bg=BLANCO, fg=GRIS, anchor="w").pack(fill="x", pady=(18, 2))
        self.lbl_peso = tk.Label(resultado, text="—", font=(FUENTE, 30, "bold"), bg=BLANCO, fg=ESMERALDA, anchor="w")
        self.lbl_peso.pack(fill="x")
        self.fuente_vertice = tkfont.Font(self, family=FUENTE, size=13, weight="bold")
        self.dibujar()

    def al_cambiar_tamano(self, evento):
        self.dibujar()

    def actualizar(self):
        self.actualizar_combos()
        self.dibujar()

    def actualizar_combos(self):
        vertices = self.datos.grafo.vertices
        self.combo_origen.config(values=vertices)
        self.combo_destino.config(values=vertices)
        if self.var_origen.get() not in vertices:
            self.var_origen.set("")
        if self.var_destino.get() not in vertices:
            self.var_destino.set("")

    def borrar_resultado(self):
        self.calculado = False
        self.aceptadas = []
        self.rechazadas = []
        self.lbl_recorrido.config(text="—")
        self.lbl_peso.config(text="—")

    def agregar_vertice(self):
        try:
            nombre = self.var_vertice.get().strip()
            if nombre == "":
                avisar(self.mensaje, "Escribe el nombre del vértice (por ejemplo A, Z, 7 o Norte).", "warn")
                return
            if not self.datos.grafo.agregar_vertice(nombre):
                avisar(self.mensaje, f"Ya existe un vértice llamado {nombre}.", "warn")
                return
            self.var_vertice.set("")
            self.borrar_resultado()
            self.actualizar_combos()
            self.dibujar()
            avisar(self.mensaje, f"Vértice {nombre} agregado.", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def conectar(self):
        try:
            grafo = self.datos.grafo
            if len(grafo.vertices) == 0:
                avisar(self.mensaje, "Agrega al menos un vértice para conectar.", "warn")
                return
            origen = self.var_origen.get()
            destino = self.var_destino.get()
            if origen == "" or destino == "":
                avisar(self.mensaje, "Elige el vértice de origen y el de destino.", "warn")
                return
            if grafo.existe_arista(origen, destino):
                avisar(self.mensaje, f"La arista {origen}-{destino} ya existe.", "warn")
                return
            peso = int(self.var_peso.get())
            grafo.agregar_arista(origen, destino, peso)
            self.borrar_resultado()
            self.dibujar()
            if origen == destino:
                avisar(self.mensaje, f"Lazo {origen}-{destino} creado con peso {peso} (arista a sí mismo).", "ok")
            else:
                avisar(self.mensaje, f"Arista {origen}-{destino} creada con peso {peso}.", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def calcular(self):
        try:
            grafo = self.datos.grafo
            if len(grafo.aristas) == 0:
                avisar(self.mensaje, "Conecta algunos vértices antes de calcular.", "warn")
                return
            aceptadas, rechazadas, costo, partes = grafo.kruskal()
            self.aceptadas = aceptadas
            self.rechazadas = rechazadas
            self.calculado = True

            recorrido = []
            for origen, destino, peso in aceptadas:
                recorrido.append(f"{origen}-{destino} ({peso})")
            self.lbl_recorrido.config(text=" → ".join(recorrido) if recorrido else "—")
            self.lbl_peso.config(text=str(costo))
            self.dibujar()
            if partes > 1:
                avisar(self.mensaje, f"El grafo no está completamente conectado ({partes} partes). "
                       f"Peso mínimo de lo que sí se conecta: {costo}.", "warn")
            else:
                avisar(self.mensaje, f"Listo. El peso mínimo es {costo}.", "ok")
        except Exception as error:
            avisar(self.mensaje, "Ocurrió un problema: " + str(error), "error")

    def posiciones_vertices(self, ancho, alto, radio_vertice, hay_lazos):
        # Los vértices se acomodan en una elipse que usa todo el lienzo, así caben muchos.
        vertices = self.datos.grafo.vertices
        n = len(vertices)
        centro_x = ancho / 2
        centro_y = alto / 2
        if n == 1:
            return {vertices[0]: (centro_x, centro_y)}
        margen = radio_vertice + 26
        if hay_lazos:
            margen = margen + 2 * RADIO_LAZO + 10
        radio_x = max(60, ancho / 2 - margen)
        radio_y = max(60, alto / 2 - margen)
        posiciones = {}
        for i in range(n):
            angulo = -math.pi / 2 + 2 * math.pi * i / n
            posiciones[vertices[i]] = (centro_x + radio_x * math.cos(angulo), centro_y + radio_y * math.sin(angulo))
        return posiciones

    def direccion_lazo(self, x, y, centro_x, centro_y):
        # El lazo se dibuja hacia afuera del grafo (si solo hay un vértice, hacia arriba).
        dx = x - centro_x
        dy = y - centro_y
        distancia = math.hypot(dx, dy)
        if distancia < 1:
            return 0, -1
        return dx / distancia, dy / distancia

    def lugar_para_peso(self, p1, p2, usados, posiciones):
        mejor = None
        mejor_distancia = -1
        for t in (0.5, 0.38, 0.62, 0.28, 0.72, 0.2, 0.8):
            x = p1[0] + (p2[0] - p1[0]) * t
            y = p1[1] + (p2[1] - p1[1]) * t
            distancia = 999
            for ux, uy in usados:
                distancia = min(distancia, math.hypot(x - ux, y - uy))
            for vx, vy in posiciones.values():
                distancia = min(distancia, math.hypot(x - vx, y - vy))
            if distancia > mejor_distancia:
                mejor = (x, y)
                mejor_distancia = distancia
            if distancia >= 34:
                break
        return mejor

    def dibujar(self):
        c = self.canvas
        c.delete("all")
        grafo = self.datos.grafo
        ancho = max(c.winfo_width(), 400)
        alto = max(c.winfo_height(), 300)
        if len(grafo.vertices) == 0:
            c.create_text(ancho / 2, alto / 2, text="Grafo vacío\nEscribe un nombre y usa «Agregar Vértice»",
                          font=(FUENTE, 14), fill=GRIS, justify="center")
            return

        # El círculo crece si algún nombre es largo.
        ancho_texto = 0
        for nombre in grafo.vertices:
            ancho_texto = max(ancho_texto, self.fuente_vertice.measure(nombre))
        radio_vertice = max(RADIO_VERTICE, ancho_texto / 2 + 8)
        hay_lazos = False
        for origen, destino, peso in grafo.aristas:
            if origen == destino:
                hay_lazos = True
        posiciones = self.posiciones_vertices(ancho, alto, radio_vertice, hay_lazos)

        colores = []
        for origen, destino, peso in grafo.aristas:
            color = GRIS_AZUL
            grosor = 2
            raya = None
            if self.calculado and (origen, destino, peso) in self.aceptadas:
                color = ESMERALDA
                grosor = 6
            elif self.calculado and (origen, destino, peso) in self.rechazadas:
                color = GRIS_ARISTA
                raya = (7, 5)
            colores.append(color)
            x1, y1 = posiciones[origen]
            x2, y2 = posiciones[destino]
            if origen == destino:
                # Lazo: un círculo pegado al vértice, del lado de afuera.
                ux, uy = self.direccion_lazo(x1, y1, ancho / 2, alto / 2)
                distancia = radio_vertice + RADIO_LAZO - 8
                lx = x1 + ux * distancia
                ly = y1 + uy * distancia
                c.create_oval(lx - RADIO_LAZO, ly - RADIO_LAZO, lx + RADIO_LAZO, ly + RADIO_LAZO,
                              outline=color, width=grosor, dash=raya)
            else:
                c.create_line(x1, y1, x2, y2, fill=color, width=grosor, dash=raya, capstyle="round")

        usados = []
        for i, (origen, destino, peso) in enumerate(grafo.aristas):
            if origen == destino:
                x, y = posiciones[origen]
                ux, uy = self.direccion_lazo(x, y, ancho / 2, alto / 2)
                distancia = radio_vertice + 2 * RADIO_LAZO + 4
                lugar = (x + ux * distancia, y + uy * distancia)
            else:
                lugar = self.lugar_para_peso(posiciones[origen], posiciones[destino], usados, posiciones)
            usados.append(lugar)
            pildora(c, lugar[0], lugar[1], str(peso), ("Consolas", 10, "bold"), TEXTO, "white", colores[i])

        for nombre, (x, y) in posiciones.items():
            circulo(c, x, y, radio_vertice, INDIGO, "white", 3)
            c.create_text(x, y, text=nombre, font=self.fuente_vertice, fill="white")
