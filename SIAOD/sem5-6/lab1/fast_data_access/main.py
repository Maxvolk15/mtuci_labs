import time

second_list = list(range(1, 100001))

def linear_serach(numbers, target):
    for ind, val in enumerate(numbers):
        if val == target:
            return ind

    return -1
        
#----------------- Test -------------------
print(f"Index_first: {second_list[0]}. Index_half: {second_list[49999]}. Index_last: {second_list[99999]}")
start = time.perf_counter()
print(f"Lin_first: {linear_serach(second_list, 1)}. Lin_half: {linear_serach(second_list, 50000)}. Lin_last: {linear_serach(second_list, 100000)}. Lin_null: {linear_serach(second_list, 100001)}")
start = time.perf_counter()
print(f"Index_rand_num: {second_list[99997]}. Time: {time.perf_counter() - start}")
start = time.perf_counter()
print(f"Lin_rand_index: {linear_serach(second_list, 99998)}. Time: {time.perf_counter() - start}")
start = time.perf_counter()
print(f"Index_rand_num: {second_list[55000]}. Time: {time.perf_counter() - start}")
start = time.perf_counter()
print(f"Lin_rand_index: {linear_serach(second_list, 55001)}. Time: {time.perf_counter() - start}")