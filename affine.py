import helper


def encode(text, key: int, shift: int):
    text = helper.preprocessing(text)
    cipher = ""
    for c in text:
        i = ord(c) - ord('A')  # Index
        cipher += chr((key * i + shift) % 26 + ord('A'))
    return ' '.join(helper.split_n(cipher, 5))


def decode(text, key: int, shift: int):
    text = helper.preprocessing(text)
    inverse = helper.mod_inverse(key, 26)
    decoded = ""
    for c in text:
        y = ord(c) - ord('A')
        decoded += chr(((y - shift) * inverse % 26) + ord('A'))
    return ' '.join(helper.split_n(decoded, 5))
