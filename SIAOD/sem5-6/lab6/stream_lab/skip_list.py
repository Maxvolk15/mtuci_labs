from random import Random
from data import events


class Node:
    def __init__(self, key, value, level):
        self.key = key
        self.value = value
        self.forward = [None] * level


class SkipList:
    def __init__(self, max_level=12, p=0.5, seed=2026):
        self.max_level = max_level
        self.p = p
        self.rng = Random(seed)
        self.head = Node(None, None, max_level)
        self.level = 1

    def _random_level(self):
        lvl = 1
        while self.rng.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, key, value):
        update = [None] * self.max_level
        curr = self.head

        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] and curr.forward[i].key < key:
                curr = curr.forward[i]
            update[i] = curr

        curr = curr.forward[0]
        if curr and curr.key == key:
            curr.value = value
            return

        new_level = self._random_level()
        if new_level > self.level:
            for i in range(self.level, new_level):
                update[i] = self.head
            self.level = new_level

        new_node = Node(key, value, new_level)
        for i in range(new_level):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def search(self, key):
        curr = self.head
        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] and curr.forward[i].key < key:
                curr = curr.forward[i]
        curr = curr.forward[0]
        if curr and curr.key == key:
            return curr.value
        return None

    def delete(self, key):
        update = [None] * self.max_level
        curr = self.head

        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] and curr.forward[i].key < key:
                curr = curr.forward[i]
            update[i] = curr

        curr = curr.forward[0]
        if curr and curr.key == key:
            for i in range(self.level):
                if update[i].forward[i] != curr:
                    break
                update[i].forward[i] = curr.forward[i]

            while self.level > 1 and self.head.forward[self.level - 1] is None:
                self.level -= 1
            return True
        return False

    def items(self):
        res = []
        curr = self.head.forward[0]
        while curr:
            res.append((curr.key, curr.value))
            curr = curr.forward[0]
        return res


def skip_list_test():
    print("--- Задание 5 ---")
    first_2000 = events[:2000]

    rng_shuffle = Random(2027)
    shuffled_events = list(first_2000)
    rng_shuffle.shuffle(shuffled_events)

    first_5_keys = [e["timestamp"] for e in shuffled_events[:5]]
    print(f"Первые 5 ключей входной перемешанной последовательности: {first_5_keys}")

    sl = SkipList(max_level=12, p=0.5, seed=2026)
    for e in shuffled_events:
        sl.insert(e["timestamp"], e["duration_ms"])

    res_0 = sl.search(0)
    res_999 = sl.search(999)
    res_1999 = sl.search(1999)
    res_missing = sl.search(5000)

    print(f"Поиск ключа 0: {res_0}")
    print(f"Поиск ключа 999: {res_999}")
    print(f"Поиск ключа 1999: {res_1999}")
    print(f"Поиск отсутствующего ключа 5000: {res_missing} (возвращён None: {res_missing is None})")

    deleted = sl.delete(999)
    res_999_after = sl.search(999)
    res_998_after = sl.search(998)
    res_1000_after = sl.search(1000)

    print(f"\nУдаление ключа 999 выполнено: {deleted}")
    print(f"Повторный поиск ключа 999: {res_999_after}")
    print(f"Проверка соседних ключей: ключ 998 = {res_998_after}, ключ 1000 = {res_1000_after}")

    all_items = sl.items()
    is_sorted = all(all_items[i][0] < all_items[i + 1][0] for i in range(len(all_items) - 1))
    print(f"Всего элементов в Skip List: {len(all_items)}")
    print(f"Ключи в items() отсортированы по возрастанию: {is_sorted}")

    return {
        "first_5_keys": first_5_keys,
        "search_0": res_0,
        "search_999": res_999,
        "search_1999": res_1999,
        "search_missing": res_missing,
        "deleted_999": deleted,
        "search_999_after": res_999_after,
        "is_sorted": is_sorted,
        "total_items": len(all_items),
    }


if __name__ == "__main__":
    skip_list_test()
