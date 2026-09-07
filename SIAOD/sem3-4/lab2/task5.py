import time

def cycle(n, k):
    if k == 0:
        return 1
    else:
        result = 1
        for _ in range(k):
            result *= n
        return result

def recursive(n, k):
    if k == 0:
        return 1
    h = recursive(n, k//2)

    if k % 2 == 0:
        return h * h
    else:
        return h * h * n
    
start_time = time.time()
print(f"Cycle: {cycle(2, 10000)}")
print("Cycle time: %s seconds" % (time.time() - start_time))
start_time = time.time()
print(f"Recursive: {recursive(2, 10000)}")
print("Recursive time: %s seconds" % (time.time() - start_time))