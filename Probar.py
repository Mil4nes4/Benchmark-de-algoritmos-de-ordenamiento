from BubbleSort import bubble_sort
from InsertionSort import insertion_sort
from MergeSort import merge_sort
from QuickSort import quick_sort
from HeapSort import heap_sort
from TimSort import tim_sort

import timeit
import random
import psutil
import os

def generate_random_list(size):
    return [random.randint(0, 10**5) for _ in range(size)]

def generate_sorted_list(size):
    return list(range(size))

def generate_reversed_list(size):
    return list(range(size, 0, -1))

def measure_performanc(sort_function, data):
    """
    Mide el tiempo de ejecución y consumo de memoria de una función de ordenamiento
    
    Args:
        sort_function (function): Función de ordenamiento a probar
        data (list): Lista de datos a ordenar
        
    Returns:
        tuple: (tiempo_ejecucion, memoria_usada, lista_ordenada)
    """
    process = psutil.Process(os.getpid())
    
    # Medición de memoria antes de ejecutar
    mem_before = process.memory_info().rss / (1024)  # MB
    
    # Medición de tiempo
    start_time = timeit.default_timer()
    
    # Ejecutar el algoritmo
    sorted_data = sort_function(data.copy())
    
    # Medición de tiempo
    end_time = timeit.default_timer()
    execution_time = end_time - start_time
    
    # Medición de memoria después de ejecutar
    mem_after = process.memory_info().rss / (1024)  # MB
    memory_used = mem_after - mem_before
    
    return execution_time, memory_used, sorted_data

from memory_profiler import memory_usage
# ...existing code...

def measure_performan(sort_function, data):
    """
    Mide el tiempo de ejecución y consumo de memoria de una función de ordenamiento
    """
    # Medición de tiempo
    start_time = timeit.default_timer()

    # Medición de memoria: obtiene el pico de uso durante la función
    mem_usage, sorted_data = memory_usage(
        (sort_function, (data.copy(),)), retval=True, max_usage=True, interval=0.01
    )

    end_time = timeit.default_timer()
    execution_time = end_time - start_time

    # mem_usage ya está en MB
    memory_used = mem_usage  # MB

    return execution_time, memory_used, sorted_data
# ...existing code...

def measure_performance(sort_function, data):
    """
    Mide el tiempo de ejecución y consumo de memoria de una función de ordenamiento
    """
    def wrapper(data):
        start_time = timeit.default_timer()
        result = sort_function(data)
        end_time = timeit.default_timer()
        return end_time - start_time, result

    # memory_usage ejecuta wrapper y devuelve el pico de memoria y el resultado
    mem_usage, (execution_time, sorted_data) = memory_usage(
        (wrapper, (data.copy(),)), retval=True, max_usage=True, interval=0.01
    )

    # mem_usage ya está en MB
    memory_used = mem_usage  # MB

    return execution_time, memory_used, sorted_data

def run_benchmark():
    """Ejecuta las pruebas de rendimiento para diferentes tamaños y tipos de listas"""
    sizes = [100, 1000, 10000, 100000]  
    list_types = {
        "random": generate_random_list,
        "sorted": generate_sorted_list,
        "reversed": generate_reversed_list
    }
    
    algorithms = {
        "Merge Sort": merge_sort,
    }
    
    results = {}
    
    for algo_name, algo_func in algorithms.items():
        results[algo_name] = {}
        for list_type, generator in list_types.items():
            results[algo_name][list_type] = {}
            for size in sizes:
                # Generar datos
                data = generator(size)
                
                times = []
                memories = []
                
                # Ejecutar 10 veces para obtener un promedio
                for _ in range(10):
                    print(f"Ejecutando {algo_name} con lista {list_type} de tamaño {size}...")
                    time, memory, _ = measure_performance(algo_func, data)
                    times.append(time)
                    memories.append(memory)
                
                # Eliminar outliers (mínimo y máximo)
                times_sorted = sorted(times)
                memories_sorted = sorted(memories)
                
                # Calcular promedio y desviación estándar
                avg_time = sum(times_sorted[1:-1]) / (len(times_sorted)-2)
                avg_memory = sum(memories_sorted[1:-1]) / (len(memories_sorted)-2)
                 
                results[algo_name][list_type][size] = {
                    'avg_time': avg_time,
                    'avg_memory': avg_memory
                }
    
    return results

if __name__ == "__main__":
    benchmark_results = run_benchmark()
    
    for algo, algo_data in benchmark_results.items():
        print(f"\nResultados para {algo}:")
        for list_type, type_data in algo_data.items():
            print(f"\n  Tipo de lista: {list_type}")
            for size, metrics in type_data.items():
                print(f"    Tamaño {size}:")
                print(f"      Tiempo promedio: {metrics['avg_time']:.6f} segundos")
                print(f"      Memoria promedio: {metrics['avg_memory']:.6f} KB")