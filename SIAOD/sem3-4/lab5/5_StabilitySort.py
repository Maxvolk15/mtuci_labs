records1 = [("A1", 4), ("A2", 2), ("A3", 4), ("A4", 1), ("A5", 3), ("A6", 2), ("A7", 4), ("A8", 1), ("A9", 3), ("A10", 2)]

def bubble_sort_tuples(arr):
   data = arr.copy()
   for i in range(len(data) - 1):
       for j in range(len(data) - i - 1):
           if data[j][1] > data[j + 1][1]:
               data[j], data[j + 1] = data[j + 1], data[j]
   return data

def selection_sort_tuples(arr):
   data = arr.copy()
   for i in range(len(data) - 1):
       min_idx = i
       for j in range(i + 1, len(data)):
           if data[j][1] < data[min_idx][1]:
               min_idx = j
       if min_idx != i:
           data[i], data[min_idx] = data[min_idx], data[i]
   return data

print("Исходный массив:", records1)

sorted_bubble = bubble_sort_tuples(records1)
print("Пузырек (Устойчивый):", sorted_bubble)

sorted_selection = selection_sort_tuples(records1)
print("Выбором (Неустойчивый):", sorted_selection)