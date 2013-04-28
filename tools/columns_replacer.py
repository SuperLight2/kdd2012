import os
from smart_reader import SmartReader
from smart_writer import SmartWriter
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

        filepath_copy = "copy.tmp.file" + replacing_filepath[-3:]
        filepath_new = "new.tmp.file" + replacing_filepath[-3:]
        os.system("cp %s %s" % (replacing_filepath, filepath_copy))
        with SmartWriter().open(filepath_new) as file_new:
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
                print >> file_new, "\t".join(map(str, s))
            file_new.close()
        os.system("mv %s %s" % (filepath_new, filepath_copy))
        _logger.debug("Not matched uniq ids = %d" % len(not_mathed_ids))
        _logger.debug("Not matched lines = %d" % not_mathed_lines)
    os.system("mv %s %s" % (filepath_copy, result_filepath))
