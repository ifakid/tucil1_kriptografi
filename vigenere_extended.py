def decode(text, key, file=False):
    key_len = len(key)
    if file:
        decoded = b''
    else:
        decoded = ""
    for i, c in enumerate(text):
        if file:
            shift = ((c-ord(key[i % key_len])) % 256)
            decoded += bytes([shift])
        else:
            shift = ((ord(c)-ord(key[i % key_len])) % 256)
            decoded += chr(shift)
    return decoded


def encode(text, key, file=False):
    key_len = len(key)
    if file:
        cipher = b''
    else:
        cipher = ""
    for i, c in enumerate(text):
        if file:
            shift = ((c+ord(key[i % key_len])) % 256)
            cipher += bytes([shift])
        else:
            shift = ((ord(c)+ord(key[i % key_len])) % 256)
            cipher += chr(shift)
    print(cipher)
    return cipher
