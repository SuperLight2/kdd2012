#!/usr/bin/env python

from optparse import OptionParser
from tools.readers import InstanceReader

import logging
_logger = logging.getLogger(__name__)


def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] INPUT_FILE""")
    opts, args = optparser.parse_args()

    _logger.info("Generating output column")
    for instance in InstanceReader().open(args[0]):
        if instance.clicks == 0:
            print 0
        else:
            print 1.0 * instance.clicks / instance.impressions


if __name__ == "__main__":
    main()