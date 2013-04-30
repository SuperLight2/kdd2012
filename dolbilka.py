from optparse import OptionParser
import logging
from tools.user_reader import InstanceReader
from tools.smart_writer import SmartWriter

_logger = logging.getLogger(__name__)


def main():
    optparser = OptionParser(usage="""
        %prog [OPTIONS] training.tsv test.tsv
        Building features pool""")
    opts, args = optparser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    training_filepath = args[0]
    test_filepath = args[1]

    _logger.info("Generating output column")
    with  SmartWriter().open("answer.tsv") as fout:
        for instance in InstanceReader().open(training_filepath):
            print >> fout, instance.clicks, instance.impressions


if __name__ == '__main__':
    main()