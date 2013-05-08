from optparse import OptionParser
from tools.readers import InstanceReader
from types import ListType
from tools.smart_writer import SmartWriter

import logging
_logger = logging.getLogger(__name__)


def main():
    optparser = OptionParser(usage="""
        %prog [OPTIONS] training.tsv test.tsv
        Building features pool""")
    opts, args = optparser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    train_filepath = args[0]
    test_filepath = args[1]

    ATTRIBUTES = ["adID", "advertiserID", "displayURL", "depth", "position", "queryID", "keywordID", "titleID",
                  "descriptionID", "userID", "user_gender", "user_age", "query_tokens", "title_tokens",
                  "keyword_tokens", "description_tokens"]
    _logger.debug("Calcing max attribute values")
    max_attribute_value = dict()
    for filepath in [train_filepath, test_filepath]:
        for instance in InstanceReader().open(filepath):
            for attribute in ATTRIBUTES:
                if attribute not in max_attribute_value:
                    max_attribute_value[attribute] = 0
                attribute_value = getattr(instance, attribute)
                if not isinstance(attribute_value, ListType):
                    attribute_value = [attribute_value]
                for value in attribute_value:
                    max_attribute_value[attribute] = max(int(value), max_attribute_value[attribute])

    _logger.debug("Making result files")
    for filepath, result_filepath in [(train_filepath, "train_vw_features.tsv.gz"),
                                      (test_filepath, "test_vw_features.tsv.gz")]:
        with SmartWriter().open(result_filepath) as result_file:
            for instance in InstanceReader().open(filepath):
                class_type = "-1"
                if instance.clicks:
                    class_type = "1"

                shift = 0
                result_string = class_type + " |"
                for attribute in ATTRIBUTES:
                    attribute_value = getattr(instance, attribute)
                    if not isinstance(attribute_value, ListType):
                        attribute_value = [attribute_value]
                    for value in attribute_value:
                        result_string += " %s:1" % str(int(value) + shift)
                    shift += max_attribute_value[attribute] + 1
                print >> result_file, result_string
            result_file.close()

if __name__ == "__main__":
    main()