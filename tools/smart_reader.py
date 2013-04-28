import gzip


class SmartReader(object):
    def open(self, filepath):
        if filepath.endswith(".gz"):
            return gzip.open(filepath, 'rb')
        else:
            return open(filepath, 'r')