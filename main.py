# Programa principal. Para correrlo:  python main.py
import tkinter as tk
from tkinter import ttk
from config import *
from interfaz.componentes import avisar
from estructuras.datos import Datos
from paginas.menu import PaginaMenu
from paginas.arreglos import PaginaArreglos
from paginas.colas import PaginaColas
from paginas.pilas import PaginaPilas
from paginas.quicksort import PaginaQuickSort
from paginas.binaria import PaginaBinaria
from paginas.lista import PaginaLista
from paginas.arbol import PaginaArbol
from paginas.grafos import PaginaGrafos

OPCIONES_HELADERIA = [
    ("arreglos", "Arreglos"),
    ("colas", "Colas"),
    ("pilas", "Pilas"),
    ("quicksort", "QuickSort"),
    ("binaria", "Búsqueda Binaria"),
    ("lista", "Lista Circular"),
]
OPCIONES_TECH = [
    ("arbol", "Árbol"),
    ("grafos", "Grafos · Kruskal"),
]


class Ventana(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Heladería Artesanal · Estructuras de Datos")
        self.geometry("1340x840")
        self.minsize(1180, 760)
        self.configure(bg=FONDO)
        self.datos = Datos()
        self.actual = "menu"
        self.configurar_estilos()
        self.crear_barra_lateral()

        self.contenedor = tk.Frame(self, bg=FONDO)
        self.contenedor.pack(side="left", fill="both", expand=True)

        self.paginas = {
            "menu": PaginaMenu(self.contenedor, self.datos, self.mostrar),
            "arreglos": PaginaArreglos(self.contenedor, self.datos),
            "colas": PaginaColas(self.contenedor, self.datos),
            "pilas": PaginaPilas(self.contenedor, self.datos),
            "quicksort": PaginaQuickSort(self.contenedor, self.datos),
            "binaria": PaginaBinaria(self.contenedor, self.datos),
            "lista": PaginaLista(self.contenedor, self.datos),
            "arbol": PaginaArbol(self.contenedor, self.datos),
            "grafos": PaginaGrafos(self.contenedor, self.datos),
        }
        for pagina in self.paginas.values():
            pagina.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.mostrar("menu")

    def configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure("TCombobox", fieldbackground="white", background=ARENA,
                         foreground=TEXTO, arrowcolor=CHOCOLATE, bordercolor=BORDE, padding=6)
        estilo.map("TCombobox", fieldbackground=[("readonly", "white")],
                   foreground=[("readonly", TEXTO)],
                   selectbackground=[("readonly", "white")],
                   selectforeground=[("readonly", TEXTO)])
        self.option_add("*TCombobox*Listbox.font", F_TEXTO)

        estilo.configure("Helado.Treeview", background="white", fieldbackground="white",
                         foreground=TEXTO, rowheight=30, borderwidth=0, font=F_TEXTO)
        estilo.configure("Helado.Treeview.Heading", background=ENCABEZADO_TABLA,
                         foreground="white", font=F_NEGRITA, relief="flat", padding=(8, 7))
        estilo.map("Helado.Treeview.Heading", background=[("active", ENCABEZADO_TABLA)])
        estilo.map("Helado.Treeview", background=[("selected", "#FFD9D9")],
                   foreground=[("selected", TEXTO)])

        for nombre in ("Vertical.TScrollbar", "Horizontal.TScrollbar"):
            estilo.configure(nombre, background=ARENA_OSCURO, troughcolor=FILA_IMPAR,
                             bordercolor=FILA_IMPAR, arrowcolor=CHOCOLATE)

    def crear_barra_lateral(self):
        barra = tk.Frame(self, bg=CACAO, width=250)
        barra.pack(side="left", fill="y")
        barra.pack_propagate(False)

        tk.Label(barra, text="Heladería", font=(FUENTE, 18, "bold"), bg=CACAO,
                 fg=TEXTO_CLARO).pack(anchor="w", padx=22, pady=(24, 0))
        tk.Label(barra, text="Estructuras de Datos", font=F_TEXTO, bg=CACAO,
                 fg=TEXTO_APAGADO).pack(anchor="w", padx=24, pady=(0, 18))

        self.filas = {}
        self.agregar_opcion(barra, "menu", "Inicio")

        self.agregar_titulo(barra, "HELADERÍA")
        for clave, texto in OPCIONES_HELADERIA:
            self.agregar_opcion(barra, clave, texto)

        self.agregar_titulo(barra, "ÁRBOLES Y GRAFOS")
        for clave, texto in OPCIONES_TECH:
            self.agregar_opcion(barra, clave, texto)

    def agregar_titulo(self, barra, texto):
        tk.Frame(barra, bg="#4A3745", height=1).pack(fill="x", padx=20, pady=(16, 6))
        tk.Label(barra, text=texto, font=("Consolas", 8, "bold"), bg=CACAO,
                 fg=TEXTO_APAGADO).pack(anchor="w", padx=22, pady=(0, 4))

    def agregar_opcion(self, barra, clave, texto):
        fila = tk.Frame(barra, bg=CACAO)
        fila.pack(fill="x", pady=1)
        franja = tk.Frame(fila, bg=CACAO, width=5)
        franja.pack(side="left", fill="y")
        boton = tk.Button(fila, text=texto, anchor="w", font=(FUENTE, 11), bg=CACAO,
                          fg=TEXTO_CLARO, activebackground=CACAO_HOVER,
                          activeforeground=TEXTO_CLARO, relief="flat", bd=0, padx=16,
                          pady=10, cursor="hand2", command=lambda: self.mostrar(clave))
        boton.pack(side="left", fill="x", expand=True)
        boton.bind("<Enter>", lambda e: self.pasar_mouse(clave, True))
        boton.bind("<Leave>", lambda e: self.pasar_mouse(clave, False))
        self.filas[clave] = (fila, franja, boton)

    def pasar_mouse(self, clave, dentro):
        if clave == self.actual:
            return
        fila, franja, boton = self.filas[clave]
        if dentro:
            color = CACAO_HOVER
        else:
            color = CACAO
        fila.config(bg=color)
        boton.config(bg=color)

    def mostrar(self, clave):
        self.actual = clave
        for nombre, (fila, franja, boton) in self.filas.items():
            if nombre == clave:
                fila.config(bg=CACAO_ACTIVO)
                boton.config(bg=CACAO_ACTIVO, font=(FUENTE, 11, "bold"))
                franja.config(bg=CORAL)
            else:
                fila.config(bg=CACAO)
                boton.config(bg=CACAO, font=(FUENTE, 11))
                franja.config(bg=CACAO)
        pagina = self.paginas[clave]
        pagina.tkraise()
        pagina.actualizar()

    def report_callback_exception(self, tipo, error, rastro):
        try:
            avisar(self.paginas[self.actual].mensaje, "Ocurrió un problema: " + str(error), "error")
        except Exception:
            pass


if __name__ == "__main__":
    Ventana().mainloop()
