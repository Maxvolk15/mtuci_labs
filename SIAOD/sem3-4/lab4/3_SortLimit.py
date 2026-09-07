import time
import random
import matplotlib.pyplot as plt

#Lin Search Algorithm
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

#Binary Search Algorithm
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

N = 100000
arr = [random.randint(1, 10**6) for _ in range(N)]
K = [1, 2, 5, 10, 20, 50, 100, 250, 500, 1000]
lin_times = []
bin_times = []

for k in K:
    targets = [random.choice(arr) for _ in range(k)]

    start_time = time.perf_counter()
    for target in targets:
        linear_search(arr, target)
    lin_times.append(time.perf_counter() - start_time)

    start_time = time.perf_counter()
    sorted_arr = sorted(arr)
    for target in targets:
        binary_search(sorted_arr, target)
    bin_times.append(time.perf_counter() - start_time)

plt.plot(K, lin_times, marker='o', label='Linear total')
plt.plot(K, bin_times, marker='s', label='Sort + Binary total')
plt.xlabel("Число K")
plt.ylabel("Время, сек")
plt.title("Сравнение стратегий поиска")
plt.legend()
plt.grid(True)
plt.show()