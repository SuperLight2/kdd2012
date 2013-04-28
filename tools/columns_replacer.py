import shutil
from smart_reader import SmartReader
import logging

_logger = logging.getLogger(__name__)


def replace_columns(result_filepath, replacing_filepath, replace_columns, dindex = 0):
    _logger.debug("Result file: %s" % result_filepath)
    _logger.debug("Replacing file: %s" % replacing_filepath)
    for filepath, column_id, not_mathed_value in replace_columns:
        _logger.debug("Replacing Column id = %d" % column_id)
        _logger.debug("Filepath = %s" % filepath)
        d = {}
        for line in SmartReader().open(filepath):
            s = line.strip().split('\t')
            key = s[0]
            value = "\t".join(s[1:])
            d[key] = value
        not_mathed_ids = set()
        not_mathed_lines = 0

        filepath_copy = replacing_filepath + ".copy"
        shutil.copy(replacing_filepath, filepath_copy)
        with open(filepath_copy + ".new", "w") as filepath_new:
            for line in SmartReader().open(filepath_copy):
                s = line.strip().split('\t')
                key = s[column_id - 1 - dindex]
                if key not in d:
                    not_mathed_ids.add(key)
                    not_mathed_lines += 1
                    value = not_mathed_value
                else:
                    value = d[key]
                s[column_id - 1 - dindex] = "\t".join(map(str, [key, value]))
                print >> filepath_new, "\t".join(map(str, s))
        shutil.move(filepath_new, filepath_copy)
        _logger.debug("Not matched uniq ids = %d" % len(not_mathed_ids))
        _logger.debug("Not matched lines = %d" % len(not_mathed_lines))
    shutil.move(filepath_copy, result_filepath)