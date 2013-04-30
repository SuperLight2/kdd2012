from optparse import OptionParser
from tools.shell import join_all_files
from tools.feature_calcer_click_and_impression import FeatureCalcerClickAndImpression
from tools.feature_calcer_general import FeatureCalcerGeneral
from tools.features_calcer_mean_ctr import FeatureCalcerMeanCtr

import logging
_logger = logging.getLogger(__name__)


def main():
    optparser = OptionParser(usage="""
        %prog [OPTIONS] training.tsv test.tsv
        Building features pool""")
    opts, args = optparser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    training_filepath = args[0]
    test_filepath = args[1]

    train_prefix = "train_"
    test_prefix = "test_"

    feature_calcers = [
        FeatureCalcerClass(training_filepath, test_filepath,
                           train_prefix + output_filepath,
                           test_prefix + output_filepath)
        for FeatureCalcerClass, output_filepath in [
            (FeatureCalcerClickAndImpression, "features_click_and_impression.tsv"),
            (FeatureCalcerGeneral, "features_general.tsv"),
            (FeatureCalcerMeanCtr, "features_mean_ctr.tsv")]
    ]

    train_result_files = []
    test_result_files = []
    for feature_calcer in feature_calcers:
        _logger.debug("Running feature calcer: %s" % feature_calcer.result_training)
        train_result_files.append(feature_calcer.result_training)
        test_result_files.append(feature_calcer.result_test)
        feature_calcer.run()
    join_all_files(train_prefix + "features.tsv", train_result_files)
    join_all_files(test_prefix + "features.tsv", test_result_files)


if __name__ == '__main__':
    main()