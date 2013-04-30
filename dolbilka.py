from optparse import OptionParser
import os
import time

import logging
_logger = logging.getLogger(__name__)


def shell_cmd(cmd):
    _logger.info(cmd)
    os.system(cmd)


def join_all_files(result_file, files_to_join):
    tmp_filepath = "dirty_tmp_file.never_used_2432"
    shell_cmd("rm -f %s; cp %s %s" % (result_file, files_to_join[0], result_file))
    for filepath in files_to_join[1:]:
        _logger.info("Joining %s" % filepath)
        os.system("paste %s %s > %s; mv %s %s" % (result_file, filepath, tmp_filepath, tmp_filepath, result_file))
    os.system("rm -f %s" % tmp_filepath)


def calc_script(result_file, script_filepath, data_file, arguments = None):
    _logger.info("Running %s script..." % script_filepath)
    os.system("rm -f %s" % result_file)
    if script_filepath.endswith(".py"):
        script_filepath = "python " + script_filepath
    if arguments is None:
        arguments = []
    running_time = time()
    shell_cmd("%s %s %s > %s" % (script_filepath, data_file, " ".join(arguments), result_file))
    _logger.info("Running time: %s sec" % str(time() - running_time))
    return result_file


def main():
    optparser = OptionParser(usage="""
        %prog [OPTIONS] training.tsv test.tsv
        Building features pool""")
    opts, args = optparser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    training_filepath = args[0]
    test_filepath = args[1]

    calc_script("train_" + "features_click_and_impression.tsv", "features_click_and_impression.py", training_filepath)
    calc_script("train_" + "features_click_and_impression.tsv", "features_click_and_impression.py", training_filepath)


if __name__ == '__main__':
    main()