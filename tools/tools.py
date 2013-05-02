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