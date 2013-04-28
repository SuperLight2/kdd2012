import gzip


class SmartReader(object):
    def open(self, filepath):
        if filepath.endswith(".gz"):
            return gzip.open(filepath)
        else:
            return open(filepath)