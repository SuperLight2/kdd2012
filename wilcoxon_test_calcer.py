import sys
from tools.score import WilcoxonTest


def main():
    x1 = []
    x2 = []
    for line in sys.stdin:
        s = map(float, line.strip().split())
        x1.append(s[0])
        x2.append(s[1])
    w_tester = WilcoxonTest(x1, x2)
    print "Nr:", w_tester.get_N(), " (it should be more than 10)"
    print "W:", w_tester.get_W()
    print "Result: ", w_tester.get_result()

if __name__ == '__main__':
    main()
