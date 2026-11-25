import math
from data import events, hash64


class HyperLogLog:
    def __init__(self, p):
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m

    def _rho(self, suffix):
        w = 64 - self.p
        if suffix == 0:
            return w + 1
        return (w - suffix.bit_length()) + 1

    def add(self, key):
        x = hash64(key)
        idx = x >> (64 - self.p)
        suffix = x & ((1 << (64 - self.p)) - 1)
        r = self._rho(suffix)
        if r > self.registers[idx]:
            self.registers[idx] = r

    def count(self):
        m = self.m
        alpha = 0.7213 / (1.0 + 1.079 / m)

        z = sum(2.0 ** (-r) for r in self.registers)
        E = alpha * (m ** 2) / z

        V = self.registers.count(0)
        if V > 0 and E <= 2.5 * m:
            E = m * math.log(m / V)

        return E


def hyperloglog_test():
    print("--- Задание 3 ---")
    user_ids = [e["user_id"] for e in events]
    exact_cardinality = len(set(user_ids))
    print(f"Точное число уникальных пользователей: {exact_cardinality}")

    results = []
    for p in [6, 8, 10]:
        hll = HyperLogLog(p=p)
        for uid in user_ids:
            hll.add(uid)

        estimate = hll.count()
        rel_error = abs(estimate - exact_cardinality) / exact_cardinality * 100.0

        for uid in user_ids:
            hll.add(uid)
        estimate_repeat = hll.count()

        results.append({
            "p": p,
            "m": 1 << p,
            "estimate": estimate,
            "rel_error": rel_error,
            "estimate_repeat": estimate_repeat,
        })

        print(f"p = {p:2d} (m = {1 << p:4d} регистров): "
              f"Оценка = {estimate:.1f}, "
              f"Относительная ошибка = {rel_error:.2f}%, "
              f"Повтор = {estimate_repeat:.1f}")

    return results


if __name__ == "__main__":
    hyperloglog_test()
