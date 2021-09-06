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


def generate_table(seed: int = 5):
    table = [['' for _ in range(26)] for _ in range(26)]
    random.seed(seed)
    fill_table(table, 0, 0, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return table


def fill_table(table, row, col, left):
    print(f'Row {row} Col {col}')
    attempts = len(left)
    checked = [False for _ in range(len(left))]

    while attempts:
        index = random.randint(0, len(left)-1)
        if not checked[index]:
            if check_row(table, left[index], row, col) and check_column(table, left[index], row, col):
                checked[index] = True
                table[row][col] = left[index]
                if row == 25 and col == 25:
                    return True
                elif col == 25:
                    result = fill_table(table, row+1, 0, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                else:
                    result = fill_table(table, row, col+1, helper.remove_at_index(left, index))

                if result:
                    return True
            attempts -= 1
    return False


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


if __name__ == '__main__':
    table = generate_table(10)
    print(table)