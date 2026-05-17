def bubble_sort(arr):
   data = arr.copy()
   n = len(data)
   comparisons, swaps, passes = 0, 0, 0
   for i in range(n - 1):
       passes += 1
       swapped = False
       for j in range(n - i - 1):
           comparisons += 1
           if data[j] > data[j + 1]:
               data[j], data[j + 1] = data[j + 1], data[j]
               swaps += 1
               swapped = True
       if not swapped:
           break
   return data, comparisons, swaps, passes

def selection_sort(arr):
   data = arr.copy()
   n = len(data)
   comparisons, swaps, passes = 0, 0, 0
   for i in range(n - 1):
       passes += 1
       min_idx = i
       for j in range(i + 1, n):
           comparisons += 1
           if data[j] < data[min_idx]:
               min_idx = j
       if min_idx != i:
           data[i], data[min_idx] = data[min_idx], data[i]
           swaps += 1
   return data, comparisons, swaps, passes

def insertion_sort(arr):
   data = arr.copy()
   n = len(data)
   comparisons, shifts, passes = 0, 0, 0
   for i in range(1, n):
       passes += 1
       key = data[i]
       j = i - 1
       while j >= 0:
           comparisons += 1
           if data[j] > key:
               data[j + 1] = data[j]
               shifts += 1
               j -= 1
           else:
               break
       data[j + 1] = key
   return data, comparisons, shifts, passes

datasets = {
   "data_random": [57, 12, 89, 34, 76, 11, 90, 43, 65, 28, 71, 5, 39, 84, 22],
   "data_sorted": [5, 11, 12, 22, 28, 34, 39, 43, 57, 65, 71, 76, 84, 89, 90],
   "data_reverse": [90, 89, 84, 76, 71, 65, 57, 43, 39, 34, 28, 22, 12, 11, 5],
   "data_almost_sorted": [5, 11, 12, 22, 28, 34, 43, 39, 57, 65, 71, 76, 84, 89, 90]
}

for name, data in datasets.items():
   print(f"\n--- Данные: {name} ---")
   print(f"Исходный: {data}")
   
   b_arr, b_comp, b_swap, b_pass = bubble_sort(data)
   print(f"Пузырек: {b_arr} | Сравнений: {b_comp}, Обменов: {b_swap}, Проходов: {b_pass}")
   
   s_arr, s_comp, s_swap, s_pass = selection_sort(data)
   print(f"Выбором: {s_arr} | Сравнений: {s_comp}, Обменов: {s_swap}, Проходов: {s_pass}")
   
   i_arr, i_comp, i_shift, i_pass = insertion_sort(data)
   print(f"Вставками: {i_arr} | Сравнений: {i_comp}, Сдвигов: {i_shift}, Проходов: {i_pass}")