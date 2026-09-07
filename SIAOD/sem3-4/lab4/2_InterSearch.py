import time
import random
import matplotlib.pyplot as plt

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

#Inter Search Algorithm
def inter_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high and target >= arr[low] and target <= arr[high]:
        if low == high:
            if arr[low] == target:
                return low
            return -1
        pos = low + ((high - low) * (target - arr[low]) // (arr[high] - arr[low]))
        if pos < low or pos > high:
            return -1
        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1

n = 100000
default = list(range(n))
quadratic = [i**2 for i in range(n)]
exponent = [2**(i//1000) + i for i in range(n)]
arr = sorted([random.randint(0, 10**6) for _ in range(n)])
random_arr = sorted([i**4 if random.random() < 0.3 else i for i in arr])

arrs = [default, quadratic, exponent, random_arr]
names = ["Равномерный", "Квадратичный", "Экспоненциальный", "Случайный"]

bin_times = []
inter_times = []

for arr in arrs:
    yes = random.sample(arr, 100)
    start_time = time.perf_counter()
    for i in yes:
        inter_search(arr, i)
    inter_times.append(time.perf_counter() - start_time)

    start_time = time.perf_counter()
    for i in yes:
        binary_search(arr, i)
    bin_times.append(time.perf_counter() - start_time)

plt.plot(names, inter_times, marker='o', label='Interpolation')
plt.plot(names, bin_times, marker='s', label='Binary')
plt.yscale('log')
plt.title("Зависимость поиска от распределения")
plt.ylabel("Время (сек)")
plt.legend()
plt.grid()

plt.show()