import time
import sys


sys.setrecursionlimit(10000)
file = open("task3_text.txt")
text = file.read()
def cycle_spaces(text) -> int:
    count = 0
    for ch in text:
        if ch == ' ':
            count += 1
    return count

def recurs_spaces(text) -> int:
    if text == "":
        return 0

    first = 1 if text[0] == ' ' else 0
    return first + recurs_spaces(text[1:])

start_time = time.time()
print(f"Cycle: {cycle_spaces(text)}")
print("Cycle time: %s seconds" % (time.time() - start_time))
start_time = time.time()
print(f"Recursive: {recurs_spaces(text)}")
print("Recursive time: %s seconds" % (time.time() - start_time))