def insertion_sort(arr):
    # Recorremos desde el segundo elemento hasta el final
    for i in range(1, len(arr)):
        key = arr[i]  # Elemento actual a insertar en su posición correcta
        
        # Movemos los elementos de arr[0..i-1] que son mayores que key
        # a una posición adelante de su posición actual
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key  # Insertamos key en su posición correcta

# Ejemplo de uso
if __name__ == "__main__":
    datos = [12, 11, 13, 5, 6]
    print("Arreglo original:", datos)
    
    insertion_sort(datos)
    print("Arreglo ordenado:", datos)