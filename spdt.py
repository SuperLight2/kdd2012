from optparse import OptionParser
from tools.readers import ObjectReader
from ml_tools.spdt_classification import SimpleClassifier, SPDTClassifier, get_class_from_object
from ml_tools.metrics import RightClassificationRatio, MulticlassLogloss, MSE, AUC

import logging
_logger = logging.getLogger(__name__)


def calc_on_test(decision_tree, test_filepath):
    mce_metric = MSE()
    right_classification_ratio_metric = RightClassificationRatio()
    mcll_metric = MulticlassLogloss()
    auc_metric = AUC()
    index = 0
    for current_object in ObjectReader().open(test_filepath):
        original_class = get_class_from_object(current_object)
        features = current_object.features
        class_probabilities = decision_tree.calc_mc(features)

        #if index < 10:
        #    _logger.debug("original class: " + str(original_class))
        #    _logger.debug("class probabilities: " + str(class_probabilities))
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
        #if index % 100000 == 0:
        #    _logger.debug("Line: " + str(index))
    _logger.debug("MSE: " + str(mce_metric.get_result()))
    _logger.debug("RightClassificationRatio: " + str(right_classification_ratio_metric.get_result()))
    _logger.debug("MultiClassLogLoss: " + str(mcll_metric.get_result()))
    auc = auc_metric.get_result()
    if auc < 0.5:
        auc = 1 - auc
    _logger.debug("AUC: " + str(auc))


def main():
    optparser = OptionParser(usage="""
        %prog [OPTIONS] features.tsv
        Train decision tree on features pool""")
    optparser.add_option('-t', '--test', dest='test_features',
                         type='string', default=None,
                         help='Use test features to calc')
    optparser.add_option('-v', '--verbose', dest='verbose',
        default=False, action='store_true',
        help='output debug information')
    opts, args = optparser.parse_args()

    loglevel = logging.INFO
    if opts.verbose:
        loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel, format="%(asctime)s - %(levelname)s - %(message)s")

    _logger.debug("Begin training")
    #classifier_tree = SimpleClassifier().learn(args[0])
    classifier_tree = SPDTClassifier().learn(args[0])
    index = 1
    #for tree in SPDTClassifier().learn(args[0]):
    #    _logger.debug("Total nodes:" + str(index))
    #    calc_on_test(tree, opts.test_features)
    #    index += 1
    _logger.debug("End training")

    if opts.test_features is not None:
        calc_on_test(classifier_tree, opts.test_features)

if __name__ == '__main__':
    main()
