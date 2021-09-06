import random
import helper


def decode(text, key, seed):
    key = key.upper()
    processed = helper.preprocessing(text)
    key_len = len(key)
    table = generate_table(seed)
    decoded = ""
    for i, c in enumerate(processed):
        # Find by shift
        decoded += find_by_shift(table, c, key[i % key_len])
    return ' '.join(helper.split_n(decoded, 5))


def encode(text, key, seed):
    key = key.upper()
    processed = helper.preprocessing(text)
    key_len = len(key)
    table = generate_table(seed)
    decoded = ""
    for i, c in enumerate(processed):
        letter = ord(c) - ord('A')
        shift = ord(key[i % key_len]) - ord('A')
        decoded += table[letter][shift]
    return ' '.join(helper.split_n(decoded, 5))


def generate_table(seed):
    table = [['' for _ in range(26)] for _ in range(26)]
    random.seed(seed)
    row = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    random.shuffle(row)
    table[0] = row
    for i in range(1, 26):
        for j in range(26):
            table[i][j] = row[(i+j) % 26]
    return table


def find_by_shift(table, letter, key):
    key_idx = ord(key) - ord('A')
    for i in range(26):
        if table[i][key_idx] == letter:
            return chr(ord('A') + i)