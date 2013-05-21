from optparse import OptionParser
from tools.readers import ObjectReader
from ml_tools.spdt_classification import SimpleClassifier, SPDTClassifier, get_class_from_object
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
        for current_object in ObjectReader().open(opts.test_features):
            original_class = get_class_from_object(current_object)
            features = current_object.features
            class_probabilities = classifier_tree.calc_mc(features)

            if index < 10:
                _logger.debug("original class: " + str(original_class))
                _logger.debug("class probabilities: " + str(class_probabilities))
            result = 0
            try:
                for key, value in class_probabilities.iteritems():
                    result += float(key) * value
            except ValueError:
                result = 0
            print result
            mce_metric.add(original_class, result)
            right_classification_ratio_metric.add(original_class, class_probabilities)
            mcll_metric.add(original_class, class_probabilities)
            auc_metric.add(current_object.clicks, current_object.impressions, result)

            index += 1
            if index % 100000 == 0:
                _logger.debug("Line: " + str(index))
        _logger.debug("MSE: " + str(mce_metric.get_result()))
        _logger.debug("RightClassificationRatio: " + str(right_classification_ratio_metric.get_result()))
        _logger.debug("MultiClassLogLoss: " + str(mcll_metric.get_result()))
        _logger.debug("AUC: " + str(auc_metric.get_result()))

if __name__ == '__main__':
    main()
