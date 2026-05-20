import time
from DynamicList_1 import DynamicArray
from LinkedList_2 import LinkedList

def benchmark():
   sizes = [10**2, 10**3, 10**4]
   
   print("--- Сравнение времени (в секундах) ---")
   for N in sizes:
       print(f"\nРазмер данных N = {N}")
       
       arr = DynamicArray()
       ll = LinkedList()
       for i in range(N):
           arr.append(i)
           ll.add_first(i)
           
       start = time.time()
       arr.append(999)
       time_arr_append = time.time() - start
       
       start = time.time()
       ll.add_last(999)
       time_ll_append = time.time() - start
       
       mid_index = N // 2
       start = time.time()
       arr.get_by_index(mid_index)
       time_arr_get = time.time() - start
       
       start = time.time()
       ll.get_by_index(mid_index)
       time_ll_get = time.time() - start
       
       print(f"Добавление в конец: Массив {time_arr_append:.7f} | Связанный список {time_ll_append:.7f}")
       print(f"Доступ по индексу:  Массив {time_arr_get:.7f} | Связанный список {time_ll_get:.7f}")