import time
import random
import heapq
from hash_table import HashTable
from binary_heap import MinHeap

def linear_search(numbers, target):
    for index, value in enumerate(numbers):
        if value == target:
            return index
    return -1

def bucket_index(key, table_size):
    return hash(key) % table_size

def top_k_heap(data, k):
    heap = []
    for value in data:
        if len(heap) < k:
            heapq.heappush(heap, value)
        elif value > heap[0]:
            heapq.heapreplace(heap, value)
    return heap

def main():
    print("--- Задание 2: Доступ по индексу и линейный поиск ---")
    numbers = list(range(100000))
    
    start = time.perf_counter()
    _ = numbers[99966]
    print(f"Доступ по индексу (конец): {time.perf_counter() - start:.8f} сек")
    
    start = time.perf_counter()
    _ = linear_search(numbers, 99966)
    print(f"Линейный поиск (конец): {time.perf_counter() - start:.8f} сек")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 3: Доступ по ключу ---")
    list_data = [(i, f"example_{i}") for i in range(10000)]
    dict_data = {i: f"example_{i}" for i in range(10000)}
    target = 9999
    
    start = time.perf_counter()
    for k, v in list_data:
        if k == target:
            break
    print(f"Поиск в списке: {time.perf_counter() - start:.8f} сек")
    
    start = time.perf_counter()
    _ = dict_data[target]
    print(f"Поиск в словаре: {time.perf_counter() - start:.8f} сек")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 4: Исследование функции hash() ---")
    for i in range(30):
        key = random.randint(1, 1000)
        idx = bucket_index(key, 10)
        print(f"Key: {key}, Hash: {hash(key)}, Index: {idx}")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 6: Коэффициент заполнения и коллизии ---")
    for size in [10, 100, 1000]:
        ht = HashTable(size)
        for _ in range(500):
            ht.set(random.randint(1, 10000), "data")
        print(f"Размер: {size}, Заполнение (alpha): {ht.load_factor}, Коллизии: {ht.collision_count()}")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 8 и 9: Проверка MinHeap ---")
    heap = MinHeap()
    for val in [10, 4, 7, 1, 9, 3]:
        heap.push(val)
        print(f"Вставка {val}, состояние кучи: {heap.data}")
    
    extracted = []
    while heap.data:
        extracted.append(heap.pop())
    print(f"Порядок извлечения: {extracted}")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 10: Приоритетная очередь ---")
    tasks = []
    count = 0
    heapq.heappush(tasks, (2, count:=count+1, "Сделать лабу"))
    heapq.heappush(tasks, (1, count:=count+1, "Покушать"))
    heapq.heappush(tasks, (4, count:=count+1, "Обновить драйвера"))
    heapq.heappush(tasks, (2, count:=count+1, "Погулять"))
    heapq.heappush(tasks, (2, count:=count+1, "Купить хлуб"))
    heapq.heappush(tasks, (1, count:=count+1, "Исправить ошибку"))
    heapq.heappush(tasks, (3, count:=count+1, "Посмотреть фильм"))
    heapq.heappush(tasks, (5, count:=count+1, "Ответить на вопросы"))
    
    while tasks:
        priority, _, task = heapq.heappop(tasks)
        print(f"Приоритет: {priority}, Задача: {task}")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 11 и 12: Top-K ---")
    data_large = [random.randint(1, 100000) for _ in range(100000)]
    for k in [10, 100, 1000]:
        start = time.perf_counter()
        _ = sorted(data_large, reverse=True)[:k]
        time_sort = time.perf_counter() - start
        
        start = time.perf_counter()
        _ = top_k_heap(data_large, k)
        time_heap = time.perf_counter() - start
        print(f"K={k} | Сортировка: {time_sort:.5f} сек | Куча: {time_heap:.5f} сек")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 13: Самостоятельная работа (Соревнование) ---")
    class Competition:
        def __init__(self):
            self.participants = {} # Поиск по ID - dict
            self.check_queue = [] # Очередь проверки - heapq
            self.counter = 0

        def add_participant(self, p_id, name, score):
            self.participants[p_id] = {"name": name, "score": score}
            print("Использована структура dict")

        def add_to_queue(self, priority, p_id):
            self.counter += 1
            heapq.heappush(self.check_queue, (priority, self.counter, p_id))
            print("Использована структура heapq (list)")

        def top_k(self, k):
            # Top-K без полной сортировки
            heap = []
            for p_id, info in self.participants.items():
                val = (info["score"], p_id, info["name"])
                if len(heap) < k:
                    heapq.heappush(heap, val)
                elif val[0] > heap[0][0]:
                    heapq.heapreplace(heap, val)
            print("Использована структура heapq (list) с размером K")
            sorted_top = sorted(heap, reverse=True) # сортируем только итоговые K элементов
            print(f"\n--- Топ-{k} участников ---")
            for score, p_id, name in sorted_top:
                print(f"ID: {p_id} | Имя: {name} | Результат: {score}")

    comp = Competition()
    comp.add_participant(1, "Максос", 150)
    comp.add_participant(2, "Денис", 200)
    comp.add_participant(3, "Дима", 100)
    comp.add_participant(4, "Влад", 120)
    comp.add_to_queue(1, 4)
    comp.add_to_queue(2, 2)
    comp.top_k(3)

if __name__ == "__main__":
    main()