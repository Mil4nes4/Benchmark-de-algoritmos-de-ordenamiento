def quick_sortult(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # pi es el índice de partición, arr[pi] está en su lugar correcto
        pi = partition(arr, low, high)
        
        # Ordenar recursivamente los elementos antes y después de la partición
        quick_sortult(arr, low, pi - 1)
        quick_sortult(arr, pi + 1, high)

def partition(arr, low, high):
    # Seleccionamos el pivote (en este caso, el último elemento)
    pivot = arr[high]
    
    # Índice del elemento más pequeño
    i = low - 1
    
    for j in range(low, high):
        # Si el elemento actual es menor o igual al pivote
        if arr[j] <= pivot:
            # Incrementamos el índice del elemento más pequeño
            i += 1
            # Intercambiamos arr[i] y arr[j]
            arr[i], arr[j] = arr[j], arr[i]
    
    # Intercambiamos el pivote con el elemento en i+1
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Ejemplo de uso
if __name__ == "__main__":
    datos = [10, 7, 8, 9, 1, 5]
    print("Arreglo original:", datos)
    
    quick_sortult(datos)
    print("Arreglo ordenado:", datos)