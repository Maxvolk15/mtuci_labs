import math
import re


REVIEWS = {
    0: "Быстрая доставка и удобное приложение. Доставка без задержек.",
    1: "Доставка задержалась, но поддержка помогла.",
    2: "Удобное приложение и быстрый поиск товаров.",
    3: "Плохая поддержка и медленная доставка.",
    4: "Отличное качество товара, быстрая доставка.",
    5: "Удобный интерфейс, но поиск работает медленно.",
    6: "Быстрая доставка, хороший сервис и поддержка.",
    7: "Поиск товаров удобный, качество отличное.",
    8: "Поддержка быстро решила проблему с заказом.",
    9: "Доставка быстрая, но качество упаковки плохое.",
}


def tokenize(text):
    return re.findall(r"[а-яёa-z0-9]+", text.lower())


# 1. ---------------------------------------------------------------------

def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0 or n < m:
        return []

    matches = []
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            matches.append(i)
    return matches


def prefix_function(pattern):
    m = len(pattern)
    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    return pi


def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0 or n < m:
        return []

    pi = prefix_function(pattern)
    matches = []
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            matches.append(i - m + 1)
            j = pi[j - 1]
    return matches


# 2. ---------------------------------------------------------------------

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

    def suggest(self, prefix, max_count=5):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]

        results = []

        def dfs(curr, path):
            if len(results) >= max_count:
                return
            if curr.is_end:
                results.append(path)
            for ch in sorted(curr.children.keys()):
                dfs(curr.children[ch], path + ch)
                if len(results) >= max_count:
                    return

        dfs(node, prefix)
        return results


# 3. ---------------------------------------------------------------------

def build_index(reviews):
    index = {}
    for doc_id, text in reviews.items():
        tokens = tokenize(text)
        for pos, word in enumerate(tokens):
            if word not in index:
                index[word] = {}
            if doc_id not in index[word]:
                index[word][doc_id] = []
            index[word][doc_id].append(pos)
    return index


def boolean_and_search(index, query):
    tokens = tokenize(query)
    if not tokens:
        return []
    if tokens[0] not in index:
        return []
    doc_ids = set(index[tokens[0]].keys())
    for token in tokens[1:]:
        if token not in index:
            return []
        doc_ids &= set(index[token].keys())
    return sorted(list(doc_ids))


def phrase_search(index, query):
    tokens = tokenize(query)
    if not tokens:
        return []
    for token in tokens:
        if token not in index:
            return []

    candidate_docs = set(index[tokens[0]].keys())
    for token in tokens[1:]:
        candidate_docs &= set(index[token].keys())

    result = []
    for doc_id in sorted(candidate_docs):
        first_positions = index[tokens[0]][doc_id]
        for start_pos in first_positions:
            if all((start_pos + i) in index[tokens[i]][doc_id] for i in range(1, len(tokens))):
                result.append(doc_id)
                break
    return result


# 4. ---------------------------------------------------------------------

def compute_idf(term, index, total_docs):
    df_t = len(index.get(term, {}))
    return math.log((total_docs + 1) / (df_t + 1)) + 1.0


def score(d, q, index, total_docs):
    tokens = tokenize(q)
    total_score = 0.0
    for t in tokens:
        tf_t_d = len(index.get(t, {}).get(d, []))
        idf_t = compute_idf(t, index, total_docs)
        total_score += tf_t_d * idf_t
    return total_score

# Т ---------------------------------------------------------------------

def main():
    print("-" * 70)
    print("Задание 1")
    print("-" * 70)
    test_text = "абабаба"
    test_pattern = "аба"
    res_naive = naive_search(test_text, test_pattern)
    res_kmp = kmp_search(test_text, test_pattern)
    print(f"Тест на строках '{test_text}' и '{test_pattern}':")
    print(f"naive_search: {res_naive}")
    print(f"kmp_search:   {res_kmp}")

    search_word = "доставка"
    print(f"\nПоиск слова '{search_word}' в отзывах:")
    f = True
    for doc_id, text in REVIEWS.items():
        text_lower = text.lower()
        n_pos = naive_search(text_lower, search_word)
        k_pos = kmp_search(text_lower, search_word)
        if n_pos != k_pos:
            f = False
        print(f"Отзыв {doc_id}: позиции {k_pos}")
    print(f"Данные сошлись? {f}")

# -----------------------------------------------------------------------------------------------------

    print("\n" + "-" * 70)
    print("Задание 2")
    print("-" * 70)
    unique_words = set()
    for text in REVIEWS.values():
        unique_words.update(tokenize(text))
    print(f"Количество уникальных слов в отзывах: {len(unique_words)}")

    trie = Trie()
    for word in unique_words:
        trie.insert(word)

    print(f"Поиск по 'доставка': {trie.search('доставка')}")
    print(f"Поиск по 'достав': {trie.search('достав')}")
    print(f"Поиск по 'дост': {trie.starts_with('дост')}")

    print(f"suggest('дост'): {trie.suggest('дост')}")
    print(f"suggest('п'):    {trie.suggest('п')}")

# -----------------------------------------------------------------------------------------------------

    print("\n" + "-" * 70)
    print("Задание 3")
    print("-" * 70)
    index = build_index(REVIEWS)

    and_query = "доставка поддержка"
    and_docs = boolean_and_search(index, and_query)
    print(f"Поиск (AND) по запросу '{and_query}': {and_docs}")

    phrase_1 = "быстрая доставка"
    res_1 = phrase_search(index, phrase_1)
    print(f"Фразовый поиск '{phrase_1}': {res_1}")

    phrase_2 = "поиск товаров"
    res_2 = phrase_search(index, phrase_2)
    print(f"Фразовый поиск '{phrase_2}': {res_2}")

# -----------------------------------------------------------------------------------------------------

    print("\n" + "-" * 70)
    print("Задание 4")
    print("-" * 70)
    query = "быстрая доставка"
    n_docs = len(REVIEWS)

    scored_docs = []
    for doc_id in REVIEWS:
        s = score(doc_id, query, index, n_docs)
        scored_docs.append((doc_id, s))

    scored_docs.sort(key=lambda x: (-x[1], x[0]))

    print(f"Топ-3 наиболее релевантных отзыва для запроса '{query}':")
    for doc_id, sc in scored_docs[:3]:
        print(f"  ID {doc_id} | Оценка: {sc:.4f} | Текст: {REVIEWS[doc_id]}")


if __name__ == "__main__":
    main()
