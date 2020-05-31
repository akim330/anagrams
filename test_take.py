from collections import Counter

def superset(word1, word2, strict=False):
    # Can word 1 take word 2?
    word1_counter = Counter(word1)
    word2_counter = Counter(word2)

    if strict:
        return (word1_counter - word2_counter and not (word2_counter - word1_counter))
    else:
        return (word1_counter - word2_counter and not (word2_counter - word1_counter)) or (
                    not (word1_counter - word2_counter) and not (word2_counter - word1_counter))

def subtract(word1, word2):
    # Subtract word2 from word1 (e.g. 'test' - 'tst' = 'e')

    list1 = list(word1)
    for letter in word2:
        try:
            list1.remove(letter)
        except ValueError:
            pass

    # Turn list into string
    str = ''
    str = str.join(list1)

    return str
