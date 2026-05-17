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

def shaker_sort(arr):
   data = arr.copy()
   left, right = 0, len(data) - 1
   comparisons, swaps, passes = 0, 0, 0
   while left <= right:
       passes += 1
       swapped = False
       for i in range(left, right):
           comparisons += 1
           if data[i] > data[i + 1]:
               data[i], data[i + 1] = data[i + 1], data[i]
               swaps += 1
               swapped = True
       right -= 1
       if not swapped:
           break
       
       swapped = False
       for i in range(right, left, -1):
           comparisons += 1
           if data[i - 1] > data[i]:
               data[i - 1], data[i] = data[i], data[i - 1]
               swaps += 1
               swapped = True
       left += 1
       if not swapped:
           break
   return data, comparisons, swaps, passes

def gnome_sort(arr):
   data = arr.copy()
   n = len(data)
   comparisons, swaps, steps = 0, 0, 0
   index = 0
   while index < n:
       steps += 1
       if index == 0:
           index += 1
           continue
       comparisons += 1
       if data[index] >= data[index - 1]:
           index += 1
       else:
           data[index], data[index - 1] = data[index - 1], data[index]
           swaps += 1
           index -= 1
   return data, comparisons, swaps, steps

gnome_datasets = {
   "data1": [1, 2, 3, 4, 6, 5, 7, 8, 9, 10],
   "data2": [2, 1, 3, 4, 5, 6, 7, 8, 10, 9],
   "data3": [1, 3, 2, 4, 5, 7, 6, 8, 10, 9],
   "data4": [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]
}

for name, data in gnome_datasets.items():
   print(f"\n--- Данные: {name} ---")
   print(f"Исходный: {data}")
   
   s_arr, s_comp, s_swap, s_pass = shaker_sort(data)
   print(f"Перемешиванием: {s_arr} | Сравнений: {s_comp}, Перестановок: {s_swap}, Проходов: {s_pass}")
   
   g_arr, g_comp, g_swap, g_step = gnome_sort(data)
   print(f"Гномья: {g_arr} | Сравнений: {g_comp}, Перестановок: {g_swap}, Шагов: {g_step}")
   
   b_arr, b_comp, b_swap, b_pass = bubble_sort(data)
   print(f"Пузырек: {b_arr} | Сравнений: {b_comp}, Перестановок: {b_swap}, Проходов: {b_pass}")