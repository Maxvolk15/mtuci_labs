#Mod Lin Search Algorithm
def linear_search(arr, target):
    a = arr.copy()
    a.append(target) #Барьерный элемент
    i=0
    while i != len(a):
        if i == len(a) - 1:
            return -1
        if a[i] == target:
            return i
        i+=1

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

yes = [6, 4, 2, 6, 15, 1, 9, 12, 20, 2, 18, 10]

targets = [6, 15, 21]
functions = [binary_search, inter_search, exponent_search]


print("Linear Search:")
for target in targets:
    print(f"Target: {target}, Index: {linear_search(yes, target)}")

for func in functions:
    print("-" * 50)
    print("Func: " + func.__name__)
    for target in targets:
        print(f"Target: {target}, Index: {func(sorted(yes), target)}")