import sys
import tkinter as tk
from tkinter import ttk
from config import *


class BotonMac(tk.Label):
    # En macOS, tk.Button ignora el color de fondo (bg) y siempre pinta el botón gris del
    # sistema, así que el texto blanco casi no se ve. En Mac el botón se arma con un Label,
    # que sí respeta los colores, y se le agrega el clic a mano.
    def __init__(self, padre, command=None, **opciones):
        tk.Label.__init__(self, padre, **opciones)
        self.comando = command
        self.bind("<ButtonRelease-1>", self.al_soltar_clic)

    def al_soltar_clic(self, evento):
        # Igual que un botón normal: solo cuenta si se suelta el clic encima del botón.
        if self.comando and self.winfo_containing(evento.x_root, evento.y_root) is self:
            self.comando()


if sys.platform == "darwin":
    BotonBase = BotonMac
else:
    BotonBase = tk.Button

COLORES_BOTON = {
    "principal": (CORAL, CORAL_OSCURO, "white"),
    "secundario": (VERDE, VERDE_OSCURO, "white"),
    "peligro": (ROJO, ROJO_OSCURO, "white"),
    "chocolate": (CHOCOLATE, CHOCOLATE_OSCURO, "white"),
    "neutro": (ARENA, ARENA_OSCURO, TEXTO),
}

COLORES_MENSAJE = {
    "ok": ("#E3F6F1", "#1F7A6D", "✔"),
    "warn": ("#FFF4D6", "#8A5A00", "⚠"),
    "error": ("#FDE8E8", "#A12626", "✖"),
    "info": ("#EAF0FA", "#2B4A7A", "ℹ"),
}

class Boton(BotonBase):
    def __init__(self, padre, texto, comando, tipo="principal"):
        color, hover, letra = COLORES_BOTON[tipo]
        BotonBase.__init__(self, padre, text=texto, command=comando, bg=color, fg=letra,
                           activebackground=hover, activeforeground=letra, relief="flat",
                           bd=0, cursor="hand2", padx=14, pady=8, font=F_NEGRITA)
        self.color_normal = color
        self.color_hover = hover
        self.bind("<Enter>", self.al_entrar)
        self.bind("<Leave>", self.al_salir)

    def al_entrar(self, evento):
        self.config(bg=self.color_hover)

    def al_salir(self, evento):
        self.config(bg=self.color_normal)

def avisar(etiqueta, texto, tipo="info"):
    fondo, letra, icono = COLORES_MENSAJE[tipo]
    etiqueta.config(text=icono + "  " + texto, bg=fondo, fg=letra)

def preparar_pagina(pagina, titulo, subtitulo, tech=False):
    pagina.config(bg=FONDO)
    arriba = tk.Frame(pagina, bg=FONDO)
    arriba.pack(fill="x", padx=24, pady=(18, 8))
    fila = tk.Frame(arriba, bg=FONDO)
    fila.pack(anchor="w")
    tk.Label(fila, text=titulo, font=F_TITULO, bg=FONDO, fg=TEXTO).pack(side="left")
    if tech:
        tk.Label(fila, text=" TECH ", font=("Consolas", 9, "bold"), bg=INDIGO,
                 fg="white").pack(side="left", padx=10)
    tk.Label(arriba, text=subtitulo, font=F_SUB, bg=FONDO, fg=GRIS).pack(anchor="w")

    pagina.mensaje = tk.Label(pagina, text="", font=F_NEGRITA, anchor="w", justify="left",
                              padx=16, pady=10, wraplength=800, highlightthickness=1,
                              highlightbackground=BORDE)
    pagina.mensaje.pack(side="bottom", fill="x", padx=24, pady=(6, 16))
    avisar(pagina.mensaje, "Listo para usar.", "info")

    centro = tk.Frame(pagina, bg=FONDO)
    centro.pack(fill="both", expand=True, padx=24)
    return centro

def tarjeta(padre, titulo=None, subtitulo=None):
    t = tk.Frame(padre, bg=BLANCO, highlightthickness=1, highlightbackground=BORDE,
                 padx=20, pady=15)
    if titulo:
        tk.Label(t, text=titulo, font=F_TARJETA, bg=BLANCO, fg=TEXTO, anchor="w").pack(fill="x")
    if subtitulo:
        tk.Label(t, text=subtitulo, font=F_TEXTO, bg=BLANCO, fg=GRIS, anchor="w",
                 justify="left").pack(fill="x", pady=(0, 8))
    return t

def etiqueta_campo(padre, texto):
    tk.Label(padre, text=texto, font=F_TEXTO, bg=BLANCO, fg=GRIS,
             anchor="w").pack(fill="x", pady=(10, 3))

def combo(padre, valores, ancho=28):
    variable = tk.StringVar()
    c = ttk.Combobox(padre, textvariable=variable, values=valores, state="readonly",
                     width=ancho, font=F_TEXTO)
    return c, variable

def spin(padre, valores, ancho=8):
    variable = tk.StringVar()
    lista = tuple(str(v) for v in valores)
    s = tk.Spinbox(padre, values=lista, textvariable=variable, width=ancho, font=F_TEXTO,
                   justify="center", relief="flat", highlightthickness=1,
                   highlightbackground=BORDE, highlightcolor=CORAL, buttonbackground=ARENA,
                   readonlybackground="white", wrap=False)
    variable.set(lista[0])
    s.config(state="readonly")
    return s, variable

def entrada(pagina, padre, maximo, solo_numeros=False):
    def permitir(texto):
        if len(texto) > maximo:
            return False
        if solo_numeros:
            for letra in texto:
                if letra not in "0123456789":
                    return False
        return True

    variable = tk.StringVar()
    campo = tk.Entry(padre, textvariable=variable, font=F_TEXTO, relief="flat", bg="white",
                     fg=TEXTO, insertbackground=TEXTO, highlightthickness=1,
                     highlightbackground=BORDE, highlightcolor=CORAL, validate="key",
                     validatecommand=(pagina.register(permitir), "%P"))
    return campo, variable

def tabla(padre, columnas, alto=6):
    marco = tk.Frame(padre, bg=BLANCO)
    nombres = [c[0] for c in columnas]
    t = ttk.Treeview(marco, columns=nombres, show="headings", height=alto,
                     style="Helado.Treeview")
    for nombre, ancho, alineacion in columnas:
        t.heading(nombre, text=nombre)
        t.column(nombre, width=ancho, anchor=alineacion)
    t.tag_configure("par", background=FILA_PAR)
    t.tag_configure("impar", background=FILA_IMPAR)
    barra = ttk.Scrollbar(marco, orient="vertical", command=t.yview)
    t.configure(yscrollcommand=barra.set)
    t.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    return marco, t

def llenar_tabla(t, filas):
    for item in t.get_children():
        t.delete(item)
    for i, fila in enumerate(filas):
        if i % 2 == 0:
            t.insert("", "end", values=fila, tags=("par",))
        else:
            t.insert("", "end", values=fila, tags=("impar",))

def recortar(texto, largo):
    if len(texto) <= largo:
        return texto
    return texto[:largo - 1] + "…"

def caja(c, x1, y1, x2, y2, relleno=BLANCO, borde=BORDE, grosor=1, raya=None):
    c.create_rectangle(x1 + 3, y1 + 3, x2 + 3, y2 + 3, fill=SOMBRA, outline="")
    c.create_rectangle(x1, y1, x2, y2, fill=relleno, outline=borde, width=grosor, dash=raya)


def circulo(c, x, y, r, relleno, borde="white", grosor=2):
    c.create_oval(x - r + 3, y - r + 3, x + r + 3, y + r + 3, fill=SOMBRA, outline="")
    c.create_oval(x - r, y - r, x + r, y + r, fill=relleno, outline=borde, width=grosor)


def pildora(c, x, y, texto, fuente=F_NEGRITA, letra=TEXTO, relleno="white", borde=BORDE):
    t = c.create_text(x, y, text=texto, font=fuente, fill=letra)
    area = c.bbox(t)
    if area:
        r = c.create_rectangle(area[0] - 7, area[1] - 3, area[2] + 7, area[3] + 3,
                               fill=relleno, outline=borde)
        c.tag_lower(r, t)
