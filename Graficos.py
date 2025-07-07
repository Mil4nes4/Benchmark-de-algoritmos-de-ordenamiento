import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_benchmark_results(results):
    """
    Función para graficar los resultados del benchmark de algoritmos de ordenamiento.
    
    Args:
        results (dict): Diccionario con los resultados del benchmark en la estructura:
                       {
                           "Algoritmo": {
                               "tipo_lista": {
                                   "tamaño": {
                                       'avg_time': float,
                                       'std_time': float,
                                       'avg_memory_kb': float,
                                       'std_memory_kb': float
                                   }
                               }
                           }
                       }
    """
    
    # Configuración general de los gráficos
    plt.style.use('seaborn-v0_8')
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12
    
    # Tipos de listas y tamaños
    list_types = ['random', 'sorted', 'reversed']
    sizes = [100, 1000, 10000, 100000]
    
    # Algoritmos a comparar (deberían coincidir con los del benchmark)
    algorithms = ["MergeSort", "QuickSort", "HeapSort", "TimSort"]
    
    # Verificar qué algoritmos están realmente en los resultados
    available_algorithms = [algo for algo in algorithms if algo in results]
    
    # Colores para cada algoritmo
    colors = plt.cm.tab10(np.linspace(0, 1, len(available_algorithms)))
    
    # =====================================================================
    # Gráfico 1: Tiempo de ejecución por tamaño de lista (promedio de los 3 tipos)
    # =====================================================================
    plt.figure(figsize=(14, 8))
    
    for algo, color in zip(available_algorithms, colors):
        avg_times = []
        std_times = []
        
        for size in sizes:
            # Calcular promedio entre los tipos de lista para este tamaño
            times = []
            stds = []
            for list_type in list_types:
                if list_type in results[algo] and size in results[algo][list_type]:
                    times.append(results[algo][list_type][size]['avg_time'])
                    stds.append(results[algo][list_type][size]['std_time'])
            
            if times:  # Si hay datos para este tamaño
                avg_times.append(np.mean(times))
                std_times.append(np.sqrt(sum(s**2 for s in stds)) / len(stds))  # Promedio de varianzas
        
        if avg_times:  # Solo graficar si hay datos
            plt.errorbar(sizes[:len(avg_times)], avg_times, yerr=std_times, 
                        label=algo, color=color, marker='o', linestyle='-', 
                        linewidth=2, markersize=8, capsize=5)
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Tamaño de la lista (elementos) - Escala logarítmica')
    plt.ylabel('Tiempo promedio de ejecución (s) - Escala logarítmica')
    plt.title('Comparación de Tiempo de Ejecución por Algoritmo\n(Promedio de todos los tipos de listas)')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.show()
    
    # =====================================================================
    # Gráfico 2: Memoria utilizada por tamaño de lista (promedio de los 3 tipos)
    # =====================================================================
    plt.figure(figsize=(14, 8))
    
    for algo, color in zip(available_algorithms, colors):
        avg_memories = []
        std_memories = []
        
        for size in sizes:
            # Calcular promedio entre los tipos de lista para este tamaño
            memories = []
            stds = []
            for list_type in list_types:
                if list_type in results[algo] and size in results[algo][list_type]:
                    memories.append(results[algo][list_type][size]['avg_memory_kb'])
                    stds.append(results[algo][list_type][size]['std_memory_kb'])
            
            if memories:  # Si hay datos para este tamaño
                avg_memories.append(np.mean(memories))
                std_memories.append(np.sqrt(sum(s**2 for s in stds)) / len(stds))  # Promedio de varianzas
        
        if avg_memories:  # Solo graficar si hay datos
            plt.errorbar(sizes[:len(avg_memories)], avg_memories, yerr=std_memories, 
                        label=algo, color=color, marker='s', linestyle='--', 
                        linewidth=2, markersize=8, capsize=5)
    
    plt.xscale('log')
    plt.xlabel('Tamaño de la lista (elementos) - Escala logarítmica')
    plt.ylabel('Memoria promedio utilizada (KB)')
    plt.title('Comparación de Memoria Utilizada por Algoritmo\n(Promedio de todos los tipos de listas)')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.show()
    
    # =====================================================================
    # Gráfico 3: Comparación por tipo de lista (para el mayor tamaño disponible)
    # =====================================================================
    max_size = max(sizes)
    
    for list_type in list_types:
        plt.figure(figsize=(14, 6))
        
        # Verificar si este tamaño existe para este tipo de lista en algún algoritmo
        has_data = False
        for algo in available_algorithms:
            if list_type in results[algo] and max_size in results[algo][list_type]:
                has_data = True
                break
        
        if not has_data:
            # Buscar el mayor tamaño que tenga datos
            for size in sorted(sizes, reverse=True):
                has_data = False
                for algo in available_algorithms:
                    if list_type in results[algo] and size in results[algo][list_type]:
                        has_data = True
                        max_size = size
                        break
                if has_data:
                    break
        
        if has_data:
            # Gráfico de tiempo
            plt.subplot(1, 2, 1)
            for algo, color in zip(available_algorithms, colors):
                if list_type in results[algo] and max_size in results[algo][list_type]:
                    data = results[algo][list_type][max_size]
                    plt.bar(algo, data['avg_time'], color=color, 
                            yerr=data['std_time'], capsize=5)
            plt.ylabel('Tiempo de ejecución (s)')
            plt.title(f'Tiempo - {list_type.capitalize()} (n={max_size})')
            plt.xticks(rotation=45)
            
            # Gráfico de memoria
            plt.subplot(1, 2, 2)
            for algo, color in zip(available_algorithms, colors):
                if list_type in results[algo] and max_size in results[algo][list_type]:
                    data = results[algo][list_type][max_size]
                    plt.bar(algo, data['avg_memory_kb'], color=color, 
                            yerr=data['std_memory_kb'], capsize=5)
            plt.ylabel('Memoria utilizada (KB)')
            plt.title(f'Memoria - {list_type.capitalize()} (n={max_size})')
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.show()
    
    # =====================================================================
    # Gráfico 4: Heatmap de tiempos por algoritmo y tamaño (para listas aleatorias)
    # =====================================================================
    if 'random' in list_types:
        # Preparar datos para el heatmap
        heatmap_data = []
        for algo in available_algorithms:
            row = []
            for size in sizes:
                if 'random' in results[algo] and size in results[algo]['random']:
                    row.append(results[algo]['random'][size]['avg_time'])
                else:
                    row.append(np.nan)
            heatmap_data.append(row)
        
        # Crear DataFrame para el heatmap
        df = pd.DataFrame(heatmap_data, index=available_algorithms, columns=sizes)
        
        # Filtrar columnas con al menos un valor no nulo
        df = df.loc[:, df.notna().any(axis=0)]
        
        if not df.empty:
            plt.figure(figsize=(12, 8))
            plt.imshow(df, cmap='viridis', aspect='auto', norm='log')
            plt.colorbar(label='Tiempo (s) - Escala logarítmica')
            plt.xticks(range(len(df.columns)), df.columns)
            plt.yticks(range(len(df.index)), df.index)
            plt.xlabel('Tamaño de la lista')
            plt.ylabel('Algoritmo')
            plt.title('Heatmap de Tiempos de Ejecución\n(Listas Aleatorias)')
            
            # Añadir anotaciones
            for i in range(len(df.index)):
                for j in range(len(df.columns)):
                    if not np.isnan(df.iloc[i, j]):
                        plt.text(j, i, f"{df.iloc[i, j]:.4f}", 
                                ha="center", va="center", color="w", fontsize=8)
            
            plt.show()

def load_results_from_file(filename):
    """
    Función para cargar resultados desde un archivo (simulada, deberías implementar
    según cómo guardes tus resultados reales)
    """
    # Esto es un ejemplo - deberías adaptarlo a cómo guardes tus datos
    import json
    with open(filename, 'r') as f:
        results = json.load(f)
    return results

def plot_algorithms_by_size(results, sizes, list_types):
    import matplotlib.pyplot as plt
    import numpy as np

    algorithms = [algo for algo in results.keys()]
    colors = plt.cm.tab10(np.linspace(0, 1, len(algorithms)))

    for list_type in list_types:
        for size in sizes:
            avg_times = []
            std_times = []
            for algo in algorithms:
                if list_type in results[algo] and size in results[algo][list_type]:
                    avg_times.append(results[algo][list_type][size]['avg_time'])
                    std_times.append(results[algo][list_type][size]['std_time'])
                else:
                    avg_times.append(np.nan)
                    std_times.append(0)
            plt.figure(figsize=(10, 6))
            plt.errorbar(algorithms, avg_times, yerr=std_times, fmt='-o', color='b', capsize=5)
            plt.ylabel('Tiempo promedio de ejecución (s)')
            plt.xlabel('Algoritmo')
            plt.title(f'Tiempo de ejecución para tamaño {size} ({list_type})')
            plt.grid(True, linestyle='--')
            plt.tight_layout()
            plt.show()

if __name__ == "__main__":
    # Ejemplo de uso:
    # 1. Ejecutar el benchmark y guardar resultados
    # benchmark_results = run_benchmark()
    
    # 2. Cargar resultados desde archivo (si ya los tienes guardados)
    # benchmark_results = load_results_from_file('benchmark_results.json')
    
    # 3. Para este ejemplo, crearemos datos de prueba
    benchmark_results = {
        "BubbleSort": {
            "random": {
                100: {"avg_time": 0.000484, "std_time": 0.000026, "avg_memory_kb": 0.890625, "std_memory_kb": 0.0},
                1000: {"avg_time": 0.642172, "std_time": 0.033457, "avg_memory_kb": 8.074219, "std_memory_kb": 0.0},
                10000: {"avg_time": 83.775204, "std_time": 1.962586, "avg_memory_kb": 78.386719, "std_memory_kb": 0.0}
            },
            "sorted": {
                100: {"avg_time": 0.000292, "std_time": 0.000015, "avg_memory_kb": 0.890625, "std_memory_kb": 0.0},
                1000: {"avg_time": 0.300863, "std_time": 0.004979, "avg_memory_kb": 8.074219, "std_memory_kb": 0.0},
                10000: {"avg_time": 50.554899, "std_time": 0.220369, "avg_memory_kb": 78.386719, "std_memory_kb": 0.0}
            },
            "reversed": {
                100: {"avg_time": 0.000717, "std_time": 0.000177, "avg_memory_kb": 0.890625, "std_memory_kb": 0.0},
                1000: {"avg_time": 0.668613, "std_time": 0.004676, "avg_memory_kb": 8.074219, "std_memory_kb": 0.0},
                10000: {"avg_time": 112.233900, "std_time": 0.940154, "avg_memory_kb": 78.386719, "std_memory_kb": 0.0}
            }
        },
        "InsertionSort": {
           "random": {
                100: {"avg_time": 0.000162, "std_time": 0.000009, "avg_memory_kb": 0.859375, "std_memory_kb": 0.0},
                1000: {"avg_time": 0.237254, "std_time": 0.003641, "avg_memory_kb": 7.949219, "std_memory_kb": 0.0},
                10000: {"avg_time": 29.798460, "std_time": 0.313564, "avg_memory_kb": 78.261719, "std_memory_kb": 0.0}
            },
            "sorted": {
                100: {"avg_time": 0.000023,"std_time": 0.000003,"avg_memory_kb": 0.859375,"std_memory_kb": 0.0},
                1000: {"avg_time": 0.001905,"std_time": 0.000478,"avg_memory_kb": 7.949219,"std_memory_kb": 0.0},
                10000: {"avg_time": 0.021720,"std_time": 0.001732,"avg_memory_kb": 78.261719,"std_memory_kb": 0.0}
            },
            "reversed": {
                100: {"avg_time": 0.001174,"std_time": 0.000348,"avg_memory_kb": 0.859375,"std_memory_kb": 0.0},
                1000: {"avg_time": 0.369291,"std_time": 0.024555,"avg_memory_kb": 7.949219,"std_memory_kb": 0.0},
                10000: {"avg_time": 56.562833,"std_time": 1.256957,"avg_memory_kb": 78.261719,"std_memory_kb": 0.0
                }
            }
        },
        "MergeSort": {
            "random": {
                100: {"avg_time": 0.000243, "std_time": 0.000002, "avg_memory_kb": 2.351562 , "std_memory_kb": 0},
                1000: {"avg_time": 0.008943, "std_time": 0.002753, "avg_memory_kb": 23.468750 , "std_memory_kb": 0},
                10000: {"avg_time": 0.191314 , "std_time": 0.004404, "avg_memory_kb": 234.562500, "std_memory_kb": 0},
                100000: {"avg_time": 2.972735, "std_time": 0.035711 , "avg_memory_kb": 2344.039062, "std_memory_kb": 0}
            },
            "sorted": {
                100: {"avg_time": 0.000315, "std_time": 0.000040, "avg_memory_kb": 2.351562 , "std_memory_kb": 0},
                1000: {"avg_time": 0.006458, "std_time": 0.000398, "avg_memory_kb": 23.468750 , "std_memory_kb": 0},
                10000: {"avg_time": 0.177929 , "std_time": 0.001913, "avg_memory_kb": 234.562500, "std_memory_kb": 0},
                100000: {"avg_time": 2.902670, "std_time": 0.032817 , "avg_memory_kb": 2344.039062, "std_memory_kb": 0}
            },
            "reversed": {
                100: {"avg_time": 0.000229, "std_time": 0.000026, "avg_memory_kb": 2.351562 , "std_memory_kb": 0},
                1000: {"avg_time": 0.005984, "std_time": 0.000371, "avg_memory_kb": 23.468750 , "std_memory_kb": 0},
                10000: {"avg_time": 0.168747  , "std_time": 0.001714, "avg_memory_kb": 234.562500, "std_memory_kb": 0},
                100000: {"avg_time": 2.778870, "std_time": 0.032016 , "avg_memory_kb": 2344.039062, "std_memory_kb": 0}
            }
        },
        "QuickSort": {
            "random": {
                100: {"avg_time": 0.000166, "std_time": 0.000029, "avg_memory_kb": 0.859375 , "std_memory_kb": 0},
                1000: {"avg_time": 0.011089, "std_time": 0.000258, "avg_memory_kb": 9.140625 , "std_memory_kb": 0},
                10000: {"avg_time": 0.155275 , "std_time": 0.001894, "avg_memory_kb": 80.031250, "std_memory_kb": 0},
                100000: {"avg_time": 2.051004, "std_time": 0.028696 , "avg_memory_kb": 783.656250, "std_memory_kb": 0}
            },
            "sorted": {
                100: {"avg_time": 0.000145, "std_time": 0.000003, "avg_memory_kb": 0.859375 , "std_memory_kb": 0},
                1000: {"avg_time": 0.009682, "std_time": 0.000333, "avg_memory_kb": 8.500000 , "std_memory_kb": 0},
                10000: {"avg_time": 0.143817 , "std_time": 0.000952, "avg_memory_kb": 79.046875, "std_memory_kb": 0},
                100000: {"avg_time": 1.896959, "std_time": 0.003120 , "avg_memory_kb": 782.375000, "std_memory_kb": 0}
            },
            "reversed": {
                100: {"avg_time": 0.000140, "std_time": 0.000001, "avg_memory_kb": 0.859375 , "std_memory_kb": 0},
                1000: {"avg_time": 0.010890, "std_time": 0.000246, "avg_memory_kb": 8.687500 , "std_memory_kb": 0},
                10000: {"avg_time": 0.158395  , "std_time": 0.003626, "avg_memory_kb": 79.250000, "std_memory_kb": 0},
                100000: {"avg_time": 1.926926, "std_time": 0.012671 , "avg_memory_kb": 782.671875, "std_memory_kb": 0}
            }
        },
        "HeapSort": {
            "random": {
                100: {"avg_time": 0.000145,"std_time": 0.000002,"avg_memory_kb": 0.859375,"std_memory_kb": 0.0},
                1000: {"avg_time": 0.008012,"std_time": 0.000262,"avg_memory_kb": 8.121094,"std_memory_kb": 0.0},
                10000: {"avg_time": 0.155017,"std_time": 0.001521,"avg_memory_kb": 78.683594,"std_memory_kb": 0.0},
                100000: {"avg_time": 2.496411,"std_time": 0.035682,"avg_memory_kb": 781.996094,"std_memory_kb": 0.0}
            },
            "sorted": {
                100: {"avg_time": 0.000162,"std_time": 0.000001,"avg_memory_kb": 0.859375,"std_memory_kb": 0.0},
                1000: {"avg_time": 0.009225,"std_time": 0.000218,"avg_memory_kb": 8.121094,"std_memory_kb": 0.0},
                10000: {"avg_time": 0.173144,"std_time": 0.001246,"avg_memory_kb": 78.683594,"std_memory_kb": 0.0},
                100000: {"avg_time": 2.599946,"std_time": 0.025884,"avg_memory_kb": 781.996094,"std_memory_kb": 0.0}
            },
            "reversed": {
                100: {"avg_time": 0.000153,"std_time": 0.000022,"avg_memory_kb": 0.859375,"std_memory_kb": 0.0},
                1000: {"avg_time": 0.006719,"std_time": 0.000268,"avg_memory_kb": 8.121094,"std_memory_kb": 0.0},
                10000: {"avg_time": 0.144183,"std_time": 0.000820,"avg_memory_kb": 78.683594,"std_memory_kb": 0.0},
                100000: {"avg_time": 2.264706,"std_time": 0.018742,"avg_memory_kb": 781.996094,"std_memory_kb": 0.0}
            }
        },
        "TimSort": {
            "random": {
                100: {"avg_time": 0.000103,"std_time": 0.000002,"avg_memory_kb": 1.593750,"std_memory_kb": 0.0},
                1000: {"avg_time": 0.013615,"std_time": 0.000316,"avg_memory_kb": 15.996094,"std_memory_kb": 0.0},
                10000: {"avg_time": 0.230496,"std_time": 0.007972,"avg_memory_kb": 156.621094,"std_memory_kb": 0.0},
                100000: {"avg_time": 2.811472,"std_time": 0.086046,"avg_memory_kb": 1562.871094,"std_memory_kb": 0.0}
            },
            "sorted": {
                100: {"avg_time": 0.000062,"std_time": 0.000011,"avg_memory_kb": 1.593750,"std_memory_kb": 0.0},
                1000: {"avg_time": 0.006122,"std_time": 0.000249,"avg_memory_kb": 15.996094,"std_memory_kb": 0.0},
                10000: {"avg_time": 0.133620,"std_time": 0.000659,"avg_memory_kb": 156.621094,"std_memory_kb": 0.0},
                100000: {"avg_time": 1.890065,"std_time": 0.028225,"avg_memory_kb": 1562.871094,"std_memory_kb": 0.0}
            },
            "reversed": {
                100: {"avg_time": 0.000154,"std_time": 0.000001,"avg_memory_kb": 1.593750,"std_memory_kb": 0.0},
                1000: {"avg_time": 0.021831,"std_time": 0.000547,"avg_memory_kb": 15.996094,"std_memory_kb": 0.0},
                10000: {"avg_time": 0.326647,"std_time": 0.001399,"avg_memory_kb": 156.621094,"std_memory_kb": 0.0},
                100000: {"avg_time": 3.883152,"std_time": 0.052388,"avg_memory_kb": 1562.871094,"std_memory_kb": 0.0}
            }
        }     
    }


def plot_comparison_by_size_and_type(results):
    # Configuración general de los gráficos
    plt.style.use('seaborn-v0_8')
    plt.rcParams['figure.figsize'] = (14, 10)
    plt.rcParams['font.size'] = 12
    
    # Tipos de listas, tamaños y algoritmos
    list_types = ['random', 'sorted', 'reversed']
    sizes = [100, 1000, 10000, 100000]
    algorithms = ["BubbleSort", "InsertionSort", "MergeSort", 
                  "QuickSort", "HeapSort", "TimSort"]
    
    # Verificar qué algoritmos están realmente en los resultados
    available_algorithms = [algo for algo in algorithms if algo in results]
    
    # Colores para cada algoritmo
    colors = plt.cm.tab10(np.linspace(0, 1, len(available_algorithms)))
    
    # =====================================================================
    # Gráficos por tipo de lista
    # =====================================================================
    for list_type in list_types:
        # Crear figura con subgráficos para tiempo y memoria
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        fig.suptitle(f'Comparación de Algoritmos - Listas {list_type.capitalize()}', fontsize=16)
        
        # Gráfico de tiempo
        ax1.set_title('Tiempo de Ejecución')
        ax1.set_xlabel('Tamaño de la lista (elementos)')
        ax1.set_ylabel('Tiempo promedio (s)')
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.grid(True, which="both", ls="--")
        
        # Configurar eje X para comenzar desde 10^2
        ax1.set_xlim(10**1.8, 10**5.2)  # Límites de 100 a 100,000
        ax1.grid(True, which="both", ls="--")
        
        # Gráfico de memoria
        ax2.set_title('Memoria Utilizada')
        ax2.set_xlabel('Tamaño de la lista (elementos)')
        ax2.set_ylabel('Memoria promedio (KB)')
        ax2.set_xscale('log')
        ax2.grid(True, which="both", ls="--")
        
        # Configurar eje X para comenzar desde 10^2
        ax2.set_xlim(10**1.8, 10**5.2)
        ax2.grid(True, which="both", ls="--")
        
        # Para cada algoritmo, trazar sus datos
        for algo, color in zip(available_algorithms, colors):
            if list_type in results[algo]:
                # Preparar datos para este algoritmo
                x = []
                y_time = []
                y_err_time = []
                y_memory = []
                y_err_memory = []
                
                for size in sizes:
                    if size in results[algo][list_type]:
                        x.append(size)
                        y_time.append(results[algo][list_type][size]['avg_time'])
                        y_err_time.append(results[algo][list_type][size]['std_time'])
                        y_memory.append(results[algo][list_type][size]['avg_memory_kb'])
                        y_err_memory.append(results[algo][list_type][size]['std_memory_kb'])
                
                if x:  # Solo si hay datos para este tipo de lista
                    # Gráfico de tiempo
                    ax1.errorbar(x, y_time, yerr=y_err_time, label=algo, color=color, 
                                marker='o', linestyle='-', linewidth=2, markersize=8, capsize=5)
                    
                    # Gráfico de memoria
                    ax2.errorbar(x, y_memory, yerr=y_err_memory, label=algo, color=color, 
                                marker='s', linestyle='--', linewidth=2, markersize=8, capsize=5)
        
        # Añadir leyenda solo una vez
        ax1.legend()
        ax2.legend()
        
        plt.tight_layout()
        plt.show()
    
    # =====================================================================
    # Gráficos por tamaño de lista
    # =====================================================================
    for size in sizes:
        # Verificar si al menos un algoritmo tiene datos para este tamaño
        has_data = any(size in results[algo].get(list_type, {}) 
            for algo in available_algorithms 
            for list_type in list_types
        )
        
        if not has_data:
            continue  # Saltar tamaños sin datos
        
        # Crear figura con subgráficos para tiempo y memoria
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        fig.suptitle(f'Comparación de Algoritmos - Tamaño {size} elementos', fontsize=16)
        
        # Gráfico de tiempo
        ax1.set_title('Tiempo de Ejecución')
        ax1.set_xlabel('Tipo de lista')
        ax1.set_ylabel('Tiempo promedio (s)')
        ax1.grid(True, which="both", ls="--")
        
        # Gráfico de memoria
        ax2.set_title('Memoria Utilizada')
        ax2.set_xlabel('Tipo de lista')
        ax2.set_ylabel('Memoria promedio (KB)')
        ax2.grid(True, which="both", ls="--")
        
        # Para cada tipo de lista, trazar datos de todos los algoritmos
        for i, list_type in enumerate(list_types):
            # Preparar posiciones en el eje X para este tipo de lista
            x_pos = i * (len(available_algorithms) + 1) + np.arange(len(available_algorithms))
            
            # Para cada algoritmo
            for j, algo in enumerate(available_algorithms):
                if list_type in results[algo] and size in results[algo][list_type]:
                    data = results[algo][list_type][size]
                    
                    # Gráfico de tiempo
                    ax1.bar(x_pos[j], data['avg_time'], color=colors[j], 
                            yerr=data['std_time'], capsize=5, label=algo if i == 0 else "")
                    
                    # Gráfico de memoria
                    ax2.bar(x_pos[j], data['avg_memory_kb'], color=colors[j], 
                            yerr=data['std_memory_kb'], capsize=5, label=algo if i == 0 else "")
        
        # Configurar ejes X
        ax1.set_xticks((np.arange(len(list_types)) * (len(available_algorithms) + 1)) + 
                      (len(available_algorithms) - 1) / 2)
        ax1.set_xticklabels([t.capitalize() for t in list_types])
        
        ax2.set_xticks((np.arange(len(list_types)) * (len(available_algorithms) + 1)) + 
                      (len(available_algorithms) - 1) / 2)
        ax2.set_xticklabels([t.capitalize() for t in list_types])
        
        # Añadir leyenda solo una vez
        ax1.legend()
        ax2.legend()
        
        plt.tight_layout()
        plt.show()


    
# Generar los gráficos
plot_comparison_by_size_and_type(benchmark_results)
    
# Generar los gráficos
plot_benchmark_results(benchmark_results)
plot_algorithms_by_size(benchmark_results, [100, 1000, 10000, 100000], ['random', 'sorted', 'reversed'])