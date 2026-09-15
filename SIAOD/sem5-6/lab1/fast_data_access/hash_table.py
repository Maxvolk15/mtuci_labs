class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0

    def set(self, key, value):
        index = hash(key) % self.size
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))
        self.count += 1

    def get(self, key):
        index = hash(key) % self.size
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def remove(self, key):
        index = hash(key) % self.size
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                self.count -= 1
                return

    @property
    def load_factor(self):
        return self.count / self.size

    def collision_count(self):
        count = 0
        for bucket in self.table:
            if len(bucket) > 1:
                count += len(bucket) - 1
        return count