from optparse import OptionParser
from tools.score import ScoreCalcer


def main():
    optparser = OptionParser(usage="""
    %prog [OPTIONS] SOLUTION_FILE SUBMISSION_FILE""")
    optparser.add_option('-f', '--filter', dest='filter',
                         type='string', default=None,
                         help='Calc only on public or private data')
    optparser.add_option('-d', '--delimiter', dest='delimiter',
                         type='string', default=',',
                         help='File columns delimiter')
    opts, args = optparser.parse_args()

    score_calcer = ScoreCalcer(args[0], args[1], opts.filter, opts.delimiter)
    print("AUC  : %f" % score_calcer.score_AUC())
    print("NWMAE: %f" % score_calcer.score_NWMAE())
    print("WRMSE: %f" % score_calcer.score_WRMSE())

if __name__ == "__main__":
    main()
