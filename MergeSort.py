def merge_sort(arr):
    if len(arr) > 1:
        # Dividir el arreglo en dos mitades
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Llamada recursiva para cada mitad
        merge_sort(left_half)
        merge_sort(right_half)

        # Fusionar las mitades ordenadas
        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Copiar los elementos restantes de left_half (si hay)
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        # Copiar los elementos restantes de right_half (si hay)
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# Ejemplo de uso
if __name__ == "__main__":
    datos = [38, 27, 43, 3, 9, 82, 10]
    print("Arreglo original:", datos)
    
    merge_sort(datos)
    print("Arreglo ordenado:", datos)