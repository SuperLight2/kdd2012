from tools.tools import gcd

def GCD(A, B):
    while True:
        r = A.x % B.x
        if r == 0:
            return B.x
        A.x = B.x
        B.x = r


class C():
    X = list([1, 2, 3])
    X.append(4)



def main():
    C.X[2] = 11
    print C.X
    d = dict()
    d[(0, 1)] = 1
    d[(1, 1)] = 2
    d[(1, 1)] += 2
    print d


if __name__ == '__main__':
    main()
