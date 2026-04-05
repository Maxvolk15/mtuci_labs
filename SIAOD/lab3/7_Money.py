coins1 = [1, 5, 10, 25, 50, 100]
coins2 = [1, 4, 6, 9]
amounts = [23, 37, 58, 74, 99, 123]

def greedy_change(coins, amount):
    result = []
    for coin in sorted(coins, reverse=True):
        while amount >= coin:
            amount -= coin
            result.append(coin)
    if amount != 0:
        return None
    return result

def dp_change(coins, amount):
    INF = 10**9
    dp = [INF] * (amount + 1)
    prev = [-1] * (amount + 1)
    dp[0] = 0

    for s in range(1, amount + 1):
        for coin in coins:
            if s >= coin and dp[s - coin] + 1 < dp[s]:
                dp[s] = dp[s - coin] + 1
                prev[s] = coin

    if dp[amount] == INF:
        return None

    result = []
    cur = amount
    while cur > 0:
        coin = prev[cur]
        result.append(coin)
        cur -= coin

    return result

def analyze_system(coins, amounts):
    print("Набор номиналов:", coins)
    for amount in amounts:
        greedy_result = greedy_change(coins, amount)
        dp_result = dp_change(coins, amount)

        print(f"{amount}: Жадный: {greedy_result} = {len(greedy_result)} | Динамический: {dp_result} = {len(dp_result)} | Совпали ли результаты: {len(greedy_result) == len(dp_result)}")

analyze_system(coins1, amounts)
print("-" * 100)
analyze_system(coins2, amounts)