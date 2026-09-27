def range_sum_naive(data, left, right):
    total = 0
    for i in range(left, right + 1):
        total += data[i]
    return total


def build_prefix(data):
    prefix = [0] * (len(data) + 1)
    for i in range(len(data)):
        prefix[i + 1] = prefix[i] + data[i]
    return prefix


def range_sum_prefix(prefix, left, right):
    return prefix[right + 1] - prefix[left]


class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def build(self, data):
        for i in range(len(data)):
            self.update(i + 1, data[i])

    def update(self, i, delta):
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def prefix_sum(self, i):
        result = 0
        while i > 0:
            result += self.tree[i]
            i -= i & (-i)
        return result

    def range_sum(self, left, right):
        return self.prefix_sum(right) - self.prefix_sum(left - 1)


class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.data = list(data)
        self.tree = [None] * (4 * self.n)
        if self.n > 0:
            self._build(1, 0, self.n - 1)

    def _build(self, node, start, end):
        if start == end:
            val = self.data[start]
            self.tree[node] = (val, val, val)
            return
        mid = (start + end) // 2
        self._build(2 * node, start, mid)
        self._build(2 * node + 1, mid + 1, end)
        self._merge(node)

    def _merge(self, node):
        left = self.tree[2 * node]
        right = self.tree[2 * node + 1]
        self.tree[node] = (
            left[0] + right[0],
            min(left[1], right[1]),
            max(left[2], right[2])
        )

    def query(self, left, right):
        return self._query(1, 0, self.n - 1, left, right)

    def _query(self, node, start, end, left, right):
        if right < start or end < left:
            return (0, float('inf'), float('-inf'))
        if left <= start and end <= right:
            return self.tree[node]
        mid = (start + end) // 2
        l_res = self._query(2 * node, start, mid, left, right)
        r_res = self._query(2 * node + 1, mid + 1, end, left, right)
        return (
            l_res[0] + r_res[0],
            min(l_res[1], r_res[1]),
            max(l_res[2], r_res[2])
        )

    def update(self, index, value):
        self.data[index] = value
        self._update(1, 0, self.n - 1, index, value)

    def _update(self, node, start, end, index, value):
        if start == end:
            self.tree[node] = (value, value, value)
            return
        mid = (start + end) // 2
        if index <= mid:
            self._update(2 * node, start, mid, index, value)
        else:
            self._update(2 * node + 1, mid + 1, end, index, value)
        self._merge(node)
