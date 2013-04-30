from optparse import OptionParser
from tools.shell import shell_cmd, join_all_files, calc_script
import logging
_logger = logging.getLogger(__name__)


class FeatureDescriptor(object):
    def __init__(self, script_filepath, result_filepath):
        self.script_filepath = script_filepath
        self.result_filepath = result_filepath

def main():
    optparser = OptionParser(usage="""
        %prog [OPTIONS] training.tsv test.tsv
        Building features pool""")
    opts, args = optparser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    training_filepath = args[0]
    test_filepath = args[1]

    features_groups = {
        "click_and_impression": FeatureDescriptor("features_click_and_impression.tsv", "features_click_and_impression.py"),
    }

    for group, descriptor in features_groups.iteritems():
        for prefix, data_filepath in zip(["train_", "test_"], [training_filepath, test_filepath]):
            calc_script(prefix + descriptor.result_filepath, descriptor.script_filepath, data_filepath)


if __name__ == '__main__':
    main()