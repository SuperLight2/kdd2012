from optparse import OptionParser


def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] features.tsv[.gz]
            Evaluate features score """)
    optparser.add_option('-f', '--feature', dest='feature_to_test',
                         type='int', default=None,
                         help='Feature index (0-based) to test score')
    opts, args = optparser.parse_args()

if __name__ == '__main__':
    main()