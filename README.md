# Heladería Artesanal · Estructuras de Datos

## Cómo correrlo
    cd heladeria_proyecto
    python main.py

(Necesita Python 3.8+ con tkinter. En Linux: `sudo apt install python3-tk`.)
No hay que instalar nada con pip.

## Archivos
| Archivo | Qué tiene |
|---|---|
| `main.py` | Ventana principal, menú lateral y estilos |
| `config.py` | Colores, fuentes, sabores con precio e insumos |
| `estructuras/arreglo.py` | Arreglo de tamaño fijo (el cono de helado) |
| `estructuras/cola.py` | Cola circular con frente y final |
| `estructuras/pila.py` | Pila (push, pop, peek) |
| `estructuras/ordenamiento.py` | QuickSort |
| `estructuras/busqueda.py` | Búsqueda binaria |
| `estructuras/lista_circular.py` | Lista circular doblemente ligada |
| `estructuras/arbol.py` | Árbol binario de búsqueda |
| `estructuras/grafo.py` | Grafo y Kruskal (Union-Find) |
| `estructuras/datos.py` | Donde se guardan todos los datos (empiezan vacíos) |
| `interfaz/componentes.py` | Botones, tarjetas, tablas y dibujos que se repiten |
| `paginas/` | Una pantalla por módulo |

## Sobre la carpeta `__pycache__`
Python la crea sola cuando ejecutas el programa (guarda los archivos ya compilados para
abrir más rápido). Es normal y se puede borrar cuando quieras.
