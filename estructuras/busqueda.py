def busqueda_binaria(pedidos, folio):
    inicio = 0
    fin = len(pedidos) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if pedidos[medio]["folio_n"] == folio:
            return medio
        elif pedidos[medio]["folio_n"] < folio:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1
