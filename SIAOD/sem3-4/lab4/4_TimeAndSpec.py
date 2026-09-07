import random

# Mod Lin Search Algorithm
def linear_search(arr, target):
    a = arr.copy()
    n = len(a)
    a.append(target)
    comparisons = 0 #Сравнения
    iterations = 0  #Итерации
    shifts = 0  #Сдвиги

    for i in range(len(a) - 1):
        iterations += 1
        comparisons += 1

        if i == n:
            return -1, comparisons, iterations, shifts

        if a[i] == target:
            return i, comparisons, iterations, shifts
        shifts += 1


# Binary Search Algorithm
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    comparisons = 0 #Сравнения
    iterations = 0  #Итерации
    shifts = 0  #Сдвиги

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        comparisons += 1
        if arr[mid] == target:
            return mid, comparisons, iterations, shifts

        comparisons += 1
        if arr[mid] < target:
            left = mid + 1
            shifts += 1
        else:
            right = mid - 1
            shifts += 1

    return -1, comparisons, iterations, shifts


# Interpolation Search Algorithm
def inter_search(arr, target):
    low, high = 0, len(arr) - 1

    comparisons = 0 #Сравнения
    iterations = 0  #Итерации
    shifts = 0  #Сдвиги

    while low <= high and target >= arr[low] and target <= arr[high]:
        iterations += 1

        if arr[high] == arr[low]:
            break

        pos = low + ((high - low) * (target - arr[low]) // (arr[high] - arr[low]))

        comparisons += 1
        if arr[pos] == target:
            return pos, comparisons, iterations, shifts

        comparisons += 1
        if arr[pos] < target:
            low = pos + 1
            shifts += 1
        else:
            high = pos - 1
            shifts += 1

    return -1, comparisons, iterations, shifts


# Exponential Search Algorithm
def exponent_search(arr, target):
    n = len(arr)

    comparisons = 0 #Сравнения
    iterations = 0  #Итерации
    shifts = 0  #Сдвиги

    comparisons += 1
    if arr[0] == target:
        return 0, comparisons, iterations, shifts

    i = 1
    while i < n and arr[i] <= target:
        iterations += 1
        comparisons += 1
        i *= 2
        shifts += 1

    left = i // 2
    right = min(i, n - 1)

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        comparisons += 1
        if arr[mid] == target:
            return mid, comparisons, iterations, shifts

        comparisons += 1
        if arr[mid] < target:
            left = mid + 1
            shifts += 1
        else:
            right = mid - 1
            shifts += 1

    return -1, comparisons, iterations, shifts

yes = [random.randint(1, 100) for _ in range(20)]
targets = [random.choice(yes) for _ in range(4)]

functions = [
    ("Linear", linear_search, yes),
    ("Binary", binary_search, sorted(yes)),
    ("Interpolation", inter_search, sorted(yes)),
    ("Exponential", exponent_search, sorted(yes))
]

print(f"Алгоритм{'':5} | Target | Index | Сравнения | Итерации | Сдвиги")

for name, func, arr in functions:
    print("-" * 65)
    for target in targets:
        index, comp, it, sh = func(arr, target)
        print(f"{name:13} | {target:6} | {index:5} | {comp:9} | {it:8} | {sh:6}")