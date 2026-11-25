import statistics
from collections import Counter
from data import events, hash64


class CountSketch:
    def __init__(self, width, depth, seed=2026):
        self.width = width
        self.depth = depth
        self.seed = seed
        self.table = [[0] * width for _ in range(depth)]

    def _bucket(self, row, key):
        return hash64(f"{self.seed}_b_{row}_{key}") % self.width

    def _sign(self, row, key):
        return 1 if (hash64(f"{self.seed}_s_{row}_{key}") & 1) else -1

    def add(self, key, delta=1):
        for j in range(self.depth):
            c = self._bucket(j, key)
            s = self._sign(j, key)
            self.table[j][c] += s * delta

    def estimate(self, key):
        estimates = []
        for j in range(self.depth):
            c = self._bucket(j, key)
            s = self._sign(j, key)
            estimates.append(s * self.table[j][c])
        return statistics.median(estimates)


def count_sketch_test():
    print("--- Задание 2 ---")
    user_ids = [e["user_id"] for e in events]
    exact = Counter(user_ids)

    sample_users = ["user_0000", "user_1000"] + [f"user_{i:04d}" for i in range(1, 21)]

    results = []
    for w in [64, 256, 1024]:
        cs = CountSketch(width=w, depth=5, seed=2026)
        for uid in user_ids:
            cs.add(uid, 1)

        mae_sample = sum(abs(cs.estimate(u) - exact[u]) for u in sample_users) / len(sample_users)
        mae_all = sum(abs(cs.estimate(u) - exact[u]) for u in exact) / len(exact)

        results.append({
            "width": w,
            "depth": 5,
            "mae_sample": mae_sample,
            "mae_all": mae_all,
            "sketch": cs,
        })

        print(f"Таблица w = {w:4d}, d = 5: MAE (выборка 22 ключа) = {mae_sample:.2f}, MAE (все 1968 ключей) = {mae_all:.2f}")

    print("\nСравнение оценок при w = 256, d = 5:")
    cs256 = results[1]["sketch"]
    print(f"{'Пользователь':<12} | {'Эталон':<8} | {'Count Sketch':<12} | {'Разность':<8}")
    print("-" * 48)
    for u in sample_users:
        est = cs256.estimate(u)
        ex = exact[u]
        print(f"{u:<12} | {ex:<8} | {est:<12.1f} | {est - ex:<+8.1f}")
    return results


if __name__ == "__main__":
    count_sketch_test()
