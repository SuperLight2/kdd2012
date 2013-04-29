from optparse import OptionParser
import tools.columns_replacer
import logging
import os

_logger = logging.getLogger(__name__)


def main():
    optparser = OptionParser(usage="""
        %prog [OPTIONS] training.tsv test.tsv
        Building features pool and predict CTR for test""")
    optparser.add_option('-q', '--queryid-tokensid', dest='queryid_tokensid',
        type='string', default='queryid_tokensid.txt',
        help='Path to queryid_tokensid.txt file')
    optparser.add_option('-p', '--purchasedkeyword-tokensid', dest='purchasedkeyword_tokensid',
            type='string', default='purchasedkeyword_tokensid.txt',
            help='Path to purchasedkeyword_tokensid.txt file')
    optparser.add_option('-t', '--titleid-tokensid', dest='titleid_tokensid',
            type='string', default='titleid_tokensid.txt',
            help='Path to titleid_tokensid.txt file')
    optparser.add_option('-d', '--descriptionid-tokensid', dest='descriptionid_tokensid',
            type='string', default='descriptionid_tokensid.txt',
            help='Path to descriptionid_tokensid.txt file')
    optparser.add_option('-u', '--userid_profile', dest='userid_profile',
            type='string', default='userid_profile.txt',
            help='Path to userid_profile.txt file')
    opts, args = optparser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    training_filepath = "replaced.training.tsv.gz"
    test_filepath = "replaced.test.tsv.gz"
    replace_columns = [(opts.userid_profile, 12, "0\t0"), (opts.descriptionid_tokensid, 11, ""),
                       (opts.titleid_tokensid, 10, ""), (opts.purchasedkeyword_tokensid, 9, ""),
                       (opts.queryid_tokensid, 8, "")]
    _logger.debug("Replacing columns for training")
    tools.columns_replacer.replace_columns(training_filepath, args[0], replace_columns)
    _logger.debug("Replacing columns for test")
    tools.columns_replacer.replace_columns(test_filepath, args[1], replace_columns, 2)

    for file_to_sort in [training_filepath, test_filepath]:
        _logger.debug("Sorting %s" % file_to_sort)
        os.system("gunzip -c %s | sort -nr -k 16,16 -k 8,8 -k 6,6 -k 7,7n | gzip -c > new.%s" % (file_to_sort, file_to_sort))


if __name__ == '__main__':
    main()