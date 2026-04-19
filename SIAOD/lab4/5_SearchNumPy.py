import random
import time
import numpy as np

#Lin Search Algorithm
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

N = 100000
arr = [random.randint(1, 10**4) for _ in range(N)]
targets = [random.choice(arr) for _ in range(1000)]


np_arr = np.array(sorted(arr))

start = time.perf_counter()
for target in targets:
    linear_search(arr, target)
time_custom = time.perf_counter() - start

start = time.perf_counter()
for target in targets:
    target in arr
time_in = time.perf_counter() - start

start = time.perf_counter()
for target in targets:
    arr.index(target)
time_index = time.perf_counter() - start

start = time.perf_counter()
for target in targets:
    pos = np.searchsorted(np_arr, target)
    if pos < len(np_arr) and np_arr[pos] == target:
        pass
time_numpy = time.perf_counter() - start

print("Собственная реализация:", time_custom)
print("Оператор in:", time_in)
print("Метод index():", time_index)
print("numpy.searchsorted():", time_numpy)