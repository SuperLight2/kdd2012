import shutil
from smart_reader import SmartReader
import logging

_logger = logging.getLogger(__name__)


def replace_columns(result_filepath, replacing_filepath, replace_columns, dindex = 0):
    _logger.debug("Result file: %s" % result_filepath)
    _logger.debug("Replacing file: %s" % replacing_filepath)
    for filepath, column_id in replace_columns:
        _logger.debug("Replacing Column id = %d" % column_id)
        _logger.debug("Filepath = %s" % filepath)
        d = {}
        for line in SmartReader().open(filepath):
            s = line.strip().split('\t')
            key = s[0]
            value = "\t".join(s[1:])
            d[key] = value
        if "0" not in d:
            d["0"] = "\t".join(["0", "0"])

        filepath_copy = replacing_filepath + ".copy"
        shutil.copy(replacing_filepath, filepath_copy)
        with open(filepath_copy + ".new", "w") as filepath_new:
            for line in SmartReader().open(filepath_copy):
                s = line.strip().split('\t')
                key = s[column_id - 1 - dindex]
                s[column_id - 1 - dindex] = "\t".join(map(str, [key, d[key]]))
                print >> filepath_new, "\t".join(map(str, s))
        shutil.move(filepath_new, filepath_copy)
    shutil.move(filepath_copy, result_filepath)