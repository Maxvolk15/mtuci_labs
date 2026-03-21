def count_spaces(text) -> int:
    count = 0
    for ch in text:
        if ch == ' ':
            count += 1
    return count

def count_spaces_rec(text) -> int:
    if text == "":
        return 0

    first = 1 if text[0] == ' ' else 0
    return first + count_spaces_rec(text[1:])