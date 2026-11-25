import math
from data import events, hash64


class BloomFilter:
    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.size_bytes = (m + 7) // 8
        self.bits = bytearray(self.size_bytes)  #Для экономии, т.к. bytearray упаковывает ровно 1 бит в 1 бит памяти

    def _positions(self, key):
        # Хеширование Кирша-Митценмахера
        h1 = hash64(f"bf1_{key}")
        h2 = hash64(f"bf2_{key}")
        for i in range(self.k):
            yield (h1 + i * h2) % self.m    # Арифметическая прогрессия

    def add(self, key):
        for pos in self._positions(key):
            self.bits[pos // 8] |= (1 << (pos % 8))

    def contains(self, key):
        for pos in self._positions(key):
            if not (self.bits[pos // 8] & (1 << (pos % 8))):
                return False
        return True


def bloom_filter_test():
    print("--- Задание 1 ---")
    train_events = events[:8000]
    test_events = events[8000:]

    results = []
    for m in [32768, 65536, 131072]:
        bf = BloomFilter(m=m, k=5)
        for e in train_events:
            bf.add(e["event_id"])

        fn_count = sum(not bf.contains(e["event_id"]) for e in train_events)

        fp_count = sum(bf.contains(e["event_id"]) for e in test_events)
        fp_rate = fp_count / len(test_events)

        p_theory = (1.0 - math.exp(-5 * len(train_events) / m)) ** 5

        results.append({
            "m": m,
            "size_bytes": bf.size_bytes,
            "fn": fn_count,
            "fp": fp_count,
            "fp_rate": fp_rate,
            "p_theory": p_theory,
        })

        print(f"m = {m:6d} бит ({bf.size_bytes} байт): "
              f"FN = {fn_count}, FP = {fp_count}/{len(test_events)} ({fp_rate * 100:.2f}%), "
              f"Теория = {p_theory * 100:.2f}%")
    return results


if __name__ == "__main__":
    bloom_filter_test()
