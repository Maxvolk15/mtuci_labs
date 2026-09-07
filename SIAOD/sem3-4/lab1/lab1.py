import time
import random

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

sizes = [1000, 2000, 5000, 10000]
bubble_times = []
sorted_times = []

for n in sizes:
    arr = [random.randint(0, 100000) for _ in range(n)]
    start = time.time()
    bubble_sort(arr.copy())
    bubble_times.append(time.time() - start)
    start = time.time()
    sorted(arr.copy())
    sorted_times.append(time.time() - start)

print(sizes, bubble_times, sorted_times, sep="\n")
