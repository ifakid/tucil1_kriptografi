# TODO

import random
import helper


def decode(text, key, seed):
    key = key.upper()
    processed = helper.preprocessing(text)
    key_len = len(key)
    decoded = ""
    for i, c in enumerate(processed):
        shift = ord(key[i % key_len]) - ord('A')
        # Find by shift
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


# TODO: Do it with backtracking
def generate_table(seed: int):
    table = [['' for _ in range(26)] for _ in range(26)]
    random.seed(seed)
    fill_table(table, 0, 0, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return table


def fill_table(table, row, col, left):
    tried = left
    for _ in range(len(tried)):
        index = random.randint(0, len(tried)-1)



def check_row(table, letter, row, col):
    for i in range(col):
        if table[row][i] == letter:
            return False
    return True


def check_column(table, letter, row, col):
    for i in range(row):
        if table[i][col] == letter:
            return False
    return True
