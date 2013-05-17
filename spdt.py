from optparse import OptionParser


import logging
_logger = logging.getLogger(__name__)



def main():
    optparser = OptionParser(usage="""
        %prog [OPTIONS] features.tsv
        Train decision tree on features pool""")
    opts, args = optparser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")



if __name__ == '__main__':
    main()
