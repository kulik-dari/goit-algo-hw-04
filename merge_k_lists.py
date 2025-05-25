from typing import List

def merge_two_lists(list1: List[int], list2: List[int]) -> List[int]:
    """
    Злиття двох відсортованих списків у один відсортований список.
    
    Args:
        list1: Перший відсортований список
        list2: Другий відсортований список
        
    Returns:
        Об'єднаний відсортований список
    """
    result = []
    i = j = 0
    
    # Порівнюємо елементи з обох списків і додаємо менший до результату
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    
    # Додаємо елементи, що залишилися (якщо є)
    result.extend(list1[i:])
    result.extend(list2[j:])
    
    return result

def merge_k_lists(lists: List[List[int]]) -> List[int]:
    """
    Злиття k відсортованих списків у один відсортований список.
    
    Args:
        lists: Список відсортованих списків
        
    Returns:
        Об'єднаний відсортований список
    """
    # Базовий випадок: якщо немає списків, повертаємо порожній список
    if not lists:
        return []
    
    # Базовий випадок: якщо є лише один список, повертаємо його
    if len(lists) == 1:
        return lists[0]
    
    # Рекурсивно об'єднуємо списки, розділяючи їх на пари
    mid = len(lists) // 2
    left = merge_k_lists(lists[:mid])
    right = merge_k_lists(lists[mid:])
    
    # Об'єднуємо дві половини
    return merge_two_lists(left, right)

def main():
    """
    Тестування функції merge_k_lists.
    """
    # Тестовий випадок з прикладу
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    merged_list = merge_k_lists(lists)
    print("Відсортований список:", merged_list)
    
    # Додаткові тестові випадки
    test_cases = [
        # Порожній список списків
        [],
        # Список з одним порожнім списком
        [[]],
        # Список з одним списком
        [[1, 2, 3]],
        # Список з кількома списками, включаючи порожні
        [[1, 3, 5], [], [2, 4, 6]],
        # Список з дублікатами
        [[1, 1, 3], [1, 2, 2], [2, 3, 3]]
    ]
    
    for i, test_case in enumerate(test_cases):
        result = merge_k_lists(test_case)
        print(f"Тест {i+1}: {test_case} -> {result}")

if __name__ == "__main__":
    main()
