class DynamicArray:
   def __init__(self):
       self.capacity = 1
       self.size = 0
       self.array = [None] * self.capacity

   def append(self, element):
       if self.size == self.capacity:
           self._resize(2 * self.capacity)
       self.array[self.size] = element
       self.size += 1

   def insert_by_index(self, index, element):
       if index < 0 or index > self.size:
           raise IndexError("Индекс вне диапазона")
       if self.size == self.capacity:
           self._resize(2 * self.capacity)
       for i in range(self.size - 1, index - 1, -1):
           self.array[i + 1] = self.array[i]
       self.array[index] = element
       self.size += 1

   def delete_by_index(self, index):
       if index < 0 or index >= self.size:
           raise IndexError("Индекс вне диапазона")
       for i in range(index, self.size - 1):
           self.array[i] = self.array[i + 1]
       self.array[self.size - 1] = None
       self.size -= 1

   def get_by_index(self, index):
       if index < 0 or index >= self.size:
           raise IndexError("Индекс вне диапазона")
       return self.array[index]

   def get_size(self):
       return self.size

   def _resize(self, new_capacity):
       new_array = [None] * new_capacity
       for i in range(self.size):
           new_array[i] = self.array[i]
       self.capacity = new_capacity
       self.array = new_array

   def __str__(self):
       return str([self.array[i] for i in range(self.size)])

arr = DynamicArray()
for val in [5, 0, 1, 7, 9, 4, 6, 2, 1]:
   arr.append(val)

arr.insert_by_index(7, 8)
arr.delete_by_index(5)

print(f"Содержимое списка: {arr}")
print(f"Размер списка: {arr.get_size()}")