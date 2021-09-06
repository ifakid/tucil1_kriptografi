def preprocessing(text: str):
    processed = ''.join(e.upper() for e in text if e.isalpha())
    return processed


def process_key(key):
    key = preprocessing(key)
    key = key.upper().replace(" ", "").replace("J", "I")
    seen = [False for _ in range(26)]
    seen[9] = True  # Letter J
    table = ""
    filled = 0

    for c in key:
        if not seen[ord(c) - ord('A')]:
            seen[ord(c) - ord('A')] = True
            table += c
            filled += 1
    if filled != 25:
        for i, a in enumerate(seen):
            if not a:  # Not seen yet
                table += chr(ord('A')+i)
    split_text = []
    for i in range(0, 25, 5):
        split_text.append([c for c in table[i:i+5]])
    return split_text


def process_text(text):
    text = preprocessing(text)
    text = text.upper().replace(" ", "").replace('J', 'I')
    seen = [False for _ in range(26)]
    seen[9] = True  # Letter J

    split_text = []
    for i in range(0, len(text), 2):
        if i+1 >= len(text) or text[i] == text[i+1]:
            text = insert_at_index(text, i+1, 'X')
        split_text.append(text[i]+text[i+1])
    return split_text


def insert_at_index(string, index, char):
    return string[:index]+char+string[index:]


def find_letter(letter, table):
    for i in range(5):  # Row
        for j in range(5):  # Column
            if table[i][j] == letter:
                return i, j


def encode(text, key):
    table = process_key(key)
    message = process_text(text)

    cipher = []
    for pair in message:
        first = find_letter(pair[0], table)
        second = find_letter(pair[1], table)

        if first[0] == second[0]:  # Same row
            first_key = table[first[0]][(first[1]+1) % 5]
            second_key = table[second[0]][(second[1]+1) % 5]
        elif first[1] == second[1]:  # Same column
            first_key = table[(first[0]+1) % 5][first[1]]
            second_key = table[(second[0]+1) % 5][second[1]]
        else:
            first_key = table[first[0]][second[1]]
            second_key = table[second[0]][first[1]]
        cipher.append(first_key + second_key)

    cipher = ''.join(cipher)
    split_text = []
    for i in range(0, len(cipher), 5):
        split_text.append(cipher[i:i + 5])
    return ' '.join(split_text)


def decode(text, key):
    table = process_key(key)
    message = process_text(text)

    cipher = []
    for pair in message:
        first = find_letter(pair[0], table)
        second = find_letter(pair[1], table)

        if first[0] == second[0]:  # Same row
            first_key = table[first[0]][(first[1]-1) % 5]
            second_key = table[second[0]][(second[1]-1) % 5]
        elif first[1] == second[1]:  # Same column
            first_key = table[(first[0]-1) % 5][first[1]]
            second_key = table[(second[0]-1) % 5][second[1]]
        else:
            first_key = table[first[0]][second[1]]
            second_key = table[second[0]][first[1]]
        cipher.append(first_key + second_key)

    cipher = ''.join(cipher)
    split_text = []
    for i in range(0, len(cipher), 5):
        split_text.append(cipher[i:i + 5])
    return ' '.join(split_text)

