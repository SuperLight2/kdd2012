import gzip


class SmartWriter(object):
    def open(self, filepath):
        if filepath.endswith(".gz"):
            return gzip.open(filepath, 'wb')
        else:
            return open(filepath, 'w')
