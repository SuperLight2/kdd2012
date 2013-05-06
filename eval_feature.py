from optparse import OptionParser
from tools.readers import SmartReader
from tools.smart_writer import SmartWriter
from tools.score import ScoreCalcer
import os
import random


def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] features.tsv[.gz]
            Evaluate features score on features.tsv[.gz] pool""")
    optparser.add_option('-f', '--feature', dest='feature_to_test',
                         type='int', default=None,
                         help='Feature index (0-based) to test score')
    optparser.add_option('--folds', dest='folds',
                             type='int', default=200,
                             help='Number of folds to test')
    optparser.add_option('--fold-size', dest='fold_size',
                             type='int', default=10000,
                             help='Each fold (learn) size in percents of original')
    optparser.add_option('--training script', dest='training_script',
                             type='string', default='learn_and_predict_default.sh',
                             help='Script to learn on pool and predict')
    opts, args = optparser.parse_args()

    result_filepath = "eval.feature.output.tsv"
    tmp_learn_filepath = "eval.learn.%d.tsv" % os.getpid()
    tmp_test_filepath = "eval.test.%d.tsv" % os.getpid()
    tmp_result_filepath = "eval.result.%d.tsv" % os.getpid()

    with open(result_filepath, 'w') as result_file:
        tmp_learn_file = SmartWriter().open(tmp_learn_filepath)
        tmp_test_file = SmartWriter().open(tmp_test_filepath)

        for iteration in xrange(opts.folds):
            for line in SmartReader().open(args[0]):
                if random.randint(0, 99) <= opts.fold_size:
                    print >> tmp_learn_file, line.strip()
                else:
                    print >> tmp_test_file, line.strip()
        tmp_learn_file.close()
        tmp_test_file.close()
        os.system('%s %s %s > %s' % (opts.training_script, tmp_learn_filepath, tmp_test_filepath, tmp_result_filepath))
        x1 = ScoreCalcer(tmp_test_filepath, tmp_result_filepath, delimiter='\t').score_AUC()
        os.system('%s -i %d %s %s > %s' % (opts.training_script, opts.feature, tmp_learn_filepath, tmp_test_filepath, tmp_result_filepath))
        x2 = ScoreCalcer(tmp_test_filepath, tmp_result_filepath, delimiter='\t').score_AUC()



if __name__ == '__main__':
    main()