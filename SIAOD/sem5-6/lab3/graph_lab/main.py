import heapq
import sys

sys.stdout.reconfigure(encoding='utf-8')

edges = [
    (0, 1, 4),
    (0, 2, 8),
    (1, 2, 1),
    (2, 0, 3),
    (2, 3, 2),
    (3, 4, 2),
    (4, 5, 3),
    (5, 3, 1),
    (5, 6, 4),
    (6, 7, 2),
]

vertices = list(range(8))

adj_g = {v: [] for v in vertices}
adj_gu = {v: [] for v in vertices}

for u, v, w in edges:
    adj_g[u].append((v, w))
    if v not in adj_gu[u]:
        adj_gu[u].append(v)
    if u not in adj_gu[v]:
        adj_gu[v].append(u)

print("=== Задание 1 ===")
print("Список смежности ориентированного графа G:")
for v in vertices:
    print(f"{v}: {adj_g[v]}")

print("\nСписок смежности неориентированной проекции G_u:")
for v in vertices:
    print(f"{v}: {adj_gu[v]}")

def dfs_order_func(graph, start):
    visited = set()
    order = []
    def dfs(curr):
        visited.add(curr)
        order.append(curr)
        for neighbor in graph[curr]:
            if neighbor not in visited:
                dfs(neighbor)
    dfs(start)
    return order

print("\nПорядок посещения вершин при DFS для G_u из вершины 0:")
print(dfs_order_func(adj_gu, 0))

def find_components(graph):
    visited = set()
    components = []
    for v in graph:
        if v not in visited:
            comp = []
            def dfs(curr):
                visited.add(curr)
                comp.append(curr)
                for neighbor in graph[curr]:
                    if neighbor not in visited:
                        dfs(neighbor)
            dfs(v)
            components.append(comp)
    return components

comp_initial = find_components(adj_gu)
print(f"\nКоличество компонент связности исходного G_u: {len(comp_initial)}")
print(f"Компоненты связности: {comp_initial}")

adj_gu_copy = {v: list(adj_gu[v]) for v in adj_gu}
adj_gu_copy[5].remove(6)
adj_gu_copy[6].remove(5)
comp_after_remove_5_6 = find_components(adj_gu_copy)
print(f"\nПосле удаления ребра {{5, 6}}:")
print(f"Количество компонент связности: {len(comp_after_remove_5_6)}")
print(f"Компоненты связности: {comp_after_remove_5_6}")

print("\n=== Задание 2 ===")
adj_g_dir = {v: [] for v in vertices}
for u, v, _ in edges:
    adj_g_dir[u].append(v)

def kosaraju(graph, v_list):
    visited = set()
    order = []
    def dfs1(curr):
        visited.add(curr)
        for neighbor in graph[curr]:
            if neighbor not in visited:
                dfs1(neighbor)
        order.append(curr)

    for v in v_list:
        if v not in visited:
            dfs1(v)

    transposed = {v: [] for v in v_list}
    for u in v_list:
        for to in graph[u]:
            transposed[to].append(u)

    visited.clear()
    sccs = []
    for v in reversed(order):
        if v not in visited:
            comp = []
            def dfs2(curr):
                visited.add(curr)
                comp.append(curr)
                for neighbor in transposed[curr]:
                    if neighbor not in visited:
                        dfs2(neighbor)
            dfs2(v)
            sccs.append(sorted(comp))
    return sccs

sccs = kosaraju(adj_g_dir, vertices)
sccs.sort(key=lambda c: c[0])
print("Найденные компоненты сильной связности (SCC):")
for idx, comp in enumerate(sccs):
    print(f"Компонента {idx}: {comp}")

print("\n=== Задание 3 ===")
tin = {}
low = {}
timer = 0
visited_bridge = set()
bridges = []
cutpoints = set()

def dfs_bridges_cutpoints(v, p=-1):
    global timer
    visited_bridge.add(v)
    tin[v] = low[v] = timer
    timer += 1
    children = 0
    for to in adj_gu[v]:
        if to == p:
            continue
        if to in visited_bridge:
            low[v] = min(low[v], tin[to])
        else:
            dfs_bridges_cutpoints(to, v)
            low[v] = min(low[v], low[to])
            if low[to] > tin[v]:
                bridges.append((v, to))
            if low[to] >= tin[v] and p != -1:
                cutpoints.add(v)
            children += 1
    if p == -1 and children > 1:
        cutpoints.add(v)

dfs_bridges_cutpoints(0, -1)

print("Найденные мосты:")
for b in bridges:
    print(f"{{{b[0]}, {b[1]}}}")

print("\nНайденные точки сочленения:")
print(sorted(list(cutpoints)))

print("\nТаблица значений tin и low:")
print("Вершина | tin | low")
print("--------+-----+----")
for v in sorted(vertices):
    print(f"   {v}    |  {tin[v]}  |  {low[v]}")

adj_gu_bridge_removed = {v: list(adj_gu[v]) for v in adj_gu}
chosen_bridge = bridges[0]
adj_gu_bridge_removed[chosen_bridge[0]].remove(chosen_bridge[1])
adj_gu_bridge_removed[chosen_bridge[1]].remove(chosen_bridge[0])
comp_bridge_removed = find_components(adj_gu_bridge_removed)
print(f"\nПосле удаления моста {{{chosen_bridge[0]}, {chosen_bridge[1]}}}:")
print(f"Количество компонент связности: {len(comp_bridge_removed)}")
print(f"Компоненты связности: {comp_bridge_removed}")

print("\n=== Задание 4 ===")
node_to_scc = {}
for idx, comp in enumerate(sccs):
    for node in comp:
        node_to_scc[node] = idx

cond_adj = {i: [] for i in range(len(sccs))}
for u, v, _ in edges:
    cu = node_to_scc[u]
    cv = node_to_scc[v]
    if cu != cv and cv not in cond_adj[cu]:
        cond_adj[cu].append(cv)

print("Список смежности графа конденсации:")
for idx in range(len(sccs)):
    print(f"Компонента {idx} {sccs[idx]} -> {[f'Компонента {to} {sccs[to]}' for to in cond_adj[idx]]}")

def topo_sort(graph):
    state = {v: 0 for v in graph}
    order = []
    has_cycle = False
    def dfs(curr):
        nonlocal has_cycle
        state[curr] = 1
        for to in graph[curr]:
            if state[to] == 1:
                has_cycle = True
            elif state[to] == 0:
                dfs(to)
        state[curr] = 2
        order.append(curr)
    for v in graph:
        if state[v] == 0:
            dfs(v)
    if has_cycle:
        return None
    return order[::-1]

topo_result = topo_sort(cond_adj)
print("\nТопологический порядок компонент:")
for comp_idx in topo_result:
    print(f"Компонента {comp_idx}: {sccs[comp_idx]}")

cond_adj_modified = {k: list(v) for k, v in cond_adj.items()}
c_from = node_to_scc[7]
c_to = node_to_scc[3]
cond_adj_modified[c_from].append(c_to)

print(f"\nДобавлено ребро от компоненты {c_from} (содержит 7) к компоненте {c_to} (содержит 3).")
topo_cycle_check = topo_sort(cond_adj_modified)
if topo_cycle_check is None:
    print("Обнаружен цикл в графе конденсации: топологическая сортировка невозможна.")
else:
    print("Топологический порядок:", topo_cycle_check)

print("\n=== Задание 5 ===")
def dijkstra(start, graph, n):
    dist = [float('inf')] * n
    parent = [None] * n
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        cur_d, u = heapq.heappop(heap)
        if cur_d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, parent

dijkstra_dist, dijkstra_parent = dijkstra(0, adj_g, len(vertices))
print("Кратчайшие расстояния от вершины 0 до всех вершин:")
print(dijkstra_dist)

def restore_path(parent, target):
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    return path[::-1]

path_7 = restore_path(dijkstra_parent, 7)
print(f"Кратчайший маршрут от 0 до 7: {' -> '.join(map(str, path_7))}")
print(f"Длина маршрута: {dijkstra_dist[7]}")

print("\n=== Задание 6 ===")
edges_bf1 = list(edges)
for i in range(len(edges_bf1)):
    if edges_bf1[i][0] == 2 and edges_bf1[i][1] == 3:
        edges_bf1[i] = (2, 3, -2)

def bellman_ford(start, edge_list, n):
    dist = [float('inf')] * n
    dist[start] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edge_list:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    has_neg_cycle = False
    for u, v, w in edge_list:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            has_neg_cycle = True
            break
    return dist, has_neg_cycle

dist_bf1, neg_cycle_1 = bellman_ford(0, edges_bf1, len(vertices))
print("Результат Беллмана-Форда с ребром (2, 3, -2):")
if neg_cycle_1:
    print("Обнаружен отрицательный цикл.")
else:
    print(f"Отрицательный цикл не обнаружен. Расстояния: {dist_bf1}")

edges_bf2 = list(edges_bf1)
for i in range(len(edges_bf2)):
    if edges_bf2[i][0] == 4 and edges_bf2[i][1] == 5:
        edges_bf2[i] = (4, 5, -4)

dist_bf2, neg_cycle_2 = bellman_ford(0, edges_bf2, len(vertices))
print("\nРезультат Беллмана-Форда с рёбрами (2, 3, -2) и (4, 5, -4):")
if neg_cycle_2:
    print("Обнаружен отрицательный цикл.")
else:
    print(f"Отрицательный цикл не обнаружен. Расстояния: {dist_bf2}")

print("\n=== Задание 7 ===")
n = len(vertices)
matrix = [[float('inf')] * n for _ in range(n)]
for i in range(n):
    matrix[i][i] = 0
for u, v, w in edges:
    matrix[u][v] = w

dist_floyd = [row[:] for row in matrix]
for k in range(n):
    for i in range(n):
        for j in range(n):
            if dist_floyd[i][k] != float('inf') and dist_floyd[k][j] != float('inf'):
                if dist_floyd[i][k] + dist_floyd[k][j] < dist_floyd[i][j]:
                    dist_floyd[i][j] = dist_floyd[i][k] + dist_floyd[k][j]

print("Итоговая матрица кратчайших расстояний (Флойд-Уоршелл):")
header = "     " + " ".join(f"{v:>5}" for v in vertices)
print(header)
for i in range(n):
    row_str = f"{i:>3}: " + " ".join(f"{dist_floyd[i][j]:>5}" if dist_floyd[i][j] != float('inf') else "  inf" for j in range(n))
    print(row_str)

row_0 = dist_floyd[0]
print("\nСравнение строки 0 матрицы Флойда-Уоршелла с результатом Дейкстры:")
print(f"Флойд-Уоршелл (строка 0): {row_0}")
print(f"Дейкстра (от вершины 0): {dijkstra_dist}")
print(f"Результаты совпадают: {row_0 == dijkstra_dist}")
