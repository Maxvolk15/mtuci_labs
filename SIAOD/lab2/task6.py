import random

#1
def memoize(func):
    cache = {}

    def wrap(*args):
        if args in cache:
            return cache[args]

        result = func(*args)
        cache[args] = result
        return result

    return wrap

#2
@memoize
def count_paths(m, n):
    if m <= 0 or n <= 0:
        return 0
    if m == 1 or n == 1:
        return 1
    return count_paths(m - 1, n) + count_paths(m, n - 1)

#3
def random_recursive(n, step=1):
    if step <= 0:
        return n

    k = random.randint(1, 10)
    return random_recursive(n * k, step - 1)

#4
def prime_recursive(n, div=2):
    if n < 2:
        return False
    if div * div > n:
        return True
    if n % div == 0:
        return False
    return prime_recursive(n, div + 1)