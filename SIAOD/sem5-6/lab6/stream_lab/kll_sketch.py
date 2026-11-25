import math
from random import Random
from data import events


class KLLSketch:
    def __init__(self, k, seed=2026):
        self.k = k
        self.rng = Random(seed)
        self.levels = [[]]

    def _capacity(self, i):
        h = len(self.levels) - 1
        return max(8, math.floor(self.k * ((2.0 / 3.0) ** (h - i))))

    def _compact_level(self, i):
        if i >= len(self.levels) - 1:
            self.levels.append([])

        lvl = self.levels[i]
        lvl.sort()
        offset = self.rng.choice([0, 1])

        if len(lvl) % 2 == 1:
            leftover = [lvl[-1]]
            pairs = lvl[:-1]
        else:
            leftover = []
            pairs = lvl

        promoted = pairs[offset::2]
        self.levels[i] = leftover
        self.levels[i + 1].extend(promoted)

    def _compress(self):
        while True:
            overflow = False
            for i in range(len(self.levels)):
                if len(self.levels[i]) > self._capacity(i):
                    self._compact_level(i)
                    overflow = True
                    break
            if not overflow:
                break

    def add(self, value):
        self.levels[0].append(value)
        if len(self.levels[0]) > self._capacity(0):
            self._compress()

    def stored_count(self):
        return sum(len(lvl) for lvl in self.levels)

    def total_weight(self):
        return sum(len(lvl) * (1 << i) for i, lvl in enumerate(self.levels))

    def quantile(self, q):
        items = []
        for i, lvl in enumerate(self.levels):
            w = 1 << i
            for v in lvl:
                items.append((v, w))

        items.sort(key=lambda x: x[0])
        total_w = sum(w for _, w in items)
        target = max(1, math.ceil(q * total_w))

        sm = 0
        for v, w in items:
            sm += w
            if sm >= target:
                return v
        return items[-1][0]


def kll_sketch_test():
    print("--- Задание 4 ---")
    durations = [e["duration_ms"] for e in events]
    n = len(durations)

    sorted_durations = sorted(durations)
    exact_p50 = sorted_durations[math.ceil(0.50 * n) - 1]
    exact_p90 = sorted_durations[math.ceil(0.90 * n) - 1]
    exact_p95 = sorted_durations[math.ceil(0.95 * n) - 1]
    print(f"Точные эталоны: P50 = {exact_p50} мс, P90 = {exact_p90} мс, P95 = {exact_p95} мс")

    results = []
    for k in [64, 128, 256]:
        kll = KLLSketch(k=k, seed=2026)
        for d in durations:
            kll.add(d)
        kll._compress()

        p50 = kll.quantile(0.50)
        p90 = kll.quantile(0.90)
        p95 = kll.quantile(0.95)
        stored = kll.stored_count()
        mass = kll.total_weight()

        results.append({
            "k": k,
            "stored": stored,
            "mass": mass,
            "p50": p50,
            "p90": p90,
            "p95": p95,
            "err_p50": abs(p50 - exact_p50),
            "err_p90": abs(p90 - exact_p90),
            "err_p95": abs(p95 - exact_p95),
        })

        print(f"k = {k:3d}: Сохранено = {stored:3d} элементов, масса = {mass:5d} (инвариант N={n} соблюдён: {mass == n})")
        print(f"        P50 = {p50:4d} мс (ошибка = {abs(p50 - exact_p50):2d} мс)")
        print(f"        P90 = {p90:4d} мс (ошибка = {abs(p90 - exact_p90):2d} мс)")
        print(f"        P95 = {p95:4d} мс (ошибка = {abs(p95 - exact_p95):2d} мс)")

    return results


if __name__ == "__main__":
    kll_sketch_test()
