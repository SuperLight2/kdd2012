import math


def gcd(x, y):
    while True:
        r = x % y
        if r == 0:
            return y
        x = y
        y = r


def norm(vector):
    result = 0
    for v in vector:
        result += v * v
    return math.sqrt(result)


def cosine(vector1, vector2):
    result = 0
    for i in xrange(len(vector1)):
        result += vector1[i] * vector2[i]
    if abs(result) < 1e-30:
        return 0
    result /= norm(vector1)
    result /= norm(vector2)
    return result


def calc_tf(word, tokens):
    count = 0
    for w in tokens:
        if word == w:
            count += 1
    return 1.0 * count / len(tokens)


def calc_tf_idf(word, tokens, hash2idf):
    if word not in hash2idf:
        return 0
    return calc_tf(word, tokens) * hash2idf[word]
