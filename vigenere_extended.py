def decode(text, key):
    key_len = len(key)
    decoded = ""
    for i, c in enumerate(text):
        shift = ((ord(c)-ord(key[i % key_len])) % 256)
        decoded += chr(shift)
    return decoded


def encode(text, key):
    key_len = len(key)
    cipher = ""
    for i, c in enumerate(text):
        shift = ((ord(c)+ord(key[i % key_len])) % 256)
        cipher += chr(shift)
    return cipher
