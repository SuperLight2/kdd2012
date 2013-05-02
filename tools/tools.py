
def gcd(x, y):
    while True:
        r = x % y
        if r == 0:
            return y
        x = y
        y = r
