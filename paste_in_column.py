#!/usr/bin/env python

import sys

def main():
    file2 = open(sys.argv[1])
    for line in sys.stdin:
        s = line.strip().split('\t')
        line = file2.readline().strip()
        print "\t".join([s[0], line] + s[1:])

if __name__ == '__main__':
    main()
