def heap_sort(arr):
    n = len(arr)
    
    # Construir un max-heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extraer elementos uno por uno
    for i in range(n - 1, 0, -1):
        # Mover la raíz actual al final
        arr[i], arr[0] = arr[0], arr[i]
        # Llamar heapify en el heap reducido
        heapify(arr, i, 0)

def heapify(arr, n, i):
    largest = i  # Inicializar el más grande como raíz
    left = 2 * i + 1
    right = 2 * i + 2
    
    # Verificar si el hijo izquierdo existe y es mayor que la raíz
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # Verificar si el hijo derecho existe y es mayor que el mayor actual
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # Cambiar la raíz si es necesario
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Swap
        # Heapify el subárbol afectado
        heapify(arr, n, largest)

# Ejemplo de uso
if __name__ == "__main__":
    datos = [12, 11, 13, 5, 6, 7]
    print("Arreglo original:", datos)
    
    heap_sort(datos)
    print("Arreglo ordenado:", datos)