import time
import random
from bst import Node, insert, search, preorder, inorder, postorder, delete, height
from avl import avl_insert, avl_inorder, get_height, get_balance
from range_queries import range_sum_naive, build_prefix, range_sum_prefix, FenwickTree, SegmentTree


def main():
    print("--- Задание 1: Создание бинарного дерева ---")
    root = Node(8)
    root.left = Node(4)
    root.right = Node(12)
    root.left.left = Node(2)
    root.left.right = Node(6)
    root.right.left = Node(10)
    root.right.right = Node(14)

    print(f"Корень: {root.key}")
    print(f"Левый потомок: {root.left.key}, Правый потомок: {root.right.key}")
    print(f"Лист: {root.left.left.key}")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 2: Вставка в BST ---")
    bst_root = None
    for val in [8, 4, 12, 2, 6, 10, 14]:
        bst_root = insert(bst_root, val)
    print(f"Inorder: {inorder(bst_root)}")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 3: Поиск элемента ---")
    for key in [8, 14, 99]:
        node, visited = search(bst_root, key)
        found = node is not None
        print(f"Ключ {key}: найден={found}, посещено узлов={visited}")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 4: Обходы дерева ---")
    print(f"Preorder:  {preorder(bst_root)}")
    print(f"Inorder:   {inorder(bst_root)}")
    print(f"Postorder: {postorder(bst_root)}")
    print("Inorder даёт отсортированную последовательность, т.к. сначала обходится левое поддерево (меньшие), потом корень, потом правое (большие).")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 5: Удаление из BST ---")
    bst_root = delete(bst_root, 2)
    print(f"Удалён лист 2, inorder: {inorder(bst_root)}")

    bst_root = delete(bst_root, 4)
    print(f"Удалён узел с одним потомком 4, inorder: {inorder(bst_root)}")

    bst_root = delete(bst_root, 12)
    print(f"Удалён узел с двумя потомками 12, inorder: {inorder(bst_root)}")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 6: Влияние порядка вставки на высоту ---")
    tree1 = None
    for val in [8, 4, 12, 2, 6, 10, 14]:
        tree1 = insert(tree1, val)

    tree2 = None
    for val in [2, 4, 6, 8, 10, 12, 14]:
        tree2 = insert(tree2, val)

    print(f"Дерево 1 (сбалансированное): высота = {height(tree1)}")
    print(f"Дерево 2 (вырожденное):      высота = {height(tree2)}")

    _, v1 = search(tree1, 14)
    _, v2 = search(tree2, 14)
    print(f"Поиск 14 в дереве 1: {v1} узлов, в дереве 2: {v2} узлов")
    print("Отсортированная вставка приводит к вырождению дерева в цепочку, поиск становится O(n).")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 7: Повороты AVL-дерева ---")

    # LL
    avl = None
    for val in [30, 20, 10]:
        avl = avl_insert(avl, val)
    print(f"LL (30,20,10): inorder={avl_inorder(avl)}, корень={avl.key}")

    # RR
    avl = None
    for val in [10, 20, 30]:
        avl = avl_insert(avl, val)
    print(f"RR (10,20,30): inorder={avl_inorder(avl)}, корень={avl.key}")

    # LR
    avl = None
    for val in [30, 10, 20]:
        avl = avl_insert(avl, val)
    print(f"LR (30,10,20): inorder={avl_inorder(avl)}, корень={avl.key}")

    # RL
    avl = None
    for val in [10, 30, 20]:
        avl = avl_insert(avl, val)
    print(f"RL (10,30,20): inorder={avl_inorder(avl)}, корень={avl.key}")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 8: Наивный запрос суммы диапазона ---")
    data = [random.randint(1, 1000) for _ in range(100000)]

    ranges = []
    for _ in range(1000):
        a = random.randint(0, len(data) - 1)
        b = random.randint(0, len(data) - 1)
        if a > b:
            a, b = b, a
        ranges.append((a, b))

    start = time.perf_counter()
    for l, r in ranges:
        range_sum_naive(data, l, r)
    naive_time = time.perf_counter() - start
    print(f"Наивный подход (1000 запросов): {naive_time:.5f} сек")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 9: Префиксные суммы ---")
    start = time.perf_counter()
    prefix = build_prefix(data)
    build_time = time.perf_counter() - start

    start = time.perf_counter()
    for l, r in ranges:
        range_sum_prefix(prefix, l, r)
    prefix_time = time.perf_counter() - start

    print(f"Построение prefix: {build_time:.5f} сек")
    print(f"Префиксные суммы (1000 запросов): {prefix_time:.5f} сек")
    print(f"Ускорение: наивный {naive_time:.5f} сек vs prefix {prefix_time:.5f} сек")
    print("При изменении одного элемента нужно пересчитать все последующие prefix — это O(n).")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 10: Дерево Фенвика ---")
    ft = FenwickTree(len(data))
    ft.build(data)

    for l, r in ranges[:5]:
        fenwick_res = ft.range_sum(l + 1, r + 1)
        real_res = sum(data[l:r + 1])
        print(f"[{l}, {r}] Фенвик: {fenwick_res}, sum(): {real_res}, совпадает: {fenwick_res == real_res}")

    print("Обновление элемента:")
    old_val = data[50]
    new_val = 999
    ft.update(51, new_val - old_val)
    data[50] = new_val
    fenwick_res = ft.range_sum(50, 52)
    real_res = sum(data[49:52])
    print(f"После обновления data[50]={new_val}: Фенвик={fenwick_res}, sum()={real_res}")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 11: Дерево отрезков для суммы ---")
    test_data = data[:1000]
    st = SegmentTree(test_data)

    test_ranges = [(0, 9), (10, 99), (100, 499), (0, 999), (500, 700)]
    for l, r in test_ranges:
        s, mn, mx = st.query(l, r)
        real_s = sum(test_data[l:r + 1])
        print(f"[{l},{r}] ST сумма: {s}, sum(): {real_s}, совпадает: {s == real_s}")

    print("Обновление data[5] = 12345:")
    st.update(5, 12345)
    test_data[5] = 12345
    s, mn, mx = st.query(0, 9)
    real_s = sum(test_data[0:10])
    print(f"[0,9] после обновления: ST={s}, sum()={real_s}, совпадает: {s == real_s}")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 12: Сумма, минимум и максимум ---")
    st2 = SegmentTree(test_data)
    for l, r in [(0, 9), (100, 200), (0, 999)]:
        s, mn, mx = st2.query(l, r)
        real_s = sum(test_data[l:r + 1])
        real_mn = min(test_data[l:r + 1])
        real_mx = max(test_data[l:r + 1])
        print(f"[{l},{r}] сумма: {s}=={real_s}, мин: {mn}=={real_mn}, макс: {mx}=={real_mx}")

    # один элемент
    s, mn, mx = st2.query(42, 42)
    print(f"[42,42] сумма={s}, мин={mn}, макс={mx}, значение={test_data[42]}")

    print("Фенвик удобен для суммы (компактный), а дерево отрезков легко расширяется для мин/макс.")

# ---------------------------------------------------------------------------------------------------

    print("\n--- Задание 13: Самостоятельная работа (Анализ датчиков) ---")

    class SensorSystem:
        def __init__(self):
            self.sensor_tree = None
            self.measurements = {}
            self.fenwick_trees = {}
            self.segment_trees = {}

        def add_sensor(self, sensor_id, measurements):
            self.sensor_tree = insert(self.sensor_tree, sensor_id)
            self.measurements[sensor_id] = list(measurements)

            ft = FenwickTree(len(measurements))
            ft.build(measurements)
            self.fenwick_trees[sensor_id] = ft

            st = SegmentTree(measurements)
            self.segment_trees[sensor_id] = st
            print(f"Датчик {sensor_id} добавлен. Использована структура: BST (дерево) + dict (хранение)")

        def find_sensor(self, sensor_id):
            node, visited = search(self.sensor_tree, sensor_id)
            print(f"Поиск датчика {sensor_id}: найден={node is not None}, посещено={visited} узлов. Структура: BST")
            return node

        def sorted_ids(self):
            ids = inorder(self.sensor_tree)
            print(f"Датчики в отсортированном порядке: {ids}. Структура: BST inorder-обход")
            return ids

        def range_sum_fenwick(self, sensor_id, left, right):
            result = self.fenwick_trees[sensor_id].range_sum(left + 1, right + 1)
            print(f"Сумма [{left},{right}] (Фенвик): {result}")
            return result

        def range_query_segment(self, sensor_id, left, right):
            s, mn, mx = self.segment_trees[sensor_id].query(left, right)
            print(f"[{left},{right}] (Дерево отрезков): сумма={s}, мин={mn}, макс={mx}")
            return s, mn, mx

        def update_measurement(self, sensor_id, index, new_value):
            old = self.measurements[sensor_id][index]
            self.measurements[sensor_id][index] = new_value
            self.fenwick_trees[sensor_id].update(index + 1, new_value - old)
            self.segment_trees[sensor_id].update(index, new_value)
            print(f"Обновлено измерение [{index}]: {old} -> {new_value}")

    system = SensorSystem()

    random.seed(42)
    for sid in [5, 3, 8, 1, 7]:
        m = [random.randint(10, 500) for _ in range(1000)]
        system.add_sensor(sid, m)

    system.find_sensor(7)
    system.find_sensor(99)
    system.sorted_ids()

    print("\nЗапросы к датчику 5:")
    system.range_sum_fenwick(5, 0, 99)
    system.range_query_segment(5, 0, 99)

    print("\nДо обновления:")
    system.range_query_segment(5, 0, 9)

    system.update_measurement(5, 5, 9999)

    print("После обновления:")
    system.range_query_segment(5, 0, 9)
    system.range_sum_fenwick(5, 0, 9)

    print("\n--- Обоснование выбора структур данных ---")
    print("BST — для поиска датчика по id и вывода в отсортированном порядке (inorder).")
    print("Дерево Фенвика — для быстрого вычисления суммы на диапазоне с поддержкой обновлений, O(log n).")
    print("Дерево отрезков — для одновременного вычисления суммы, минимума и максимума на диапазоне.")


if __name__ == "__main__":
    main()
