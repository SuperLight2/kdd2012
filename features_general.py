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
        print "\t".join(map(str, [instance.adID, instance.advertiserID,
                                  instance.queryID, len(instance.query_tokens),
                                  instance.keywordID, len(instance.keyword_tokens),
                                  instance.titleID, len(instance.title_tokens),
                                  instance.descriptionID, len(instance.description_tokens),
                                  instance.userID, instance.user_age, instance.user_gender,
                                  instance.position, instance.depth,
                                  1.0 * instance.position / instance.depth,
                                  1.0 * (instance.position + 0.5 * 0.8) / (instance.depth + 0.5),
                                  int(instance.adID) / 1000,
                                  int(instance.advertiserID) / 1000,
                                  int(instance.queryID) / 1000,
                                  int(instance.keywordID) / 1000,
                                  int(instance.titleID) / 1000,
                                  int(instance.descriptionID) / 1000,
                                  int(instance.userID) / 1000]))


if __name__ == "__main__":
    main()