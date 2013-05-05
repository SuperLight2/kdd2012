import sys
import math


def main():
    x1 = []
    x2 = []
    for line in sys.stdin:
        s = map(float, line.strip().split())
        if abs(s[0] - s[1]) < 1e-7:
            continue
        x1.append(s[0])
        x2.append(s[1])
    Nr = len(x1)
    delta = sorted([(abs(x2[i] - x1[i]), i) for i in xrange(Nr)], key=lambda x: (-x[0], x[1]))
    W = 0
    for rank in xrange(Nr):
        original_x1 = x1[delta[rank][1]]
        original_x2 = x2[delta[rank][1]]
        sign = 1
        if original_x1 > original_x2:
            sign = -1
        W += sign * (rank + 1)
    delta_W = math.sqrt(1.0 * Nr * (Nr + 1) * (2 * Nr + 1) / 6)
    z = (abs(W) - 0.5) / delta_W
    z_critical = 1.645
    print "Nr:", Nr, " (it should be more than 10)"
    print "W:", W
    print "z:", z
    print "z_critical:", z_critical
    if z < z_critical:
        print "Result: Unknown"
    else:
        if W > 0:
            print "Result: Feature RULES"
        else:
            print "Result: Feature SUCKS"


if __name__ == '__main__':
    main()
