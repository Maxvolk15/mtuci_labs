import random
import time
import matplotlib.pyplot as plt

#Mod Lin Search Algorithm
def linear_search(arr, target):
    a = arr.copy()
    a.append(target) #Барьерный элемент
    for i in range(len(a)):
        if i == len(a) - 1:
            return -1
        if a[i] == target:
            return i

#Binary Search Algorithm
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
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

#Exponent Search Algorithm
def exponent_search(arr, target):
    n = len(arr)
    if arr[0] == target:
        return 0

    i = 1
    while i < n and arr[i] <= target:
        i *= 2

    left = i // 2
    right = min(i, n - 1)

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

sizes = [10**3, 10**4, 10**5, 10**6]

lin_times = []
bin_times = []
inter_times = []
exp_times = []

for N in sizes:
    arr = list(range(N))
    targets = random.sample(arr, min(500, N))

    start = time.perf_counter()
    for target in targets:
        linear_search(arr, target)
    lin_times.append((time.perf_counter() - start) / len(targets))

    start = time.perf_counter()
    for target in targets:
        binary_search(arr, target)
    bin_times.append((time.perf_counter() - start) / len(targets))

    start = time.perf_counter()
    for target in targets:
        inter_search(arr, target)
    inter_times.append((time.perf_counter() - start) / len(targets))

    start = time.perf_counter()
    for target in targets:
        exponent_search(arr, target)
    exp_times.append((time.perf_counter() - start) / len(targets))


plt.plot(sizes, lin_times, marker='o', label='Linear')
plt.plot(sizes, bin_times, marker='s', label='Binary')
plt.plot(sizes, inter_times, marker='^', label='Interpolation')
plt.plot(sizes, exp_times, marker='d', label='Exponential')
plt.xscale('log')
plt.xlabel("Размер N")
plt.ylabel("Среднее время, сек")
plt.title("Влияние размера массива на поиск")
plt.legend()
plt.grid()

plt.show()