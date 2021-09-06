import helper


def decode(text, key):
    key = key.upper()
    processed = helper.preprocessing(text)
    key_len = len(key)
    decoded = ""
    for i, c in enumerate(processed):
        if i >= key_len:
            shift = ((ord(c)-ord(decoded[i-key_len])) % 26)+ord('A')
        else:
            shift = ((ord(c)-ord(key[i])) % 26)+ord('A')
        decoded += chr(shift)
    return ' '.join(helper.split_n(decoded, 5))


def encode(text, key):
    key = key.upper()
    processed = helper.preprocessing(text)
    if len(key) < len(processed):
        key += processed
    print(key)

    cipher = ""
    for i, c in enumerate(processed):
        shift = ((ord(c)+ord(key[i])-(ord('A')*2)) % 26)+ord('A')
        cipher += chr(shift)

    return ' '.join(helper.split_n(cipher, 5))