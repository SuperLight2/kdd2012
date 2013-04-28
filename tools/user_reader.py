from tools.data_types import User

class UserReader(object):
    def __init__(self, filepath):
        self.file = open(filepath)

    def read(self):
        result = User()
        yield result
