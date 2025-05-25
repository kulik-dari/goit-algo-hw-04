"""
sorting_comparison_with_plots.py - Порівняння алгоритмів сортування З matplotlib

Цей файл містить повну реалізацію з графічною візуалізацією.
Використовуйте цей файл, якщо у вас встановлено matplotlib.

Встановлення matplotlib:
pip3 install matplotlib
або
python3 -m venv venv && source venv/bin/activate && pip install matplotlib
"""

import timeit
import random
import matplotlib.pyplot as plt
import numpy as np
from typing import List
import csv

def insertion_sort(arr: List[int]) -> List[int]:
    """
    Алгоритм сортування вставками.
    
    Args:
        arr: Список цілих чисел для сортування
        
    Returns:
        Відсортований список
    """
    arr = arr.copy()
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        
    return arr

def merge_sort(arr: List[int]) -> List[int]:
    """
    Алгоритм сортування злиттям.
    
    Args:
        arr: Список цілих чисел для сортування
        
    Returns:
        Відсортований список
    """
    arr = arr.copy()
    
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    """
    Допоміжна функція для злиття двох відсортованих списків.
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def timsort(arr: List[int]) -> List[int]:
    """
    Вбудований алгоритм сортування Python (Timsort).
    """
    return sorted(arr.copy())

def generate_data(size: int, data_type: str = "random") -> List[int]:
    """
    Генерує тестові дані різних типів.
    """
    if data_type == "random":
        return [random.randint(0, 1000000) for _ in range(size)]
    elif data_type == "sorted":
        return list(range(size))
    elif data_type == "reversed":
        return list(range(size, 0, -1))
    elif data_type == "partially_sorted":
        arr = list(range(size))
        for _ in range(size // 4):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    else:
        raise ValueError(f"Невідомий тип даних: {data_type}")

def measure_time(func, data, runs=3):
    """
    Вимірює час виконання функції.
    """
    total_time = timeit.timeit(lambda: func(data), number=runs)
    return total_time / runs

def compare_sorting_algorithms(sizes, data_types):
    """
    Порівнює алгоритми сортування за часом на різних типах даних.
    """
    results = {data_type: {"insertion": [], "merge": [], "timsort": []} for data_type in data_types}
    
    print("🔄 Початок порівняння алгоритмів сортування...")
    print("=" * 60)
    
    for size in sizes:
        print(f"\n📊 Тестування для розміру {size:,} елементів:")
        
        for data_type in data_types:
            data = generate_data(size, data_type)
            
            # Пропускаємо сортування вставками для великих масивів
            if size <= 10000:
                insertion_time = measure_time(insertion_sort, data)
                results[data_type]["insertion"].append(insertion_time)
            else:
                results[data_type]["insertion"].append(None)
            
            merge_time = measure_time(merge_sort, data)
            results[data_type]["merge"].append(merge_time)
            
            timsort_time = measure_time(timsort, data)
            results[data_type]["timsort"].append(timsort_time)
            
            print(f"  {data_type}: merge={merge_time:.6f}s, timsort={timsort_time:.6f}s")
    
    return results, sizes

def plot_results(results, sizes, data_types):
    """
    Створює графічну візуалізацію результатів.
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.flatten()
    
    colors = {
        'insertion': '#FF6B6B',  # Червоний
        'merge': '#4ECDC4',      # Бірюзовий
        'timsort': '#45B7D1'     # Синій
    }
    
    for i, data_type in enumerate(data_types):
        ax = axes[i]
        
        # Фільтруємо None значення для сортування вставками
        valid_sizes_insertion = [s for j, s in enumerate(sizes) if results[data_type]["insertion"][j] is not None]
        valid_times_insertion = [t for t in results[data_type]["insertion"] if t is not None]
        
        # Малюємо графіки
        if valid_sizes_insertion:
            ax.plot(valid_sizes_insertion, valid_times_insertion, 'o-', 
                   label="Insertion Sort", color=colors['insertion'], linewidth=2, markersize=6)
        
        ax.plot(sizes, results[data_type]["merge"], 'o-', 
               label="Merge Sort", color=colors['merge'], linewidth=2, markersize=6)
        
        ax.plot(sizes, results[data_type]["timsort"], 'o-', 
               label="Timsort", color=colors['timsort'], linewidth=2, markersize=6)
        
        # Налаштування графіка
        ax.set_title(f'Час сортування для {data_type} даних', fontsize=14, fontweight='bold')
        ax.set_xlabel("Розмір списку", fontsize=12)
        ax.set_ylabel("Час виконання (секунди)", fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')  # Логарифмічна шкала для кращого відображення
        
        # Форматування осей
        ax.ticklabel_format(style='plain', axis='x')
        
        # Додаємо анотації для найкращих результатів
        timsort_times = results[data_type]["timsort"]
        min_time_idx = timsort_times.index(min(timsort_times))
        ax.annotate(f'Найкращий: {min(timsort_times):.6f}s', 
                   xy=(sizes[min_time_idx], min(timsort_times)),
                   xytext=(10, 10), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                   fontsize=8)
    
    plt.tight_layout(pad=3.0)
    plt.savefig("sorting_comparison_with_plots.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\n📊 Графіки збережено у файл: sorting_comparison_with_plots.png")

def create_comparison_chart(results, sizes, data_types):
    """
    Створює додатковий графік порівняння швидкості.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Обчислюємо середній speedup Timsort vs Merge Sort
    speedups = []
    labels = []
    
    for data_type in data_types:
        merge_times = results[data_type]["merge"]
        timsort_times = results[data_type]["timsort"]
        
        avg_speedup = np.mean([m/t for m, t in zip(merge_times, timsort_times)])
        speedups.append(avg_speedup)
        labels.append(data_type.replace('_', ' ').title())
    
    # Створюємо стовпчасту діаграму
    bars = ax.bar(labels, speedups, color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99'])
    
    # Додаємо значення на стовпчики
    for bar, speedup in zip(bars, speedups):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{speedup:.2f}x', ha='center', va='bottom', fontweight='bold')
    
    ax.set_title('Середнє прискорення Timsort порівняно з Merge Sort', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Коефіцієнт прискорення', fontsize=12)
    ax.set_xlabel('Тип даних', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Додаємо горизонтальну лінію на рівні 1.0
    ax.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Однакова швидкість')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig("timsort_speedup_comparison.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"📈 Графік прискорення збережено у файл: timsort_speedup_comparison.png")

def save_results_to_csv(results, sizes, data_types, filename="sorting_results.csv"):
    """
    Зберігає результати у CSV файл.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['data_type', 'size', 'insertion_sort', 'merge_sort', 'timsort']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data_type in data_types:
            for i, size in enumerate(sizes):
                writer.writerow({
                    'data_type': data_type,
                    'size': size,
                    'insertion_sort': results[data_type]["insertion"][i],
                    'merge_sort': results[data_type]["merge"][i],
                    'timsort': results[data_type]["timsort"][i]
                })
    
    print(f"\n💾 Результати збережено у файл: {filename}")

def main():
    """
    Головна функція програми.
    """
    print("📊" + "="*58 + "📊")
    print("📊  ПОРІВНЯННЯ АЛГОРИТМІВ СОРТУВАННЯ (З MATPLOTLIB)  📊")
    print("📊" + "="*58 + "📊")
    print("🎯 Повний аналіз з графічною візуалізацією")
    print("📈 Створення детальних графіків та діаграм")
    print("="*62)
    
    # Перевірка наявності matplotlib
    try:
        import matplotlib.pyplot as plt
        print("✅ Matplotlib доступний - використовуємо повну візуалізацію")
    except ImportError:
        print("❌ Помилка: matplotlib не встановлено!")
        print("Встановіть за допомогою: pip3 install matplotlib")
        return
    
    # Розміри та типи даних
    sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
    data_types = ["random", "sorted", "reversed", "partially_sorted"]
    
    print(f"📋 Розміри: {', '.join(map(str, sizes))}")
    print(f"📊 Типи даних: {', '.join(data_types)}")
    
    # Виконуємо порівняння
    results, sizes = compare_sorting_algorithms(sizes, data_types)
    
    # Створюємо візуалізації
    plot_results(results, sizes, data_types)
    create_comparison_chart(results, sizes, data_types)
    
    # Зберігаємо дані
    save_results_to_csv(results, sizes, data_types)
    
    # Висновки
    print(f"\n🎯 ПІДСУМКИ:")
    print("✅ Графіки створено та збережено")
    print("✅ Дані експортовано у CSV")
    print("✅ Аналіз завершено")
    
    print(f"\n📁 Створені файли:")
    print("  • sorting_comparison_with_plots.png - основні графіки")
    print("  • timsort_speedup_comparison.png - порівняння швидкості")
    print("  • sorting_results.csv - сирі дані")

if __name__ == "__main__":
    main()
