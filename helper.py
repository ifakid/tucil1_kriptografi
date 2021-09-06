def split_n(text, n):
    split_text = []
    for i in range(0, len(text), n):
        split_text.append(text[i:i + n])
    return split_text


def preprocessing(text: str):
    processed = ''.join(e.upper() for e in text if e.isalpha())
    return processed


def mod_inverse(a, mod):
    m0 = mod
    y = 0
    x = 1
    while a > 1:
        q = a // mod
        t = mod
        mod = a % mod
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x = x + m0
    return x


def gcd(p, q):
    while q != 0:
        p, q = q, p % q
    return p


def is_coprime(x, y):
    return gcd(x, y) == 1


def remove_at_index(arr, index):
    return arr[:index] + arr[index+1:]
