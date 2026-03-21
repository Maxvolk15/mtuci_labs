import random


def memoize(func):
    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]

        result = func(*args)
        cache[args] = result
        return result

    return wrapper


@memoize
def count_paths(m, n):
    if m <= 0 or n <= 0:
        return 0
    if m == 1 or n == 1:
        return 1
    return count_paths(m - 1, n) + count_paths(m, n - 1)


def random_recursive(n, steps=1):
    if steps <= 0:
        return n

    k = random.randint(1, 10)
    return random_recursive(n * k, steps - 1)


def prime_recursive(n, div=2):
    if n < 2:
        return False
    if div * div > n:
        return True
    if n % div == 0:
        return False
    return prime_recursive(n, div + 1)