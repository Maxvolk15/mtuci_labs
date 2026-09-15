class MinHeap:
    def __init__(self):
        self.data = []

    def push(self, value):
        self.data.append(value)
        self._sift_up(len(self.data) - 1)

    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.data[parent] <= self.data[index]:
                break
            self.data[parent], self.data[index] = self.data[index], self.data[parent]
            index = parent

    def pop(self):
        if not self.data:
            return None
        if len(self.data) == 1:
            return self.data.pop()
        
        root = self.data[0]
        self.data[0] = self.data.pop()
        self._sift_down(0)
        return root

    def _sift_down(self, index):
        size = len(self.data)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < size and self.data[left] < self.data[smallest]:
                smallest = left
            if right < size and self.data[right] < self.data[smallest]:
                smallest = right
                
            if smallest == index:
                break
                
            self.data[index], self.data[smallest] = self.data[smallest], self.data[index]
            index = smallest