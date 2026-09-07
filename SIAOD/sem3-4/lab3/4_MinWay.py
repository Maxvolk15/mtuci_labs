grid = [
    [((i * 13 + j * 19 + 5) % 7) + 1 for j in range(128)]
    for i in range(128)
]

for i in range(40, 90):
    for j in range(50, 55):
        grid[i][j] = 20

for i in range(70, 100):
    for j in range(80, 120):
        grid[i][j] = 15


def min_way(grid):
    n = len(grid)
    m = len(grid[0])

    dp = [[0] * m for _ in range(n)]
    parent = [[None] * m for _ in range(n)]

    dp[0][0] = grid[0][0]

    for i in range(1, n):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
        parent[i][0] = (i - 1, 0)

    for j in range(1, m):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
        parent[0][j] = (0, j - 1)

    for i in range(1, n):
        for j in range(1, m):
            if dp[i - 1][j] <= dp[i][j - 1]:
                dp[i][j] = dp[i - 1][j] + grid[i][j]
                parent[i][j] = (i - 1, j)
            else:
                dp[i][j] = dp[i][j - 1] + grid[i][j]
                parent[i][j] = (i, j - 1)

    path = []
    i, j = n - 1, m - 1

    while True:
        path.append((i, j))
        if i == 0 and j == 0:
            break
        i, j = parent[i][j]

    path.reverse()
    return dp[n - 1][m - 1], path

cost, path = min_way(grid)

print("Минимальная стоимость пути:", cost)
print("Длина пути в клетках:", len(path))
print("Координаты пути:")
print(path)
