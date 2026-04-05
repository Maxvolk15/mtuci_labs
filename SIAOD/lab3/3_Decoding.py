a="QWJXNTZLPMRAVKSDHUEYCIFOGBQRWPELKJHGFDSAMNBVCXZQWERTYUIOPLKJHGFDSAZXCVBNMQWERTYUIOPASDFGHJKLZXCVBNMTRXQPLMNSHADOWPROTOCOLDELTASEVENXK91REDNODEALPHAOMEGASIGMATRACEVECTORCYBERLATTICEPHANTOMKEYMIRRORCHAINQUANTUMDRIFTHELIXSIGNALCRYPTONOVAARCGRIDZETAFRAMEDELTAFORGESTELLARCODEXIONPATHWAYNEXUSLOCKSEQUENCEPRIMEGLYPHAXIOMLAYEROBSIDIANLINKVORTEXCHANNELSPECTRALCOREMATRIXFUSIONTHREADKRYPTOSPHEREZLQMWNXPTRAKVSHDUEYFICOGBLRAPQMTNZXCVWQPOIUYTREWQLKJHGFDSAMNBVCXZQWERT"
b="MNBVCXZLKJHGFDSAPOIUYTREWQZXCVBNMASDFGHJKLQWERTYUIOPMNBVCXZLKJHGFDSAQWERTYUIOPZXCVBNMLKJHGFDSAPROTOCOLSHADOWDELTASEVENXK91REDNODEALPHAOMEGASIGMATRACEVECTORCYBERLATTICEPHANTOMKEYMIRRORCHAINQUANTUMDRIFTHELIXSIGNALCRYPTONOVAARCGRIDZETAFRAMEDELTAFORGESTELLARCODEXIONPATHWAYNEXUSLOCKSEQUENCEPRIMEGLYPHAXIOMLAYEROBSIDIANLINKVORTEXCHANNELSPECTRALCOREMATRIXFUSIONTHREADKRYPTOSPHEREPLKMIJNUHBYGVTFCRDXESZWAQOMNPLKJIHGFEDCBAVTREWQLZXCVBNMASDFGHJKQWERTYUIOPLKJHG"

def lcs(a, b):
    n = len(a)
    m = len(b)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    i = n
    j = m
    result = []

    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    result.reverse()
    return dp[n][m], "".join(result), dp

length, sequence, table = lcs(a, b)

print("Длина LCS:", length)
print("Одна из найденных подпоследовательностей:")
print(sequence)
print("Размер таблицы:", len(table), "x", len(table[0]))

print("Фрагмент таблицы 20x20:")
print(" ","  ".join(b[:20]))
for row in table[:20]:
    print(a[table.index(row)], "  ".join(str(x) for x in row[:20]))