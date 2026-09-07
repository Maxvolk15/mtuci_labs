import time
import sys

sys.setrecursionlimit(10000)
def cycle(n):
    if n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n+1):
            result *= i
        return result

def recursive(n):
    if n == 0:
        return 1
    else:
        return n * recursive(n-1)

start_time = time.time()
print(f"Cycle: {cycle(1000)}")
print("Cycle time: %s seconds" % (time.time() - start_time))
start_time = time.time()
print(f"Recursive: {recursive(1000)}")
print("Recursive time: %s seconds" % (time.time() - start_time))