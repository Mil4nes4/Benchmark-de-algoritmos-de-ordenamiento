def bubble_sort(arr):
    """
    Implementación clásica del algoritmo Bubble Sort.
    
    Args:
        arr (list): Lista de elementos a ordenar (enteros en este caso)
        
    Returns:
        list: Lista ordenada
    """
    n = len(arr)
    # Realizamos n-1 pasadas
    for i in range(n-1):
        # En cada pasada, comparamos elementos adyacentes
        for j in range(0, n-i-1):
            # Si el elemento actual es mayor que el siguiente, los intercambiamos
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def optimized_bubble_sort(arr):
    """
    Versión optimizada de Bubble Sort que detecta si la lista ya está ordenada.
    
    Args:
        arr (list): Lista de elementos a ordenar
        
    Returns:
        list: Lista ordenada
    """
    n = len(arr)
    for i in range(n-1):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        # Si no hubo intercambios en la pasada completa, la lista ya está ordenada
        if not swapped:
            break
    return arr

if __name__ == "__main__":
    # Ejemplo de uso
    lista = [64, 34, 25, 12, 22, 11, 90]
    print("Lista original:", lista)
    lista_ordenada = bubble_sort(lista)
    print("Lista ordenada:", lista_ordenada)