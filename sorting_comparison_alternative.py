"""
sorting_comparison.py - Порівняння алгоритмів сортування БЕЗ matplotlib

Цей файл створено для систем, де matplotlib не можна встановити 
або виникають проблеми з встановленням (наприклад, macOS з externally-managed-environment).

Функціональність:
- Повне порівняння алгоритмів сортування
- Детальний текстовий аналіз та таблиці
- Збереження результатів у CSV
- Незалежність від зовнішніх графічних бібліотек

Для графічної візуалізації використовуйте sorting_comparison_with_plots.py
"""

import timeit
import random
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
    # Створюємо копію вхідного списку, щоб не змінювати оригінал
    arr = arr.copy()
    
    # Проходимо по всіх елементах, починаючи з другого
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Поки не дійшли до початку списку і поточний елемент більший за ключ
        while j >= 0 and arr[j] > key:
            # Зсуваємо елементи вправо
            arr[j + 1] = arr[j]
            j -= 1
        # Вставляємо ключ у відповідну позицію
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
    # Створюємо копію вхідного списку, щоб не змінювати оригінал
    arr = arr.copy()
    
    # Базовий випадок: якщо список має 1 або 0 елементів, він вже відсортований
    if len(arr) <= 1:
        return arr
    
    # Знаходимо середину списку
    mid = len(arr) // 2
    
    # Рекурсивно сортуємо ліву та праву частини
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Об'єднуємо ліву та праву частини
    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    """
    Допоміжна функція для злиття двох відсортованих списків.
    
    Args:
        left: Перший відсортований список
        right: Другий відсортований список
        
    Returns:
        Об'єднаний відсортований список
    """
    result = []
    i = j = 0
    
    # Порівнюємо елементи з обох списків і додаємо менший до результату
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Додаємо елементи, що залишилися (якщо є)
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def timsort(arr: List[int]) -> List[int]:
    """
    Вбудований алгоритм сортування Python (Timsort).
    
    Args:
        arr: Список цілих чисел для сортування
        
    Returns:
        Відсортований список
    """
    # Створюємо копію вхідного списку, щоб не змінювати оригінал
    arr = arr.copy()
    
    # Використовуємо вбудований метод sorted()
    return sorted(arr)

def generate_data(size: int, data_type: str = "random") -> List[int]:
    """
    Генерує тестові дані різних типів.
    
    Args:
        size: Розмір списку
        data_type: Тип даних ("random", "sorted", "reversed", "partially_sorted")
        
    Returns:
        Список цілих чисел
    """
    if data_type == "random":
        # Генеруємо випадковий список чисел
        return [random.randint(0, 1000000) for _ in range(size)]
    elif data_type == "sorted":
        # Генеруємо відсортований список чисел
        return list(range(size))
    elif data_type == "reversed":
        # Генеруємо список чисел у зворотному порядку
        return list(range(size, 0, -1))
    elif data_type == "partially_sorted":
        # Генеруємо частково відсортований список
        arr = list(range(size))
        # Перемішуємо ~25% елементів
        for _ in range(size // 4):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    else:
        raise ValueError(f"Невідомий тип даних: {data_type}")

def measure_time(func, data, runs=3):
    """
    Вимірює час виконання функції.
    
    Args:
        func: Функція для вимірювання
        data: Вхідні дані
        runs: Кількість запусків для усереднення
        
    Returns:
        Середній час виконання (в секундах)
    """
    # Використовуємо timeit для точного вимірювання часу
    total_time = timeit.timeit(lambda: func(data), number=runs)
    return total_time / runs

def compare_sorting_algorithms(sizes, data_types):
    """
    Порівнює алгоритми сортування за часом на різних типах даних.
    
    Args:
        sizes: Список розмірів вхідних даних
        data_types: Список типів даних
        
    Returns:
        Словник з результатами
    """
    results = {data_type: {"insertion": [], "merge": [], "timsort": []} for data_type in data_types}
    
    print("🔄 Початок порівняння алгоритмів сортування...")
    print("=" * 60)
    
    for size in sizes:
        print(f"\n📊 Тестування для розміру {size:,} елементів:")
        print("-" * 45)
        
        for data_type in data_types:
            data = generate_data(size, data_type)
            
            print(f"  📈 Тип даних: {data_type}")
            
            # Пропускаємо сортування вставками для великих масивів (надто повільно)
            if size <= 10000:
                print("    ⏱️  Вимірюємо insertion sort...", end=" ")
                insertion_time = measure_time(insertion_sort, data)
                results[data_type]["insertion"].append(insertion_time)
                print(f"{insertion_time:.6f}s")
            else:
                results[data_type]["insertion"].append(None)
                print("    ⏱️  Insertion sort пропущено (занадто великий розмір)")
            
            print("    ⏱️  Вимірюємо merge sort...", end=" ")
            merge_time = measure_time(merge_sort, data)
            results[data_type]["merge"].append(merge_time)
            print(f"{merge_time:.6f}s")
            
            print("    ⏱️  Вимірюємо timsort...", end=" ")
            timsort_time = measure_time(timsort, data)
            results[data_type]["timsort"].append(timsort_time)
            print(f"{timsort_time:.6f}s")
    
    return results, sizes

def print_results_table(results, sizes, data_types):
    """
    Виводить результати у вигляді таблиці.
    
    Args:
        results: Словник з результатами
        sizes: Список розмірів
        data_types: Список типів даних
    """
    print("\n" + "="*80)
    print("📋 РЕЗУЛЬТАТИ ПОРІВНЯННЯ АЛГОРИТМІВ СОРТУВАННЯ")
    print("="*80)
    
    for data_type in data_types:
        print(f"\n🔸 {data_type.upper()} ДАНІ:")
        print("-" * 70)
        print(f"{'Розмір':<10} {'Insertion':<12} {'Merge':<12} {'Timsort':<12} {'Найкращий':<15}")
        print("-" * 70)
        
        for i, size in enumerate(sizes):
            insertion_time = results[data_type]["insertion"][i]
            merge_time = results[data_type]["merge"][i]
            timsort_time = results[data_type]["timsort"][i]
            
            # Визначаємо найкращий алгоритм
            times = []
            if insertion_time is not None:
                times.append(("Insertion", insertion_time))
            times.append(("Merge", merge_time))
            times.append(("Timsort", timsort_time))
            
            best_algo, best_time = min(times, key=lambda x: x[1])
            
            # Форматуємо результати
            insertion_str = f"{insertion_time:.6f}s" if insertion_time else "N/A"
            merge_str = f"{merge_time:.6f}s"
            timsort_str = f"{timsort_time:.6f}s"
            
            print(f"{size:<10,} {insertion_str:<12} {merge_str:<12} {timsort_str:<12} {best_algo:<15}")

def analyze_performance(results, sizes, data_types):
    """
    Аналізує продуктивність алгоритмів.
    
    Args:
        results: Словник з результатами
        sizes: Список розмірів
        data_types: Список типів даних
    """
    print(f"\n" + "="*80)
    print("🔬 АНАЛІЗ ПРОДУКТИВНОСТІ")
    print("="*80)
    
    for data_type in data_types:
        print(f"\n📊 Аналіз для {data_type} даних:")
        print("-" * 50)
        
        # Аналізуємо співвідношення швидкості
        merge_times = results[data_type]["merge"]
        timsort_times = results[data_type]["timsort"]
        
        print("🚀 Швидкість Timsort vs Merge Sort:")
        for i, size in enumerate(sizes):
            if i < len(merge_times) and i < len(timsort_times):
                speedup = merge_times[i] / timsort_times[i]
                print(f"   Розмір {size:,}: Timsort швидший у {speedup:.2f} разів")
        
        # Аналіз для insertion sort (тільки для малих розмірів)
        insertion_times = [t for t in results[data_type]["insertion"] if t is not None]
        if insertion_times:
            print("\n⚡ Insertion Sort (малі розміри):")
            valid_sizes = sizes[:len(insertion_times)]
            for i, (size, time) in enumerate(zip(valid_sizes, insertion_times)):
                timsort_time = timsort_times[i]
                if data_type == "sorted":
                    comparison = "швидший" if time < timsort_time else "повільніший"
                    ratio = max(time, timsort_time) / min(time, timsort_time)
                    print(f"   Розмір {size:,}: Insertion Sort {comparison} у {ratio:.2f} разів")

def save_results_to_csv(results, sizes, data_types, filename="sorting_results.csv"):
    """
    Зберігає результати у CSV файл.
    
    Args:
        results: Словник з результатами
        sizes: Список розмірів
        data_types: Список типів даних
        filename: Ім'я файлу для збереження
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
    print("🔬" + "="*58 + "🔬")
    print("🔬  ПОРІВНЯННЯ АЛГОРИТМІВ СОРТУВАННЯ (БЕЗ MATPLOTLIB)  🔬")
    print("🔬" + "="*58 + "🔬")
    print("📋 Порівняння: Insertion Sort, Merge Sort, Timsort")
    print("📊 Тестування на різних типах та розмірах даних")
    print("⏱️  Вимірювання часу за допомогою модуля timeit")
    print("="*62)
    
    # Розміри списків для тестування
    sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
    
    # Типи даних для тестування
    data_types = ["random", "sorted", "reversed", "partially_sorted"]
    
    print(f"📋 Розміри для тестування: {', '.join(map(str, sizes))}")
    print(f"📊 Типи даних: {', '.join(data_types)}")
    
    # Порівнюємо алгоритми
    results, sizes = compare_sorting_algorithms(sizes, data_types)
    
    # Виводимо результати у вигляді таблиці
    print_results_table(results, sizes, data_types)
    
    # Аналізуємо продуктивність
    analyze_performance(results, sizes, data_types)
    
    # Зберігаємо результати у CSV
    save_results_to_csv(results, sizes, data_types)
    
    # Виводимо висновки
    print(f"\n" + "="*80)
    print("📝 ГОЛОВНІ ВИСНОВКИ")
    print("="*80)
    print("""
🎯 1. TIMSORT ПЕРЕВАЖАЄ ВСІ ІНШІ АЛГОРИТМИ:
   • Показує найкращу продуктивність на всіх типах даних
   • Особливо ефективний для відсортованих та частково відсортованих даних
   • Адаптується до структури даних, використовуючи вже відсортовані ділянки

⚡ 2. INSERTION SORT - ДОБРИЙ ДЛЯ МАЛИХ ДАНИХ:
   • Ефективний для списків до 1000 елементів
   • Має лінійну складність O(n) для відсортованих даних
   • Стає неефективним для великих списків (квадратична складність)

🔄 3. MERGE SORT - СТАБІЛЬНИЙ ТА ПЕРЕДБАЧУВАНИЙ:
   • Завжди O(n log n), незалежно від типу даних
   • Програє Timsort у продуктивності
   • Хороший вибір, коли потрібна гарантована складність

🏆 4. ЧОМУ TIMSORT ТАК ЕФЕКТИВНИЙ:
   • Гібридний підхід: поєднує insertion sort + merge sort
   • Використовує insertion sort для малих ділянок
   • Виявляє та використовує природні послідовності у даних
   • Оптимізований для реальних даних, які часто частково відсортовані

💡 5. ПРАКТИЧНІ РЕКОМЕНДАЦІЇ:
   • Завжди використовуйте sorted() або .sort() у Python
   • Не реалізовуйте власні алгоритми сортування без необхідності
   • Timsort оптимізований роками розробки та тестування
   • Вбудовані алгоритми Python - найкращий вибір для більшості задач
    """)
    
    print("✅ Аналіз завершено! Детальні дані збережено у sorting_results.csv")

if __name__ == "__main__":
    main()
