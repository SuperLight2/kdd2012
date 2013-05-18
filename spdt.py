from optparse import OptionParser
from ml_tools.spdt_classification import train_classifier_tree
import math

import logging
_logger = logging.getLogger(__name__)


def multiclass_logloss_metric(original_class, class_probabilities):
    p = 0
    if original_class in class_probabilities:
        p = class_probabilities[original_class]
    p = max(min(p, 1 - 1e-15), 1e-15)
    return -math.log(p)


def right_classification_metric(original_class, class_probabilities):
    original_class_probability = 0
    if original_class in class_probabilities:
        original_class_probability = class_probabilities[original_class]
    for key, value in class_probabilities.iteritems():
        if key != original_class:
            if value > original_class_probability:
                return 0
    return 1


def main():
    optparser = OptionParser(usage="""
        %prog [OPTIONS] features.tsv
        Train decision tree on features pool""")
    optparser.add_option('-t', '--test', dest='test_features',
                         type='string', default=None,
                         help='Use test features to calc')
    opts, args = optparser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    _logger.debug("Begin training")
    decision_tree = train_classifier_tree(args[0])
    _logger.debug("End training")

    if opts.test_features is not None:
        mcll = 0.0
        rc = 0.0
        index = 0
        for line in open(opts.test_features):
            s = line.strip().split('\t')
            original_cls = s[0]
            features = map(float, s[1:])
            #if index < 10:
            #    _logger.debug("original class: " + str(original_cls))
            #    _logger.debug("class probabilities: " + str(decision_tree.calc_mc(features)))
            mcll += multiclass_logloss_metric(original_cls, decision_tree.calc_mc(features))
            rc += right_classification_metric(original_cls, decision_tree.calc_mc(features))
            index += 1
        mcll /= index
        rc /= index
        _logger.debug("Multiclass logloss: " + str(mcll))
        _logger.debug("Right classification ratio:" + str(rc))


if __name__ == '__main__':
    main()
