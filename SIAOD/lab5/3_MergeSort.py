cargo_priority = [42, 17, 93, 58, 11, 76, 24, 65, 39, 88, 5, 71, 30, 54, 19, 93, 7, 80, 80, 48, 77, 98, 97, 56, 27, 94, 73, 74, 72, 47, 95, 70, 96, 93, 84, 53, 38, 90, 94, 85, 34, 88, 56, 29, 65, 84, 72, 60, 63, 59, 61, 61, 14, 42, 89, 97, 62, 27, 19, 36, 18, 89, 3, 64, 99, 38, 26, 99, 55, 40, 32, 99, 86, 44, 1, 100, 53, 74, 78, 68, 21, 24, 85, 32, 99, 68, 85, 12, 4, 18, 69, 46, 46, 50, 64, 7, 68, 27, 98, 77, 41, 76, 12, 12, 62, 75, 29, 52, 12, 91, 73, 14, 22, 47, 47, 16, 25, 64, 54, 66, 89, 20, 68, 82, 4, 7, 58, 42, 13, 3, 60, 10, 52, 25, 98, 64, 86, 48, 44, 38, 2, 33, 14, 28, 29, 40, 23, 83, 47, 35]

def merge_sort_recursive(arr):
   comparisons = [0]
   max_depth = [0]
   
   def merge(left, right):
       result = []
       i = j = 0
       while i < len(left) and j < len(right):
           comparisons[0] += 1
           if left[i] <= right[j]:
               result.append(left[i])
               i += 1
           else:
               result.append(right[j])
               j += 1
       result.extend(left[i:])
       result.extend(right[j:])
       return result

   def sort_logic(data, depth):
       max_depth[0] = max(max_depth[0], depth)
       if len(data) <= 1:
           return data
       mid = len(data) // 2
       left = sort_logic(data[:mid], depth + 1)
       right = sort_logic(data[mid:], depth + 1)
       return merge(left, right)

   sorted_arr = sort_logic(arr, 0)
   return sorted_arr, comparisons[0], max_depth[0]

def merge_sort_iterative(arr):
   data = arr.copy()
   n = len(data)
   temp = [0] * n
   comparisons = 0
   passes = 0
   width = 1
   while width < n:
       passes += 1
       for i in range(0, n, 2 * width):
           left = i
           mid = min(i + width, n)
           right = min(i + 2 * width, n)
           
           l, r, t = left, mid, left
           while l < mid and r < right:
               comparisons += 1
               if data[l] <= data[r]:
                   temp[t] = data[l]
                   l += 1
               else:
                   temp[t] = data[r]
                   r += 1
               t += 1
           while l < mid:
               temp[t] = data[l]
               l += 1
               t += 1
           while r < right:
               temp[t] = data[r]
               r += 1
               t += 1
           for k in range(left, right):
               data[k] = temp[k]
       width *= 2
   return data, comparisons, passes

print("--- Сортировка слиянием ---")
print(f"Исходный: {cargo_priority}")

r_arr, r_comp, r_depth = merge_sort_recursive(cargo_priority)
print(f"Рекурсивная: Сравнений = {r_comp}, Макс. глубина = {r_depth}")

i_arr, i_comp, i_pass = merge_sort_iterative(cargo_priority)
print(f"Итерационная: Сравнений = {i_comp}, Проходов = {i_pass}")