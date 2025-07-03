def insertion_sort(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge(arr, l, m, r):
    len1, len2 = m - l + 1, r - m
    left, right = arr[l:m+1], arr[m+1:r+1]
    
    i = j = 0
    k = l
    
    while i < len1 and j < len2:
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    
    while i < len1:
        arr[k] = left[i]
        i += 1
        k += 1
    
    while j < len2:
        arr[k] = right[j]
        j += 1
        k += 1

def tim_sort(arr):
    min_run = 32
    n = len(arr)
    
    # Ordenar subarreglos individuales de tamaño min_run
    for i in range(0, n, min_run):
        insertion_sort(arr, i, min((i + min_run - 1), n - 1))
    
    # Comenzar a fusionar desde min_run
    size = min_run
    while size < n:
        for start in range(0, n, size * 2):
            mid = min((start + size - 1), (n - 1))
            end = min((start + size * 2 - 1), (n - 1))
            merge(arr, start, mid, end)
        size *= 2

# Ejemplo de uso
if __name__ == "__main__":
    datos = [5, 2, 4, 7, 1, 3, 2, 6, -3, 8, 0, 12, 9, 4, 5]
    print("Arreglo original:", datos)
    
    tim_sort(datos)
    print("Arreglo ordenado:", datos)