import helper


def preprocessing(text: str):
    processed = ''.join(e.upper() for e in text if e.isalpha())
    return processed


def decode(text):
    f = open('running_key.txt', 'r')
    key = preprocessing(f.read(len(text)*2))
    processed = preprocessing(text)
    key_len = len(key)
    decoded = ""
    for i, c in enumerate(processed):
        shift = ((ord(c)-ord(key[i % key_len])) % 26)+ord('A')
        decoded += chr(shift)
    return ' '.join(helper.split_n(decoded, 5))


def encode(text):
    f = open('running_key.txt', 'r')
    key = preprocessing(f.read(len(text) * 2))
    processed = preprocessing(text)
    key_len = len(key)
    cipher = ""
    for i, c in enumerate(processed):
        shift = ((ord(c)+ord(key[i % key_len])-(ord('A')*2)) % 26)+ord('A')
        cipher += chr(shift)
    return ' '.join(helper.split_n(cipher, 5))
