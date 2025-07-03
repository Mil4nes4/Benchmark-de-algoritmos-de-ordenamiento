from BubbleSort import bubble_sort
from InsertionSort import insertion_sort
from MergeSort import merge_sort
from QuickSort import quick_sort
from HeapSort import heap_sort
from TimSort import tim_sort

import timeit
import random
import tracemalloc  # Módulo más preciso para medir memoria en Python
import numpy as np  # Para cálculos estadísticos

def generate_random_list(size):
    return [random.randint(0, 10**5) for _ in range(size)]

def generate_sorted_list(size):
    return list(range(size))

def generate_reversed_list(size):
    return list(range(size, 0, -1))

def measure_performance(sort_function, data):
    """
    Versión mejorada para medir memoria usando tracemalloc
    
    Args:
        sort_function (function): Función de ordenamiento a probar
        data (list): Lista de datos a ordenar
        
    Returns:
        tuple: (tiempo_ejecucion, memoria_usada_kb, lista_ordenada)
    """
    # Iniciar el trazado de memoria
    tracemalloc.start()
        
    # Medir tiempo de ejecución
    start_time = timeit.default_timer()
    sorted_data = sort_function(data.copy())
    end_time = timeit.default_timer()
    
    current, peak = tracemalloc.get_traced_memory()   
    
    # Detener el trazado
    tracemalloc.stop()
    memory_used_kb = peak / 1024
    
    execution_time = end_time - start_time
    
    return execution_time, memory_used_kb, sorted_data

def run_benchmark():
    sizes = [100, 1000, 10000] # Tamaños a probar
    list_types = {
        'random': generate_random_list,
        'sorted': generate_sorted_list,
        'reversed': generate_reversed_list
    }
    
    algorithms = {
        "Insertion Sort": insertion_sort,
    }
    
    results = {}
    
    for algo_name, algo_func in algorithms.items():
        results[algo_name] = {}
        for list_type, generator in list_types.items():
            results[algo_name][list_type] = {}
            for size in sizes:
                
                data = generator(size)
                times = []
                memories = []
                
                for _ in range(10):  # 10 repeticiones como en el estudio
                    print(f"Ejecutando {algo_name} con lista {list_type} de tamaño {size}...")
                    time, memory, _ = measure_performance(algo_func, data)
                    times.append(time)
                    memories.append(memory)
                
                # Eliminar outliers (mínimo y máximo)
                if len(times) > 2:  # Solo si hay suficientes datos
                    times_sorted = sorted(times)
                    memories_sorted = sorted(memories)
                    times_filtered = times_sorted[1:-1]
                    memories_filtered = memories_sorted[1:-1]
                else:
                    times_filtered = times
                    memories_filtered = memories
                
                # Calcular estadísticas
                avg_time = np.mean(times_filtered)
                std_time = np.std(times_filtered)
                avg_memory = np.mean(memories_filtered)
                std_memory = np.std(memories_filtered)
                
                results[algo_name][list_type][size] = {
                    'avg_time': avg_time,
                    'std_time': std_time,
                    'avg_memory_kb': avg_memory,
                    'std_memory_kb': std_memory
                }
    
    return results

def print_results(results):
    """Función para mostrar los resultados de forma legible"""
    for algo, algo_data in results.items():
        print(f"\n{'='*50}")
        print(f"RESULTADOS PARA {algo.upper()}")
        print(f"{'='*50}")
        
        for list_type, type_data in algo_data.items():
            print(f"\nTipo de lista: {list_type.upper()}")
            print(f"{'-'*40}")
            print(f"{'Tamaño':<10} | {'Tiempo (s)':<15} | {'Memoria (KB)':<15}")
            print(f"{'-'*40}")
            
            for size, metrics in type_data.items():
                print(f"{size:<10} | {metrics['avg_time']:.6f} ± {metrics['std_time']:.6f} | "
                      f"{metrics['avg_memory_kb']:.6f} ± {metrics['std_memory_kb']:.2f}")

if __name__ == "__main__":
    print("Iniciando pruebas de rendimiento...")
    benchmark_results = run_benchmark()
    print("\nPruebas completadas. Resultados:")
    print_results(benchmark_results)