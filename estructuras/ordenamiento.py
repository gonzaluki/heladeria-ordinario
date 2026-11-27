def particion(lista, bajo, alto):
    pivote = lista[alto]["total"]
    i = bajo - 1
    for j in range(bajo, alto):
        if lista[j]["total"] <= pivote:
            i = i + 1
            lista[i], lista[j] = lista[j], lista[i]
    lista[i + 1], lista[alto] = lista[alto], lista[i + 1]
    return i + 1

def quicksort(lista, bajo, alto):
    if bajo < alto:
        p = particion(lista, bajo, alto)
        quicksort(lista, bajo, p - 1)
        quicksort(lista, p + 1, alto)   
