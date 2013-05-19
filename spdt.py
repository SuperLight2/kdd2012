from optparse import OptionParser
from ml_tools.spdt_classification import SimpleClassifier, SPDTClassifier
from tools.readers import SmartReader
from ml_tools.metrics import RightClassificationRatio, MulticlassLogloss, MSE, AUC

import logging
_logger = logging.getLogger(__name__)


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
    #classifier_tree = SimpleClassifier().learn(args[0])
    classifier_tree = SPDTClassifier().learn(args[0])
    _logger.debug("End training")

    mce_metric = MSE()
    right_classification_ratio_metric = RightClassificationRatio()
    mcll_metric = MulticlassLogloss()
    auc_metric = AUC()

    if opts.test_features is not None:
        index = 0
        for line in SmartReader().open(opts.test_features):
            s = line.strip().split('\t')
            original_cls = s[0]
            features = map(float, s[1:])
            class_probabilities = classifier_tree.calc_mc(features)

            #if index < 10:
            #    _logger.debug("original class: " + str(original_cls))
            #    _logger.debug("class probabilities: " + str(class_probabilities))
            result = 0
            try:
                for key, value in class_probabilities.iteritems():
                    result += float(key) * value
            except ValueError:
                result = 0
            print result
            mce_metric.add(original_cls, result)
            right_classification_ratio_metric.add(original_cls, class_probabilities)
            mcll_metric.add(original_cls, class_probabilities)
            auc_metric.add(1, 2, result)

            index += 1
            if index % 100000 == 0:
                _logger.debug("Line: " + str(index))
        _logger.debug("MSE: " + str(mce_metric.get_result()))
        _logger.debug("RightClassificationRatio: " + str(right_classification_ratio_metric.get_result()))
        _logger.debug("MultiClassLogLoss: " + str(mcll_metric.get_result()))
        _logger.debug("AUC: " + str(auc_metric.get_result()))

if __name__ == '__main__':
    main()
