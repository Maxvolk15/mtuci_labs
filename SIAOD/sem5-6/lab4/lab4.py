import sys
import math
import heapq
from collections import deque

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


# ---------------------------------------------------------------------
# Задание 1: DSU и минимальное остовное дерево (алгоритм Краскала)
# ---------------------------------------------------------------------

# Исходный граф для 1 задания
graph_edges = [
    (4, 'A', 'B'),
    (3, 'A', 'C'),
    (1, 'B', 'C'),
    (2, 'B', 'D'),
    (4, 'C', 'D'),
    (2, 'C', 'E'),
    (3, 'D', 'E'),
    (2, 'D', 'F'),
    (3, 'E', 'F'),
    (6, 'E', 'G'),
    (1, 'F', 'G'),
]

# Реализация DSU
class DSU:
    def __init__(self, elements):
        self.parent = {x: x for x in elements}
        self.rank = {x: 0 for x in elements}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False
        
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1
        return True

# Алгоритм Краскала
def kraskal(edges):
    vertices = set()
    for _, u, v in edges:
        vertices.add(u)
        vertices.add(v)
    
    dsu = DSU(vertices)
    mst = []
    total_weight = 0

    for weight, u, v in sorted(edges, key=lambda x: x[0]):
        if dsu.union(u, v):
            mst.append((u, v, weight))
            total_weight += weight
            if len(mst) == len(vertices) - 1:
                break

    return mst, total_weight


# ---------------------------------------------------------------------
# Данные для заданий 2–6 (Клеточное поле)
# ---------------------------------------------------------------------

GRID = [
    "S..#........",
    ".#.#.######.",
    ".#...#......",
    ".###.#.####.",
    ".....#....#.",
    ".#####.##.#.",
    ".......##...",
    ".#####....#.",
    ".#...####.#.",
    ".#.#......#.",
    "...#.####...",
    "####......G.",
]

ROWS = len(GRID)
COLS = len(GRID[0])
START = (0, 0)
GOAL = (11, 10)

# Порядок генерации соседей: вниз, вверх, вправо, влево
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# Проверка и получение проходимых соседей
def get_neighbors(r, c):
    neighbors = []
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and GRID[nr][nc] != '#':
            neighbors.append((nr, nc))
    return neighbors

# Функция отрисовки маршрута поверх копии поля
def render_grid_with_path(grid, path):
    rendered = [list(row) for row in grid]
    for r, c in path:
        if (r, c) != START and (r, c) != GOAL:
            rendered[r][c] = '*'
    return "\n".join("".join(row) for row in rendered)


# ---------------------------------------------------------------------
# Задание 2: Пространство состояний и базовый BFS
# ---------------------------------------------------------------------

def bfs(start, goal):
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    processed_count = 0

    while queue:
        curr = queue.popleft()
        processed_count += 1
        if curr == goal:
            break
        for nxt in get_neighbors(*curr):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = curr
                queue.append(nxt)

    # Восстановление маршрута
    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr)
    path.reverse()

    return path, processed_count


# ---------------------------------------------------------------------
# Задание 3: Эвристические функции
# ---------------------------------------------------------------------

def manhattan(a, b):
    # Расстояние городских кварталов (L1 норма)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    # Прямое геометрическое расстояние (L2 норма)
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


# ---------------------------------------------------------------------
# Задание 4: Greedy Best-First Search
# ---------------------------------------------------------------------

def greedy_bfs(start, goal, heuristic_func):
    open_heap = []
    insertion_order = 0
    # Приоритет в очереди - только значение эвристики h(n)
    heapq.heappush(open_heap, (heuristic_func(start, goal), insertion_order, start))
    parent = {start: None}
    closed = set()
    processed_count = 0

    while open_heap:
        h, _, curr = heapq.heappop(open_heap)
        if curr in closed:
            continue
        closed.add(curr)
        processed_count += 1

        if curr == goal:
            break

        for nxt in get_neighbors(*curr):
            if nxt not in closed:
                if nxt not in parent:
                    parent[nxt] = curr
                insertion_order += 1
                heapq.heappush(open_heap, (heuristic_func(nxt, goal), insertion_order, nxt))

    # Восстановление маршрута
    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr)
    path.reverse()

    return path, processed_count


# ---------------------------------------------------------------------
# Задание 5: Алгоритм A*
# ---------------------------------------------------------------------

def a_star(start, goal, heuristic_func, cost_matrix=None):
    open_heap = []
    insertion_order = 0
    # Приоритет f(n) = g(n) + h(n)
    h_start = heuristic_func(start, goal)
    heapq.heappush(open_heap, (h_start, 0, insertion_order, start))

    g_score = {start: 0}
    parent = {start: None}
    closed = set()
    processed_count = 0

    while open_heap:
        f, g, _, curr = heapq.heappop(open_heap)
        if curr in closed:
            continue
        closed.add(curr)
        processed_count += 1

        if curr == goal:
            break

        for nxt in get_neighbors(*curr):
            step_cost = cost_matrix[nxt[0]][nxt[1]] if cost_matrix else 1
            tentative_g = g_score[curr] + step_cost

            if tentative_g < g_score.get(nxt, float('inf')):
                g_score[nxt] = tentative_g
                parent[nxt] = curr
                insertion_order += 1
                h = heuristic_func(nxt, goal)
                heapq.heappush(open_heap, (tentative_g + h, tentative_g, insertion_order, nxt))

    # Восстановление маршрута
    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr)
    path.reverse()

    cost = g_score.get(goal, 0)
    return path, cost, processed_count


# ---------------------------------------------------------------------
# Задание 6: Алгоритм Дейкстры и итоговое сравнение
# ---------------------------------------------------------------------

def dijkstra(start, goal, cost_matrix=None):
    open_heap = []
    insertion_order = 0
    heapq.heappush(open_heap, (0, insertion_order, start))

    dist = {start: 0}
    parent = {start: None}
    closed = set()
    processed_count = 0

    while open_heap:
        d, _, curr = heapq.heappop(open_heap)
        if curr in closed:
            continue
        closed.add(curr)
        processed_count += 1

        if curr == goal:
            break

        for nxt in get_neighbors(*curr):
            step_cost = cost_matrix[nxt[0]][nxt[1]] if cost_matrix else 1
            if dist[curr] + step_cost < dist.get(nxt, float('inf')):
                dist[nxt] = dist[curr] + step_cost
                parent[nxt] = curr
                insertion_order += 1
                heapq.heappush(open_heap, (dist[nxt], insertion_order, nxt))

    # Восстановление маршрута
    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr)
    path.reverse()

    return path, dist.get(goal, 0), processed_count


def calculate_path_cost(path, cost_matrix=None):
    # Старт бесплатный, стоимость переходов определяется входом в клетки
    if not path or len(path) < 2:
        return 0
    if not cost_matrix:
        return len(path) - 1
    return sum(cost_matrix[r][c] for r, c in path[1:])


# ---------------------------------------------------------------------
# Тесты
# ---------------------------------------------------------------------

def main():
    print("-" * 70)
    print("Задание 1: DSU и минимальное остовное дерево")
    print("-" * 70)
    mst_edges, mst_weight = kraskal(graph_edges)
    print("Рёбра минимального остовного дерева (MST):")
    for u, v, w in mst_edges:
        print(f"  {u} - {v} : вес {w}")
    print(f"Суммарный вес MST: {mst_weight}")

# -----------------------------------------------------------------------------------------------------

    print("\n" + "-" * 70)
    print("Задание 2: Пространство состояний и базовый BFS")
    print("-" * 70)
    bfs_path, bfs_processed = bfs(START, GOAL)
    bfs_steps = len(bfs_path) - 1
    print(f"Старт: {START}, Цель: {GOAL}")
    print(f"Длина пути (количество шагов): {bfs_steps}")
    print(f"Количество обработанных клеток: {bfs_processed}")
    print(f"Маршрут: {bfs_path}")
    print("\nВизуализация маршрута (*):")
    print(render_grid_with_path(GRID, bfs_path))

# -----------------------------------------------------------------------------------------------------

    print("\n" + "-" * 70)
    print("Задание 3: Эвристические функции")
    print("-" * 70)
    test_cells = [(0, 0), (6, 0), (6, 6), (7, 9), (11, 9)]
    print(f"Координаты цели G: {GOAL}")
    print(f"{'Клетка':<12} | {'Манхэттенское':<15} | {'Евклидово':<15}")
    print("-" * 46)
    for c in test_cells:
        m_val = manhattan(c, GOAL)
        e_val = euclidean(c, GOAL)
        print(f"{str(c):<12} | {m_val:<15} | {e_val:<15.4f}")

# -----------------------------------------------------------------------------------------------------

    print("\n" + "-" * 70)
    print("Задание 4: Greedy Best-First Search")
    print("-" * 70)
    greedy_path, greedy_processed = greedy_bfs(START, GOAL, manhattan)
    greedy_steps = len(greedy_path) - 1
    print(f"Длина маршрута Greedy (шагов): {greedy_steps}")
    print(f"Количество обработанных клеток: {greedy_processed}")
    print(f"Маршрут Greedy: {greedy_path}")
    print("\nВизуализация маршрута Greedy (*):")
    print(render_grid_with_path(GRID, greedy_path))

# -----------------------------------------------------------------------------------------------------

    print("\n" + "-" * 70)
    print("Задание 5: Алгоритм A*")
    print("-" * 70)
    astar_m_path, astar_m_cost, astar_m_processed = a_star(START, GOAL, manhattan)
    astar_e_path, astar_e_cost, astar_e_processed = a_star(START, GOAL, euclidean)
    
    print(f"A* (Манхэттен): длина = {len(astar_m_path) - 1} шагов, стоимость = {astar_m_cost}, обработано = {astar_m_processed}")
    print(f"A* (Евклид):    длина = {len(astar_e_path) - 1} шагов, стоимость = {astar_e_cost}, обработано = {astar_e_processed}")

# -----------------------------------------------------------------------------------------------------

    print("\n" + "-" * 70)
    print("Задание 6: Итоговое сравнение BFS, Дейкстры, Greedy и A*")
    print("-" * 70)
    
    # Стоимость входа в клетки (6,2), (6,3), (6,4), (6,5), (6,6) равна 5, остальные - 1
    weighted_cells = {(6, 2), (6, 3), (6, 4), (6, 5), (6, 6)}
    cost_matrix = [[5 if (r, c) in weighted_cells else 1 for c in range(COLS)] for r in range(ROWS)]

    # Запуск Дейкстры и A* на взвешенном поле
    dijkstra_path_w, dijkstra_cost_w, dijkstra_proc_w = dijkstra(START, GOAL, cost_matrix)
    astar_m_path_w, astar_m_cost_w, astar_m_proc_w = a_star(START, GOAL, manhattan, cost_matrix)

    # Стоимость маршрута BFS на взвешенном поле
    bfs_cost_on_weighted = calculate_path_cost(bfs_path, cost_matrix)
    print(f"Маршрут BFS на взвешенном поле: длина = {len(bfs_path) - 1} шагов, стоимость = {bfs_cost_on_weighted}")
    print(f"Маршрут Дейкстры на взвешенном поле: длина = {len(dijkstra_path_w) - 1} шагов, стоимость = {dijkstra_cost_w}")
    print(f"Маршрут A* на взвешенном поле: длина = {len(astar_m_path_w) - 1} шагов, стоимость = {astar_m_cost_w}")


if __name__ == "__main__":
    main()
