from smart_reader import SmartReader
from data_types import Instance, User


class UserReader(object):
    def __init__(self):
        self.current_instance = None
        self.current_user = None

    def open(self, filename):
        for line in SmartReader().open(filename):
            instance = Instance(line)
            if self.current_user is None:
                self.current_user = User(instance.userID, instance.user_gender, instance.user_age)
            if self.current_user.userID != instance.userID:
                yield self.current_user
                self.current_user = User(instance.userID, instance.user_gender, instance.user_age)
            self.current_user.add_instance(instance)
        if self.current_user is not None:
            yield self.current_user


class InstanceReader(object):
    def open(self, filename):
        for line in SmartReader().open(filename):
            if not line.strip():
                yield Instance(line)
