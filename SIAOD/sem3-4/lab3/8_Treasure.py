import ast

capacities = [10, 14, 18]


def load_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read().strip()


    var_name, data_part = text.split("=", 1)
    var_name = var_name.strip()
    data_part = data_part.strip()


    items = ast.literal_eval(data_part)
    return items


def three_bags(items, capacities):
    c1, c2, c3 = capacities
    n = len(items)

    dp = {}
    choice = {}

    def put_items(i, cap1, cap2, cap3):
        if i == n:
            return 0

        state = (i, cap1, cap2, cap3)
        if state in dp:
            return dp[state]

        name, weight, value = items[i]

        best_value = put_items(i + 1, cap1, cap2, cap3)
        best_choice = 0

        if weight <= cap1:
            candidate = value + put_items(i + 1, cap1 - weight, cap2, cap3)
            if candidate > best_value:
                best_value = candidate
                best_choice = 1

        if weight <= cap2:
            candidate = value + put_items(i + 1, cap1, cap2 - weight, cap3)
            if candidate > best_value:
                best_value = candidate
                best_choice = 2

        if weight <= cap3:
            candidate = value + put_items(i + 1, cap1, cap2, cap3 - weight)
            if candidate > best_value:
                best_value = candidate
                best_choice = 3

        dp[state] = best_value
        choice[state] = best_choice
        return best_value

    max_total_value = put_items(0, c1, c2, c3)

    bag1 = []
    bag2 = []
    bag3 = []

    i = 0
    cap1, cap2, cap3 = c1, c2, c3

    while i < n:
        state = (i, cap1, cap2, cap3)
        action = choice.get(state, 0)

        name, weight, value = items[i]

        if action == 1:
            bag1.append(items[i])
            cap1 -= weight
        elif action == 2:
            bag2.append(items[i])
            cap2 -= weight
        elif action == 3:
            bag3.append(items[i])
            cap3 -= weight

        i += 1

    return max_total_value, bag1, bag2, bag3


def print_bag(bag_name, bag, capacity):
    print(bag_name)
    print("Вместимость:", capacity)
    print("Итоговый вес:", sum(item[1] for item in bag))
    print("Итоговая стоимость:", sum(item[2] for item in bag))
    print("Предметы:")

    for name, weight, value in bag:
        print(f"Название: {name}, вес: {weight}, стоимость: {value}")

    print()


items = load_from_file("treasures.txt")

max_total_value, petya_bag, vasya_bag, terentiy_bag = three_bags(items, capacities)

print("Максимальная суммарная стоимость:", max_total_value)
print()

print_bag("Рюкзак Пети", petya_bag, capacities[0])
print_bag("Рюкзак Васи", vasya_bag, capacities[1])
print_bag("Рюкзак Терентия", terentiy_bag, capacities[2])