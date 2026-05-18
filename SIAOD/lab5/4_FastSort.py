import random

orders_random = [57, 14, 83, 29, 61, 45, 72, 10, 34, 98, 21, 66, 39, 50, 7, 66, 28, 64, 72, 62, 66, 26, 8, 29, 89, 35, 15, 32, 27, 55, 3, 59, 100, 21, 56, 85, 36, 23, 75, 18, 49, 18, 78, 44, 59, 59, 96, 68, 23, 81, 89, 4, 25, 90, 92, 72, 8, 82, 89, 44, 82, 55, 49, 23, 49, 80, 22, 84, 67, 21, 88, 65, 73, 99, 88, 49, 92, 39, 83, 66, 83, 26, 53, 75, 56, 94, 59, 89, 71, 37, 64, 99, 96, 73, 83, 30, 79, 78, 29, 7]

def partition_lomuto(arr, left, right, pivot_type, stats):
   if pivot_type == 'mid':
       mid = (left + right) // 2
       arr[mid], arr[right] = arr[right], arr[mid]
   elif pivot_type == 'rand':
       rand_idx = random.randint(left, right)
       arr[rand_idx], arr[right] = arr[right], arr[rand_idx]
   
   pivot = arr[right]
   i = left - 1
   
   if stats['partition_calls'] < 3:
       print(f"[Ломуто Шаг {stats['partition_calls']+1}] Границы: {left}..{right}, Опорный: {pivot}")

   for j in range(left, right):
       stats['comparisons'] += 1
       if arr[j] <= pivot:
           i += 1
           arr[i], arr[j] = arr[j], arr[i]
           stats['swaps'] += 1
           
   arr[i + 1], arr[right] = arr[right], arr[i + 1]
   stats['swaps'] += 1
   
   if stats['partition_calls'] < 3:
       print(f"Рез-т разбиения: {arr[left:right+1]}, Возврат: {i + 1}")
   stats['partition_calls'] += 1
   
   return i + 1

def partition_hoare(arr, left, right, pivot_type, stats):
   if pivot_type == 'mid':
       mid = (left + right) // 2
       arr[left], arr[mid] = arr[mid], arr[left]
   elif pivot_type == 'rand':
       rand_idx = random.randint(left, right)
       arr[left], arr[rand_idx] = arr[rand_idx], arr[left]
       
   pivot = arr[left]
   i = left - 1
   j = right + 1

   if stats['partition_calls'] < 3:
       print(f"[Хоар Шаг {stats['partition_calls']+1}] Границы: {left}..{right}, Опорный: {pivot}")

   while True:
       while True:
           i += 1
           stats['comparisons'] += 1
           if arr[i] >= pivot:
               break
       while True:
           j -= 1
           stats['comparisons'] += 1
           if arr[j] <= pivot:
               break
       if i >= j:
           if stats['partition_calls'] < 3:
               print(f"Рез-т разбиения: {arr[left:right+1]}, Возврат: {j}")
           stats['partition_calls'] += 1
           return j
       arr[i], arr[j] = arr[j], arr[i]
       stats['swaps'] += 1

def quicksort(arr, left, right, scheme, pivot_type, stats, depth=0):
   stats['max_depth'] = max(stats['max_depth'], depth)
   if left < right:
       if scheme == 'lomuto':
           p = partition_lomuto(arr, left, right, pivot_type, stats)
           quicksort(arr, left, p - 1, scheme, pivot_type, stats, depth + 1)
           quicksort(arr, p + 1, right, scheme, pivot_type, stats, depth + 1)
       else:
           p = partition_hoare(arr, left, right, pivot_type, stats)
           quicksort(arr, left, p, scheme, pivot_type, stats, depth + 1)
           quicksort(arr, p + 1, right, scheme, pivot_type, stats, depth + 1)

stats_hoare_first = {'comparisons': 0, 'swaps': 0, 'partition_calls': 0, 'max_depth': 0}
arr_copy = orders_random.copy()
quicksort(arr_copy, 0, len(arr_copy) - 1, 'hoare', 'first', stats_hoare_first)
print(f"\nХоар (Опорный: первый). Сравнений: {stats_hoare_first['comparisons']}, Макс глубина: {stats_hoare_first['max_depth']}")